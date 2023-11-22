
from copy import deepcopy
from math import sin, cos, atan, pi


def read_matrix(way):
    with open(way, "r") as file:
        *matrix, vector = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
    return matrix, vector


def transport_matrix(matrix):
    trans = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return trans


def composition_matrix(matrix_1, matrix_2):
    n, m = len(matrix_1), len(matrix_1[0])
    if n != len(matrix_2[0]) or m != len(matrix_2):
        raise Exception
    result = [[0] * n for i in range(len(matrix_2[0]))]
    for i in range(len(matrix_1)):
        for j in range(len(matrix_2[0])):
            for k in range(len(matrix_2)):
                result[i][j] += matrix_1[i][k] * matrix_2[k][j]
    return result


def sum_composition_vector(vector_1, vector_2):
    return sum(list(map(lambda x, y: x * y, vector_1, vector_2)))


def multiply_matrix_vector(matrix_1: [[float]], matrix_2: [float]) -> [float]:
    res = []
    for i in range(len(matrix_1)):
        res.append(round(sum(list(map(lambda x, y: x * y, matrix_1[i], matrix_2))), 6))
    return res


def max_non_diagonal(matrix):
    maximum = [matrix[0][1], 0, 1]
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if abs(maximum[0]) < abs(matrix[i][j]):
                maximum = [matrix[i][j], i, j]
    return maximum


def calculate_the_angle(matrix, line, row):
    if matrix[line][line] == matrix[row][row]:
        return pi / 4
    return 0.5 * (atan((2 * matrix[line][row]) / (matrix[line][line] - matrix[row][row])))


def build_matrix(angle, size, line, row):
    res = [[1. if i == j else 0. for j in range(size)] for i in range(size)]
    res[line][row], res[row][line], res[line][line], res[row][row] = round(-sin(angle), 6), round(sin(angle), 6), round(
        cos(angle), 6), round(cos(angle), 6)
    return res


def find_size_non_diagonal_element(matrix):
    result = 0
    for i in range(len(matrix) - 1):
        for j in range(i + 1, len(matrix)):
            result += matrix[i][j] * matrix[i][j]
    result **= 0.5
    return result


def normalization_vector(vector, norm):
    return [i / norm for i in vector]


def rotation(matrix, epsilon):
    A = deepcopy(matrix)
    result = [[1 if i == j else 0 for i in range(len(matrix))] for j in range(len(matrix))]
    count = 0
    while abs(find_size_non_diagonal_element(A)) > epsilon:
        count += 1
        maximum_and_position = max_non_diagonal(A)
        U = build_matrix(calculate_the_angle(A, *maximum_and_position[1:]), len(A), *maximum_and_position[1:])
        result = composition_matrix(result, U)
        A = composition_matrix(composition_matrix(transport_matrix(U), A), U)
    if sum_composition_vector(result[0], result[1]) > epsilon or sum_composition_vector(result[0], result[
        2]) > epsilon or sum_composition_vector(result[1], result[2]) > epsilon:
        raise Exception("Something went wrong for this matrix!")
    return result, [A[i][i] for i in range(len(A))], count


def power_method(matrix, epsilon):
    Lambda, Lambda_prev = 0.0, 0.0
    A = deepcopy(matrix)
    y = [1] * len(matrix)
    iteration = 10000
    flag = 0
    count = 0
    for i in range(iteration):
        if flag == 2:
            if abs(Lambda - Lambda_prev) < epsilon:
                break
            Z = multiply_matrix_vector(A, y)
            Lambda_prev = Lambda
            Lambda = Z[0] / y[0]
            y = normalization_vector(Z, max(Z))
            count += 1
        else:
            count += 1
            flag += 1
            Z = multiply_matrix_vector(A, y)
            Lambda_prev = Lambda
            Lambda = Z[0] / y[0]
            y = normalization_vector(Z, max(Z))
    return Lambda, y, count


if __name__ == '__main__':
    s = "input4.txt"
    matrix, epsilon = read_matrix(s)
    print(*rotation(matrix, epsilon[0]))
    Lambda, result, count = power_method(matrix, epsilon[0])
    print("Собственный вектор ", result, "Спектральный радиус ", Lambda, "Количество итераций", count, sep='\n')

