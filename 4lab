import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

with open('4lab_input.txt', 'r') as f:
    K = int(f.readline())
    A = np.array([list(map(int, line.split())) for line in f])

N = len(A)
F = A.copy()
n = N // 2
E, B, D, C = A[:n, :n], A[:n, n:], A[n:, :n], A[n:, n:]
perim = np.r_[E[0, :], E[-1, :], E[1:-1, 0], E[1:-1, -1]]

if perim.sum() > (perim == 0).sum():
    F[:n, n:], F[n:, n:] = C.T, B.T
else:
    F[:n, :n], F[:n, n:] = B, E

det_A = np.linalg.det(A)
diag_F = F.trace()

if det_A > diag_F:
    F = A @ A.T - K * F
else:
    F = (np.linalg.inv(A) + np.tril(A) - np.linalg.inv(F)) * K

plt.figure(figsize=(6, 4))
plt.imshow(F, cmap='coolwarm')
plt.colorbar()
plt.title("Тепловая карта F")
plt.show()

plt.figure(figsize=(6, 4))
plt.bar(range(N), F.sum(axis=1), color='coral')
plt.title("Сумма строк F")
plt.xlabel("Строка")
plt.ylabel("Сумма")
plt.show()

plt.figure(figsize=(6, 4))
plt.hist(F.flatten(), bins=10, color='lightblue', edgecolor='black')
plt.title("Гистограмма F")
plt.xlabel("Значение")
plt.ylabel("Частота")
plt.show()

input("Нажмите Enter для завершения...")
