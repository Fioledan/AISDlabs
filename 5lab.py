import time
from itertools import permutations
# Алгоритмический подход: рекурсивная генерация перестановок с учетом уникальности бойцов
def generate_assignments_algo(k, n):
    result = []
    used = [False] * k  # Массив для отслеживания использованных бойцов

    def backtrack(assignment, obj_idx):
        if obj_idx == n:  # Если назначены все объекты
            result.append(assignment[:])
            return
        for i in range(k):
            if not used[i]:  # Если боец еще не использован
                used[i] = True
                assignment.append(i + 1)  # Добавляем бойца (нумерация с 1)
                backtrack(assignment, obj_idx + 1)
                assignment.pop()
                used[i] = False

    backtrack([], 0)
    return result
# Подход с использованием itertools.permutations
def generate_assignments_itertools(k, n):
    fighters = list(range(1, k + 1))  # Список бойцов: [1, 2, ..., K]
    return list(permutations(fighters, n))
    
# Основная функция для части 1
def part1(K, N):
    print("=== Часть 1: Генерация всех возможных назначений ===")

    # Проверка краевых случаев
    if K < N:
        print("Ошибка: Количество бойцов должно быть не меньше количества объектов.")
        return
    if K <= 0 or N <= 0:
        print("Ошибка: K и N должны быть положительными.")
        return
   
    start_time = time.time()
    assignments_algo = generate_assignments_algo(K, N)
    algo_time = time.time() - start_time
    print(f"Алгоритмический подход: {len(assignments_algo)} вариантов")
    print(f"Время выполнения: {algo_time:.6f} секунд")
    print("Первые 5 вариантов (или все, если их меньше):")
    for perm in assignments_algo[:min(5, len(assignments_algo))]:
        print(perm)


    start_time = time.time()
    assignments_itertools = generate_assignments_itertools(K, N)
    itertools_time = time.time() - start_time
    print(f"\nПодход с itertools: {len(assignments_itertools)} вариантов")
    print(f"Время выполнения: {itertools_time:.6f} секунд")
    print("Первые 5 вариантов (или все, если их меньше):")
    for perm in assignments_itertools[:min(5, len(assignments_itertools))]:
        print(perm)

    print(f"\nСравнение: itertools быстрее на {(algo_time - itertools_time):.6f} секунд")

# Тест
K = 5 
N = 3 
part1(K, N)
