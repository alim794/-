# transport_problem.py
# Чете данни от конзолата и решава транспортна задача със забрани (Фаза 1)

import numpy as np
from sympy import symbols, Rational

def read_list(prompt, cast=float):
    vals = input(prompt + " (запетайка-разделени): ").split(',')
    return [cast(v.strip()) for v in vals]

def read_matrix(m, n, cast=float):
    print(f"Въведете матрица {m}x{n}, всеки ред на нов ред:")
    mat = []
    for i in range(m):
        row = input(f"Ред {i+1}: ").split(',')
        if len(row) != n:
            raise ValueError("Грешен брой елементи в реда.")
        mat.append([cast(v.strip()) for v in row])
    return mat

def main():
    print("=== Фаза 1: Транспортна задача със забрани ===")
    m = int(input("Брой доставчици m: "))
    n = int(input("Брой суровини n: "))
    A = np.array(read_list(f"Наличности S_i ({m} стойности)", float))
    D = np.array(read_list(f"Заявки D_j ({n} стойности)", float))

    # Четем C_raw като текст, позволявайки 'M' за голямо число
    raw = read_matrix(m, n, str)
    M = symbols('M')
    M_VALUE = 10_000
    C = np.empty((m,n), dtype=object)
    for i in range(m):
        for j in range(n):
            val = raw[i][j]
            if val.upper() == 'M':
                C[i,j] = Rational(M_VALUE)
            else:
                C[i,j] = Rational(val)

    # Четем забрани Z
    Z = []
    print("Въвеждане на забранени двойки (i,j). Въведете 'готово' за край.")
    while True:
        s = input("  Забрана (i,j): ")
        if s.strip().lower() == 'готово':
            break
        i,j = map(int, s.split(','))
        Z.append((i-1, j-1))  # превръщаме в 0-базиран

    # Метод на минималния елемент
    supply = A.copy()
    demand = D.copy()
    X = np.zeros((m,n), dtype=float)
    while True:
        valid = [(i,j) for i in range(m) for j in range(n)
                 if supply[i]>0 and demand[j]>0 and (i,j) not in Z]
        if not valid:
            break
        i,j = min(valid, key=lambda t: float(C[t].subs(M, M_VALUE)))
        q = min(supply[i], demand[j])
        X[i,j] = q
        supply[i] -= q
        demand[j] -= q

    print("\nОптимално разпределение x_{ij}:")
    for i in range(m):
        row = ["%g" % X[i,j] for j in range(n)]
        print(f"Доставчик {i+1}: [{', '.join(row)}]")

if __name__ == '__main__':
    main()
