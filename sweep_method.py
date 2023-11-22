def check_matrix(matrix):
    size = len(matrix)
    for i in matrix:
        if size != len(i):
            raise ValueError


def check_vector(size, vector):
    if len(vector) != size:
        raise ValueError


def read_matrix(way):
    with open(way, "r") as file:
        *matrix, vector = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
        return matrix, vector


def tridiagonales_chack(matrix):
    n = len(matrix)
    for i in range(1, n - 1):
        if abs(matrix[i][i]) <= (abs(matrix[i][i - 1]) + abs(matrix[i][i + 1])) or matrix[i][i] == 0 or matrix[i][
            i - 1] == 0 or matrix[i][i + 1] == 0:
            raise ValueError

    if abs(matrix[0][0]) < abs(matrix[0][1]) or abs(matrix[n - 1][n - 1]) < abs(matrix[n - 1][n - 2]):
        raise ValueError

    for i in range(0, n):
        if matrix[i][i] == 0:
            raise ValueError
    count = 0
    for i in range(1, n - 1):
        for j in range(n):
            if matrix[i][j] != 0:
                count += 1
            if count > 3:
                raise ValueError
        count = 0
    count = 0
    for j in range(n):
        if matrix[0][j] != 0:
            count += 1
        if count > 2:
            raise ValueError
    count = 0
    for j in range(n):
        if matrix[n - 1][j] != 0:
            count += 1
        if count > 2:
            raise ValueError


def straight_stroke(matrix, vector):
    u = [0 for a in range(len(matrix))]
    v = [0 for b in range(len(matrix))]
    v[0] = matrix[0][1] / (-matrix[0][0])
    u[0] = vector[0] / matrix[0][0]
    for i in range(1, len(matrix) - 1):
        v[i] = matrix[i][i + 1] / (-matrix[i][i] - matrix[i][i - 1] * v[i - 1])
        u[i] = (matrix[i][i - 1] * u[i - 1] - vector[i]) / (-matrix[i][i] - matrix[i][i - 1] * v[i - 1])
    n = len(matrix)
    v[n - 1] = 0
    u[n - 1] = (matrix[n - 1][n - 2] * u[n - 2] - vector[n - 1]) / (
            -matrix[n - 1][n - 1] - matrix[n - 1][n - 2] * v[n - 2])
    return u, v


def solution(u, v, matrix):
    n = len(matrix)
    x = [0 for a in range(n)]
    x[n - 1] = u[n - 1]
    for i in range(n - 1, 0, -1):
        x[i - 1] = v[i - 1] * x[i] + u[i - 1]
    return x


if __name__ == '__main__':
    s = "input.txt"
    try:
        a, b = read_matrix(s)
        check_matrix(a)
        check_vector(len(a), b)
        tridiagonales_chack(a)
        u, v = straight_stroke(a, b)
        X = solution(u, v, a)
        print("Получили ответ:")
        print("\n".join("X{0} =\t{1:10.8f}".format(i + 1, x) for i, x in enumerate(X)))
    except ValueError:
        print("Uncorrect matrix or vector")
        exit()
