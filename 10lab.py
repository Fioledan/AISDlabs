import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Крестики-нолики")
root.geometry("400x500")
root.configure(bg="yellow")

board = [""] * 9
game_over = False
BOT = "X"
HUMAN = "O"

def check_win(b):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for w in wins:
        if b[w[0]] == b[w[1]] == b[w[2]] != "":
            return b[w[0]]
    return None

def bot_move():
    # Попытка победить
    for i in range(9):
        if board[i] == "":
            board[i] = BOT
            if check_win(board) == BOT:
                return i
            board[i] = ""
    # Блокировка
    for i in range(9):
        if board[i] == "":
            board[i] = HUMAN
            if check_win(board) == HUMAN:
                board[i] = ""
                return i
            board[i] = ""
    # Приоритет: центр → углы → остальное
    for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if board[i] == "":
            return i
    return -1

def on_click(i):
    global game_over
    if board[i] != "" or game_over:
        return

    # Ход игрока (O)
    board[i] = HUMAN
    btns[i].config(text=HUMAN, fg="blue", state="disabled")

    # Проверка: может ли игрок победить?
    if check_win(board) == HUMAN:
        # Теоретически невозможно
        game_over = True
        root.configure(bg="blue")
        messagebox.showinfo("Победа?", "Это не должно было произойти!")
        return

    if "" not in board:
        game_over = True
        root.configure(bg="gray")
        messagebox.showinfo("Ничья!", "Ничья!")
        return

    # Ход бота (X)
    bi = bot_move()
    if bi != -1:
        board[bi] = BOT
        btns[bi].config(text=BOT, fg="red", state="disabled")

        winner = check_win(board)
        if winner == BOT:
            game_over = True
            root.configure(bg="red")
            messagebox.showinfo("Поражение", "Бот победил! Ты проиграл.")
        elif "" not in board:
            game_over = True
            root.configure(bg="gray")
            messagebox.showinfo("Ничья!", "Ничья!")

def reset():
    global board, game_over
    board = [""] * 9
    game_over = False
    root.configure(bg="yellow")
    for b in btns:
        b.config(text="", state="normal", fg="black")
    # Бот делает первый ход!
    first_move = bot_move()
    if first_move != -1:
        board[first_move] = BOT
        btns[first_move].config(text=BOT, fg="red", state="disabled")

# Создание кнопок
btns = []
for i in range(9):
    btn = tk.Button(root, text="", font=("Arial", 24), width=5, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    btns.append(btn)

tk.Button(root, text="Новая игра", bg="lightgreen", command=reset).grid(row=3, column=0, columnspan=3, pady=10)
tk.Label(root, text="Ты — O (синий)\nБот — X (красный, ходит первым)",
         bg="yellow", font=("Arial", 9)).grid(row=4, column=0, columnspan=3)

# Первый ход бота при запуске
reset()

root.mainloop()