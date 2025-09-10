import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import math


class Square:
    def __init__(self, x, y, side, color="black"):
        self.x = x
        self.y = y
        self.side = side
        self.color = color

    def scale(self, factor):
        """Масштабирование квадрата"""
        if factor > 0:
            self.side = int(self.side * factor)

    def recolor(self, new_color):
        """Смена цвета"""
        self.color = new_color

    def rotate(self, angle):
        """Поворот вокруг центра (угол в градусах)"""
        rad = math.radians(angle)
        half = self.side / 2

        # Координаты вершин до поворота
        points = [
            (-half, -half),
            (half, -half),
            (half, half),
            (-half, half)
        ]

        rotated = []
        for (px, py) in points:
            rx = px * math.cos(rad) - py * math.sin(rad)
            ry = px * math.sin(rad) + py * math.cos(rad)
            rotated.append((self.x + rx, self.y + ry))
        return rotated

    def draw(self, canvas, angle=0):
        """Отрисовка квадрата"""
        points = self.rotate(angle)
        flat_points = [coord for point in points for coord in point]
        canvas.create_polygon(flat_points, fill=self.color, outline="black")


class SquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №8 — Вариант 27")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.squares = []
        self.current_angle = 0

        # Цвета для циклической смены
        self.colors = ["red", "green", "blue", "yellow", "purple", "orange"]

        # Кнопки
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Загрузить квадраты", command=self.load_squares).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame, text="Масштабировать x2", command=lambda: self.scale_all(2)).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Уменьшить в 2 раза", command=lambda: self.scale_all(0.5)).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Сменить цвет", command=self.change_color).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Повернуть на 30°", command=lambda: self.rotate_all(30)).grid(row=0, column=4, padx=5)

    def load_squares(self):
        """Загрузка квадратов из CSV файла"""
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filename:
            return

        try:
            with open(filename, newline="") as csvfile:
                reader = csv.reader(csvfile)
                self.squares = []
                for row in reader:
                    if len(row) != 4:
                        raise ValueError("Неверный формат строки")
                    x, y, side, color = row
                    self.squares.append(Square(int(x), int(y), int(side), color))
            self.draw_all()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def draw_all(self):
        """Перерисовка всех квадратов"""
        self.canvas.delete("all")
        for sq in self.squares:
            sq.draw(self.canvas, self.current_angle)

    def scale_all(self, factor):
        """Масштабирование всех квадратов"""
        for sq in self.squares:
            sq.scale(factor)
        self.draw_all()

    def change_color(self):
        """Циклическая смена цвета"""
        for sq in self.squares:
            try:
                idx = self.colors.index(sq.color)
                sq.recolor(self.colors[(idx + 1) % len(self.colors)])
            except ValueError:
                sq.recolor(self.colors[0])  # если цвет неизвестный, ставим первый
        self.draw_all()

    def rotate_all(self, angle):
        """Поворот всех квадратов"""
        self.current_angle += angle
        self.draw_all()


if __name__ == "__main__":
    root = tk.Tk()
    app = SquareApp(root)
    root.mainloop()
