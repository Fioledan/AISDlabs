A = []
with open('input.txt', 'r') as file:
    for line in file:
        row = [int(x) for x in line.strip().split()]
        A.append(row)

N = len(A)
F = [row[:] for row in A]

B = [row[:] for row in A]
region1 = [(i, j) for i in range(N) for j in range(N) if i < j and i < N-1-j]
region4 = [(i, j) for i in range(N) for j in range(N) if i > j and i < N-1-j]

for (i1, j1), (i4, j4) in zip(region1, region4):
    B[i1][j1], B[i4][j4] = B[i4][j4], B[i1][j1]

K = 2
A_T = [[A[j][i] for j in range(N)] for i in range(N)]
F_plus_A = [[F[i][j] + A[i][j] for j in range(N)] for i in range(N)]
K_A_T = [[K * A_T[i][j] for j in range(N)] for i in range(N)]
term1 = [[K_A_T[i][j] * F_plus_A[i][j] for j in range(N)] for i in range(N)]
F_T = [[F[j][i] for j in range(N)] for i in range(N)]
K_F_T = [[K * F_T[i][j] for j in range(N)] for i in range(N)]
F = [[term1[i][j] - K_F_T[i][j] for j in range(N)] for i in range(N)]

for i in range(N):
    print(' '.join(map(str, F[i])))