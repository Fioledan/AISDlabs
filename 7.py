import tkinter as tk
from tkinter import messagebox, scrolledtext
from itertools import permutations

# Функция генерации перестановок
def generate():
    try:
        k = int(entry_k.get())
        n = int(entry_n.get())

        if k < n:
            messagebox.showerror("Ошибка", "K должно быть больше или равно N.")
            return
        if k <= 0 or n <= 0:
            messagebox.showerror("Ошибка", "Введите положительные числа.")
            return

        fighters = list(range(1, k + 1))
        results = list(permutations(fighters, n))

        output.delete(1.0, tk.END)
        output.insert(tk.END, f"Всего вариантов: {len(results)}\n\n")
        for r in results:
            output.insert(tk.END, f"{r}\n")

    except ValueError:
        messagebox.showerror("Ошибка", "Введите целые числа.")

# Интерфейс
root = tk.Tk()
root.title("Назначения бойцов на объекты")

tk.Label(root, text="K (бойцы):").pack()
entry_k = tk.Entry(root)
entry_k.pack()

tk.Label(root, text="N (объекты):").pack()
entry_n = tk.Entry(root)
entry_n.pack()

tk.Button(root, text="Сгенерировать", command=generate).pack(pady=10)

output = scrolledtext.ScrolledText(root, width=50, height=20)
output.pack()

root.mainloop()
