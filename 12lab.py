import tkinter as tk
import random, time

# размеры лабиринта
W, H = 31, 31 
CELL = 20

# окно
root = tk.Tk()
root.title("Лабиринт - поиск пути")
canvas = tk.Canvas(root, width=W*CELL, height=H*CELL, bg="#1c1c1c")
canvas.pack()

maze = [['#'] * W for _ in range(H)]

# генерация лабиринта (рекурсивно)
def carve(x, y):
    dirs = [(2,0), (-2,0), (0,2), (0,-2)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x+dx, y+dy
        if 0<nx<W-1 and 0<ny<H-1 and maze[ny][nx] == '#':
            maze[ny-dy//2][nx-dx//2] = ' '
            maze[ny][nx] = ' '
            carve(nx, ny)

# старт — центр
maze[H//2][W//2] = ' '
carve(W//2, H//2)

# выбираем выход
edges = [(x,0) for x in range(W)] + [(x,H-1) for x in range(W)] + [(0,y) for y in range(H)] + [(W-1,y) for y in range(H)]
free_edges = [p for p in edges if maze[p[1]][p[0]] == ' ']
if not free_edges:
    side = random.choice(['top','bottom','left','right'])
    if side == 'top': ex = (random.randrange(1,W-1,2), 0)
    elif side == 'bottom': ex = (random.randrange(1,W-1,2), H-1)
    elif side == 'left': ex = (0, random.randrange(1,H-1,2))
    else: ex = (W-1, random.randrange(1,H-1,2))
    maze[ex[1]][ex[0]] = ' '
else:
    ex = random.choice(free_edges)
maze[ex[1]][ex[0]] = 'E'

start = (W//2, H//2)

# рисуем квадрат
def draw_cell(x, y, color):
    canvas.create_rectangle(
        x*CELL, y*CELL, (x+1)*CELL, (y+1)*CELL,
        fill=color, outline="#2b2b2b"
    )

# рисуем лабиринт
def draw_maze():
    canvas.delete("all")
    for y in range(H):
        for x in range(W):
            c = maze[y][x]
            if c == '#':
                draw_cell(x, y, "#2d2d2d")
            elif c == 'E':
                draw_cell(x, y, "#8b0000")
            else:
                draw_cell(x, y, "#bfbfbf")
    draw_cell(*start, "#00ff6a")
    root.update()

draw_maze()

# BFS (поиск пути)
queue = [start]
visited = {start}
parent = {}
found = None

def step():
    global found
    if queue and not found:
        x, y = queue.pop(0)
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H and maze[ny][nx] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                draw_cell(nx, ny, "#9c27b0")  # фиолетовый — просмотренные
                if maze[ny][nx] == 'E':
                    found = (nx, ny)
                    root.after(100, show_path)
                    return
                queue.append((nx, ny))
        root.after(20, step)

def show_path():
    cur = found
    while cur != start:
        x, y = cur
        draw_cell(x, y, "#ff9800")  # оранжевый путь
        cur = parent[cur]
        root.update()
        time.sleep(0.03)
    draw_cell(*start, "#00ff6a")

# старт визуализации
root.after(500, step)
root.mainloop()
