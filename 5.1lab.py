import time
import random
from itertools import permutations


# Генерация допустимых перестановок с учетом ограничений
def generate_valid_assignments(fighters, skills, objects, min_skills):
    valid_perms = []
    for perm in permutations(fighters, len(objects)):
        valid = True
        for i, fighter in enumerate(perm):
            if skills[fighter - 1] < min_skills[i]:  # Проверка ограничения
                valid = False
                break
        if valid:
            valid_perms.append(perm)
    return valid_perms


# Основная функция для части 2
def part2(K, N):
    print(" Часть 2: Усложнение с ограничениями и целевой функцией")

    # Проверка краевых случаев
    if K < N:
        print("Ошибка: Количество бойцов должно быть не меньше количества объектов.")
        return
    if K <= 0 or N <= 0:
        print("Ошибка: K и N должны быть положительными.")
        return

    # Генерация характеристик
    random.seed(42)  # Для воспроизводимости
    fighters = list(range(1, K + 1))  # Бойцы: [1, 2, ..., K]
    skills = [random.randint(1, 10) for _ in range(K)]  # Уровни подготовки бойцов
    min_skills = [random.randint(1, 5) for _ in range(N)]  # Минимальные требования объектов

    print(f"Уровни подготовки бойцов: {skills}")
    print(f"Минимальные требования объектов: {min_skills}")

    # Генерация допустимых назначений
    start_time = time.time()
    valid_perms = generate_valid_assignments(fighters, skills, list(range(N)), min_skills)
    time_taken = time.time() - start_time

    print(f"\nКоличество допустимых вариантов: {len(valid_perms)}")
    print(f"Время выполнения: {time_taken:.6f} секунд")

    # Нахождение оптимального решения (максимизация суммарного уровня подготовки)
    max_skill_sum = -1
    best_perm = None
    for perm in valid_perms:
        skill_sum = sum(skills[fighter - 1] for fighter in perm)
        if skill_sum > max_skill_sum:
            max_skill_sum = skill_sum
            best_perm = perm

    # Вывод результата
    if best_perm:
        print(f"\nОптимальное назначение: {best_perm}")
        print(f"Суммарный уровень подготовки: {max_skill_sum}")
        print("Назначение бойцов на объекты:")
        for i, fighter in enumerate(best_perm):
            print(f"Объект {i + 1}: Боец {fighter} (уровень подготовки: {skills[fighter - 1]})")
    else:
        print("\nНет допустимых назначений.")


# Тест
K = 5
N = 3
part2(K, N)
