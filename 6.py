import time
import matplotlib.pyplot as plt

# Функция для вычисления факториала (для рекурсии)
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Рекурсивная функция с мемоизацией
def F_recursive(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 1 or n == 2:
        memo[n] = 1
        return 1
    sign = -1 if n % 2 else 1
    memo[n] = sign * (F_recursive(n - 1, memo) // factorial(n))
    return memo[n]

# Итеративная функция с использованием одной переменной
def F_iterative(n):
    if n == 1 or n == 2:
        return 1
    f_prev = 1  # F(2)
    factorial = 2  # 2!
    for i in range(3, n + 1):
        factorial *= i  # Обновляем факториал
        sign = -1 if i % 2 else 1  # Знак (-1)^i
        f_current = sign * (f_prev // factorial)
        f_prev = f_current  # Обновляем предыдущее значение
    return f_prev

# Функция для измерения времени
def measure_time(func, n):
    start = time.perf_counter()
    result = func(n)
    end = time.perf_counter()
    return result, end - start

# Основная программа
n_values = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
recursive_times = []
iterative_times = []
recursive_values = []
iterative_values = []

print("n\tРекурсия\tВремя (рек)\tИтерация\tВремя (итер)")
print("-" * 60)
for n in n_values:
    try:
        res_rec, time_rec = measure_time(F_recursive, n)
    except (RecursionError, OverflowError):
        res_rec, time_rec = "Ошибка", None
    res_iter, time_iter = measure_time(F_iterative, n)
    
    recursive_times.append(time_rec if time_rec is not None else float('inf'))
    iterative_times.append(time_iter)
    recursive_values.append(res_rec)
    iterative_values.append(res_iter)
    
    rec_time_str = f"{time_rec:.6f}" if time_rec is not None else "Ошибка"
    print(f"{n}\t{res_rec}\t\t{rec_time_str}\t{res_iter}\t\t{time_iter:.6f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(n_values, recursive_times, label="Рекурсия (с мемоизацией)", marker='o')
plt.plot(n_values, iterative_times, label="Итерация", marker='s')
plt.xlabel("n")
plt.ylabel("Время выполнения (сек)")
plt.title("Сравнение времени выполнения рекурсивного и итеративного подходов")
plt.legend()
plt.grid(True)
plt.savefig("time_comparison.png")
plt.show()
