import tkinter as tk
import random

SIZE = 10
FLEET = [4,3,3,2,2,2,1,1,1,1]

class Board:
    def __init__(self, hide=False):
        self.hide = hide
        self.ships = []
        self.grid = [[None]*SIZE for _ in range(SIZE)]
        self.shots = [[None]*SIZE for _ in range(SIZE)]
    def can_place(self,x,y,L,horiz):
        cells=[(x+i,y) if horiz else (x,y+i) for i in range(L)]
        for cx,cy in cells:
            if not(0<=cx<SIZE and 0<=cy<SIZE): return False
            if self.grid[cy][cx] is not None: return False
            for dx in(-1,0,1):
                for dy in(-1,0,1):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<SIZE and 0<=ny<SIZE and self.grid[ny][nx] is not None:
                        return False
        return True
    def place_ship(self,x,y,L,horiz):
        if not self.can_place(x,y,L,horiz): return False
        cells=[(x+i,y) if horiz else (x,y+i) for i in range(L)]
        ship={'cells':cells,'hits':set()}
        for cx,cy in cells: self.grid[cy][cx]=ship
        self.ships.append(ship)
        return True
    def remove_all(self):
        self.ships.clear()
        self.grid=[[None]*SIZE for _ in range(SIZE)]
        self.shots=[[None]*SIZE for _ in range(SIZE)]
    def random_place(self):
        self.remove_all()
        for L in FLEET:
            placed=False
            while not placed:
                horiz=random.choice([True,False])
                x=random.randrange(SIZE)
                y=random.randrange(SIZE)
                if self.place_ship(x,y,L,horiz):
                    placed=True
    def receive_shot(self,x,y):
        if self.shots[y][x] is not None: return None
        ship=self.grid[y][x]
        if ship is None:
            self.shots[y][x]='miss'
            return 'miss'
        ship['hits'].add((x,y))
        self.shots[y][x]='hit'
        if set(ship['cells'])==ship['hits']:
            self.mark_around(ship)
            return 'sank'
        return 'hit'
    def mark_around(self,ship):
        for cx,cy in ship['cells']:
            for dx in(-1,0,1):
                for dy in(-1,0,1):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<SIZE and 0<=ny<SIZE and self.shots[ny][nx] is None:
                        self.shots[ny][nx]='miss'
    def all_sunk(self):
        return all(set(s['cells'])==s['hits'] for s in self.ships)

class AI:
    def __init__(self):
        self.known=[[None]*SIZE for _ in range(SIZE)]
    def update(self,x,y,res,board):
        self.known[y][x]=res
        if res=='sank':
            for s in board.ships:
                if set(s['cells'])==s['hits']:
                    for cx,cy in s['cells']:
                        self.known[cy][cx]='sank'
                        for dx in(-1,0,1):
                            for dy in(-1,0,1):
                                nx,ny=cx+dx,cy+dy
                                if 0<=nx<SIZE and 0<=ny<SIZE and self.known[ny][nx] is None:
                                    self.known[ny][nx]='miss'
    def neighbors(self,x,y):
        for dx,dy in[(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<SIZE and 0<=ny<SIZE: yield nx,ny
    def choose(self,board):
        hits=[(x,y) for y in range(SIZE) for x in range(SIZE) if self.known[y][x]=='hit']
        if hits:
            for x,y in hits:
                for nx,ny in self.neighbors(x,y):
                    if self.known[ny][nx] is None: return nx,ny
        probs=[[0]*SIZE for _ in range(SIZE)]
        remain=[len(s['cells'])-len(s['hits']) for s in board.ships if len(s['hits'])<len(s['cells'])]
        if not remain: remain=[1]
        for L in remain:
            for y in range(SIZE):
                for x in range(SIZE-L+1):
                    if all(self.known[y][x+i] in (None,'hit') for i in range(L)):
                        for i in range(L):
                            if self.known[y][x+i] is None: probs[y][x+i]+=1
            for x in range(SIZE):
                for y in range(SIZE-L+1):
                    if all(self.known[y+i][x] in (None,'hit') for i in range(L)):
                        for i in range(L):
                            if self.known[y+i][x] is None: probs[y+i][x]+=1
        best=max((probs[y][x],x,y) for y in range(SIZE) for x in range(SIZE) if self.known[y][x] is None)
        return best[1],best[2]

class Game:
    def __init__(self,root):
        self.root=root
        self.root.title("Морской бой")
        self.player=Board()
        self.enemy=Board(True)
        self.ai=AI()
        self.dir=True
        self.idx=0
        self.started=False
        self.make_ui()
        self.draw()
    def make_ui(self):
        top=tk.Frame(self.root)
        top.pack()
        self.pf=tk.Frame(top)
        self.cf=tk.Frame(top)
        self.pf.pack(side='left',padx=10)
        self.cf.pack(side='left',padx=10)
        self.pb=[]
        self.cb=[]
        for y in range(SIZE):
            rowp=[]
            rowc=[]
            for x in range(SIZE):
                bp=tk.Button(self.pf,width=2,command=lambda x=x,y=y:self.click_player(x,y))
                bc=tk.Button(self.cf,width=2,command=lambda x=x,y=y:self.shoot(x,y))
                bp.grid(row=y,column=x)
                bc.grid(row=y,column=x)
                rowp.append(bp); rowc.append(bc)
            self.pb.append(rowp)
            self.cb.append(rowc)
        ctrl=tk.Frame(self.root)
        ctrl.pack(pady=10)
        tk.Button(ctrl,text="Сменить направление",command=self.toggle).grid(row=0,column=0,padx=5)
        tk.Button(ctrl,text="Случайная расстановка",command=self.rand_place).grid(row=0,column=1,padx=5)
        self.start=tk.Button(ctrl,text="Старт",command=self.start_game)
        self.start.grid(row=0,column=2,padx=5)
        self.status=tk.Label(self.root,text="Расставьте корабли")
        self.status.pack()
    def toggle(self):
        if not self.started:
            self.dir=not self.dir
    def rand_place(self):
        if not self.started:
            self.player.random_place()
            self.idx=len(FLEET)
            self.draw()
    def click_player(self,x,y):
        if self.started: return
        if self.idx>=len(FLEET): return
        L=FLEET[self.idx]
        if self.player.place_ship(x,y,L,self.dir):
            self.idx+=1
            self.draw()
    def draw(self):
        for y in range(SIZE):
            for x in range(SIZE):
                v=self.player.grid[y][x]
                sh=self.player.shots[y][x]
                b=self.pb[y][x]
                if v: b.config(bg='lightgrey')
                else: b.config(bg='SystemButtonFace',text='')
                if sh=='miss': b.config(text='X')
                elif sh=='hit': b.config(bg='red')
        for y in range(SIZE):
            for x in range(SIZE):
                sh=self.enemy.shots[y][x]
                b=self.cb[y][x]
                if sh=='miss': b.config(text='X',state='disabled')
                elif sh=='hit': b.config(bg='red',state='disabled')
                else: b.config(text='',bg='SystemButtonFace',state='normal' if self.started else 'disabled')
        if not self.started:
            self.status.config(text=f"Расставлено {len(self.player.ships)}/{len(FLEET)} кораблей")
    def start_game(self):
        if self.started: return
        if len(self.player.ships)!=len(FLEET): return
        self.enemy.random_place()
        self.started=True
        self.status.config(text="Ход игрока")
        self.draw()
    def shoot(self,x,y):
        if not self.started: return
        if self.enemy.shots[y][x] is not None: return
        r=self.enemy.receive_shot(x,y)
        self.draw()
        if self.enemy.all_sunk():
            self.status.config(text="Вы победили!")
            self.started=False
            return
        if r=='miss':
            self.status.config(text="Промах. Ход компьютера")
            self.root.after(300,self.cpu_turn)
        else:
            self.status.config(text="Попадание! Ваш следующий ход")
    def cpu_turn(self):
        x,y=self.ai.choose(self.player)
        r=self.player.receive_shot(x,y)
        self.ai.update(x,y,r,self.player)
        self.draw()
        if self.player.all_sunk():
            self.status.config(text="Компьютер победил!")
            self.started=False
            return
        if r=='miss':
            self.status.config(text="Ход игрока")
        else:
            self.status.config(text="Компьютер попал! Он стреляет снова")
            self.root.after(300,self.cpu_turn)

root=tk.Tk()
Game(root)
root.mainloop()
