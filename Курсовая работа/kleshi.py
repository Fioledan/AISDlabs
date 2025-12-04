import tkinter as tk
from tkinter import ttk, messagebox
import hashlib, os

N=8
EMPTY,WM,BM,WK,BK=0,1,2,3,4
CLIGHT,CDARK="#f0f0f0","#a0a0a0"
CWHITE,CBLACK,CKING="#ffffff","#000000","#444444"
PLAYERS_FILE="players.txt"

def inside(r,c): return 0<=r<N and 0<=c<N
def pcolor(p):
    if p in (WM,WK): return "white"
    if p in (BM,BK): return "black"
    return None
def is_king(p): return p in (WK,BK)
def enc(t): return hashlib.md5(t.encode("utf-8")).hexdigest()[:8]

def save_players(n1,p1,n2,p2):
    with open(PLAYERS_FILE,"w",encoding="utf-8") as f:
        f.write(enc(n1)+" "+enc(p1)+"\n")
        f.write(enc(n2)+" "+enc(p2)+"\n")

def load_players():
    if not os.path.exists(PLAYERS_FILE): return None
    with open(PLAYERS_FILE,"r",encoding="utf-8") as f:
        lines=[x.strip() for x in f if x.strip()]
    if len(lines)<2: return None
    a=lines[0].split(); b=lines[1].split()
    if len(a)!=2 or len(b)!=2: return None
    return a[0],a[1],b[0],b[1]

def check_players(n1,p1,n2,p2):
    d=load_players()
    if not d: return False
    a1,b1,a2,b2=d
    return enc(n1)==a1 and enc(p1)==b1 and enc(n2)==a2 and enc(p2)==b2

class GameState:
    def __init__(self):
        self.board=[[EMPTY]*N for _ in range(N)]
        self.current="white"
        self.reset()
    def reset(self):
        self.current="white"
        b=self.board
        for r in range(N):
            for c in range(N): b[r][c]=EMPTY
        for r in range(3):
            for c in range(N):
                if (r+c)%2: b[r][c]=BM
        for r in range(5,N):
            for c in range(N):
                if (r+c)%2: b[r][c]=WM
    def moves_from(self,r,c,color):
        p=self.board[r][c]; quiet=[]
        if p==EMPTY: return quiet
        if not is_king(p):
            step=-1 if color=="white" else 1
            for dc in (-1,1):
                nr,nc=r+step,c+dc
                if inside(nr,nc) and self.board[nr][nc]==EMPTY:
                    quiet.append((r,c,nr,nc))
        else:
            for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                nr,nc=r+dr,c+dc
                while inside(nr,nc) and self.board[nr][nc]==EMPTY:
                    quiet.append((r,c,nr,nc))
                    nr+=dr; nc+=dc
        return quiet
    def move_piece(self,r1,c1,r2,c2):
        p=self.board[r1][c1]
        self.board[r1][c1]=EMPTY
        self.board[r2][c2]=p
    def apply_pincers(self,mr,mc):
        b=self.board
        col=pcolor(b[mr][mc])
        if not col: return False
        enemy="black" if col=="white" else "white"
        victims=set()
        for dr,dc in [(-1,-1),(-1,1),(1,1),(1,-1)]:
            vr,vc=mr+dr,mc+dc
            if not inside(vr,vc): continue
            if pcolor(b[vr][vc])!=enemy: continue
            neigh=[(vr-1,vc-1),(vr-1,vc+1),(vr+1,vc+1),(vr+1,vc-1)]
            pairs=[(0,1),(1,2),(2,3),(3,0)]
            for i,j in pairs:
                a1,a2=neigh[i],neigh[j]
                if not (inside(*a1) and inside(*a2)): continue
                r1,c1=a1; r2,c2=a2
                if pcolor(b[r1][c1])==col and pcolor(b[r2][c2])==col:
                    if (r1,c1)==(mr,mc) or (r2,c2)==(mr,mc):
                        victims.add((vr,vc))
        for vr,vc in victims: b[vr][vc]=EMPTY
        return bool(victims)
    def promote(self,r,c):
        p=self.board[r][c]
        if p==WM and r==0: self.board[r][c]=WK
        if p==BM and r==N-1: self.board[r][c]=BK
    def count_pieces(self,color):
        return sum(1 for r in range(N) for c in range(N) if pcolor(self.board[r][c])==color)
    def has_moves(self,color):
        for r in range(N):
            for c in range(N):
                if pcolor(self.board[r][c])!=color: continue
                if self.moves_from(r,c,color): return True
        return False

class CheckersApp(tk.Tk):
    def __init__(self,name1,name2):
        super().__init__()
        self.title("Шашки Клещи – Поддавки")
        self.p1,self.p2=name1,name2
        self.state=GameState()
        self.cell,self.margin=64,20
        w=self.margin*2+self.cell*N
        h=self.margin*2+self.cell*N+60
        self.geometry(f"{w}x{h}")
        self.sel=None
        self.hl=[]
        self.canvas=tk.Canvas(self,width=w,height=h-60,bg="#dddddd",highlightthickness=0)
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind("<Button-1>",self.on_click)
        panel=ttk.Frame(self); panel.pack(fill=tk.X,side=tk.BOTTOM)
        ttk.Button(panel,text="Новая партия",command=self.new_game).pack(side=tk.LEFT,padx=10)
        self.info=ttk.Label(panel,text=""); self.info.pack(side=tk.RIGHT,padx=10)
        self.update_labels(); self.redraw(); self.check_for_win()
    def new_game(self):
        self.state.reset()
        self.sel,self.hl=None,[]
        self.redraw(); self.update_labels(); self.check_for_win()
    def bcoords(self,x,y):
        x-=self.margin; y-=self.margin
        if x<0 or y<0: return None
        c=x//self.cell; r=N-1-y//self.cell
        return (int(r),int(c)) if inside(r,c) else None
    def ccoords(self,r,c):
        x1=self.margin+c*self.cell
        y1=self.margin+(N-1-r)*self.cell
        return x1,y1,x1+self.cell,y1+self.cell
    def redraw(self):
        cv=self.canvas; cv.delete("all")
        for r in range(N):
            for c in range(N):
                x1,y1,x2,y2=self.ccoords(r,c)
                base=CDARK if (r+c)%2 else CLIGHT
                cv.create_rectangle(x1,y1,x2,y2,fill=base,outline="#000")
        for r,c in self.hl:
            x1,y1,x2,y2=self.ccoords(r,c)
            cv.create_rectangle(x1+3,y1+3,x2-3,y2-3,outline="#666",width=3)
        for r in range(N):
            for c in range(N):
                p=self.state.board[r][c]
                if p==EMPTY: continue
                x1,y1,x2,y2=self.ccoords(r,c)
                cx,cy=(x1+x2)/2,(y1+y2)/2
                fill=CWHITE if pcolor(p)=="white" else CBLACK
                cv.create_oval(cx-20,cy-20,cx+20,cy+20,fill=fill,outline="#000",width=2)
                if is_king(p):
                    cv.create_oval(cx-14,cy-14,cx+14,cy+14,outline=CKING,width=3)
        if self.sel:
            r,c=self.sel
            x1,y1,x2,y2=self.ccoords(r,c)
            cv.create_oval(x1+6,y1+6,x2-6,y2-6,outline="#666",width=3)
    def on_click(self,e):
        pos=self.bcoords(e.x,e.y)
        if not pos: return
        r,c=pos
        if self.sel is None:
            if pcolor(self.state.board[r][c])!=self.state.current: return
            self.select_cell(r,c)
        else:
            if (r,c)==self.sel:
                self.sel,self.hl=None,[]; self.redraw()
            else:
                self.try_move(self.sel[0],self.sel[1],r,c)
    def select_cell(self,r,c):
        self.sel=(r,c); self.hl=[]
        col=pcolor(self.state.board[r][c])
        if not col: return
        q=self.state.moves_from(r,c,col)
        for m in q: self.hl.append((m[2],m[3]))
        self.redraw()
    def try_move(self,r1,c1,r2,c2):
        col=self.state.current
        q=self.state.moves_from(r1,c1,col)
        if (r2,c2) not in {(m[2],m[3]) for m in q}: return
        self.state.move_piece(r1,c1,r2,c2)
        self.state.apply_pincers(r2,c2)
        self.state.promote(r2,c2)
        self.sel,self.hl=None,[]
        self.redraw()
        if self.check_for_win(): return
        self.state.current="black" if col=="white" else "white"
        self.update_labels(); self.redraw()
    def update_labels(self):
        side=self.p1 if self.state.current=="white" else self.p2
        self.info.config(text="Ход: "+side)
    def check_for_win(self):
        for col in ("white","black"):
            if self.state.count_pieces(col)==0 or not self.state.has_moves(col):
                self.finish_game(col); return True
        return False
    def finish_game(self,winner):
        name=self.p1 if winner=="white" else self.p2
        messagebox.showinfo("Конец партии",name+" выигрывает (поддавки).")
        self.new_game()

class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Шашки Клещи – Поддавки")
        self.geometry("420x220"); self.resizable(False,False)
        self.frame=ttk.Frame(self,padding=20); self.frame.pack()
        self.build_start()
    def clear(self):
        for w in self.frame.winfo_children(): w.destroy()
    def build_start(self):
        self.clear()
        ttk.Label(self.frame,text="Компьютерная игра «Шашки Клещи – Поддавки»").pack(pady=10)
        ttk.Button(self.frame,text="Регистрация игроков",command=self.build_reg).pack(fill=tk.X,pady=5)
        ttk.Button(self.frame,text="Вход по логину и паролю",command=self.build_log).pack(fill=tk.X,pady=5)
    def build_reg(self):
        self.clear()
        ttk.Label(self.frame,text="Регистрация игроков").grid(row=0,column=0,columnspan=2,pady=5)
        self._build_fields()
        ttk.Button(self.frame,text="Сохранить и начать",command=self.do_reg).grid(row=5,column=0,columnspan=2,pady=10)
    def build_log(self):
        if not os.path.exists(PLAYERS_FILE):
            messagebox.showerror("Ошибка","Файл players.txt ещё не создан.\nСначала зарегистрируйтесь."); return
        self.clear()
        ttk.Label(self.frame,text="Вход игроков").grid(row=0,column=0,columnspan=2,pady=5)
        self._build_fields()
        ttk.Button(self.frame,text="Начать игру",command=self.do_log).grid(row=5,column=0,columnspan=2,pady=10)
    def _build_fields(self):
        ttk.Label(self.frame,text="Игрок 1 имя:").grid(row=1,column=0,sticky="w",padx=5,pady=2)
        ttk.Label(self.frame,text="Игрок 1 пароль:").grid(row=2,column=0,sticky="w",padx=5,pady=2)
        ttk.Label(self.frame,text="Игрок 2 имя:").grid(row=3,column=0,sticky="w",padx=5,pady=2)
        ttk.Label(self.frame,text="Игрок 2 пароль:").grid(row=4,column=0,sticky="w",padx=5,pady=2)
        self.e1n=ttk.Entry(self.frame); self.e1p=ttk.Entry(self.frame,show="*")
        self.e2n=ttk.Entry(self.frame); self.e2p=ttk.Entry(self.frame,show="*")
        self.e1n.grid(row=1,column=1,padx=5,pady=2); self.e1p.grid(row=2,column=1,padx=5,pady=2)
        self.e2n.grid(row=3,column=1,padx=5,pady=2); self.e2p.grid(row=4,column=1,padx=5,pady=2)
    def get_data(self):
        n1,p1=self.e1n.get().strip(),self.e1p.get().strip()
        n2,p2=self.e2n.get().strip(),self.e2p.get().strip()
        if not n1 or not p1 or not n2 or not p2:
            messagebox.showerror("Ошибка","Заполните все поля."); return None
        return n1,p1,n2,p2
    def do_reg(self):
        d=self.get_data()
        if not d: return
        n1,p1,n2,p2=d
        save_players(n1,p1,n2,p2); self.start_game(n1,n2)
    def do_log(self):
        d=self.get_data()
        if not d: return
        n1,p1,n2,p2=d
        if not check_players(n1,p1,n2,p2):
            messagebox.showerror("Ошибка","Неверные имя или пароль."); return
        self.start_game(n1,n2)
    def start_game(self,n1,n2):
        self.destroy()
        CheckersApp(n1,n2).mainloop()

if __name__=="__main__":
    AuthApp().mainloop()
