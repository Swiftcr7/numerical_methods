import numpy as np
import matplotlib.pyplot as plt


def read_matrix(way):
    with open(way, "r") as file:
        matrix = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
        return matrix


def normal_system(matrix):
    result_matrix_1 = [[0] * 2 for i in range(2)]
    result_vector_1 = [0] * 2
    result_matrix_2 = [[0] * 3 for i in range(3)]
    result_vector_2 = [0] * 3
    result_matrix_1[0][0] = len(matrix)
    sum_x = 0
    sum_x_pow = 0
    sum_y = 0
    sum_y_x = 0
    sum_x_pow_3 = 0
    sum_x_pow_4 = 0
    sum_y_x_pow_2 = 0
    for i in range(len(matrix)):
        sum_x += matrix[i][0]
        sum_y += matrix[i][1]
        sum_x_pow += matrix[i][0] ** 2
        sum_x_pow_3 += matrix[i][0] ** 3
        sum_x_pow_4 += matrix[i][0] ** 4
        sum_y_x_pow_2 += (matrix[i][0] ** 2) * matrix[i][1]
        sum_y_x += matrix[i][0] * matrix[i][1]

    result_matrix_1[0][1], result_matrix_1[1][0], result_matrix_1[1][1], result_vector_1[0], result_vector_1[
        1] = sum_x, sum_x, sum_x_pow, sum_y, sum_y_x

    result_matrix_2[0][0], result_matrix_2[0][1], result_matrix_2[0][2], result_matrix_2[1][0], result_matrix_2[1][1], \
    result_matrix_2[1][2], result_matrix_2[2][0], result_matrix_2[2][1], result_matrix_2[2][2] = len(
        matrix), sum_x, sum_x_pow, sum_x, sum_x_pow, sum_x_pow_3, sum_x_pow, sum_x_pow_3, sum_x_pow_4

    result_vector_2[0], result_vector_2[1], result_vector_2[2] = sum_y, sum_y_x, sum_y_x_pow_2

    return result_matrix_1, result_vector_1, result_matrix_2, result_vector_2


def sum_row(row1, row2, coeficient, matrix, vector, reverse_matrix):
    matrix[row1] = [(a + k * coeficient) for a, k in zip(matrix[row1], matrix[row2])]
    vector[row1] += vector[row2] * coeficient
    reverse_matrix[row1] = [(a + k * coeficient) for a, k in zip(reverse_matrix[row1], reverse_matrix[row2])]


def swap_row(matrix, vector, reverse_matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    vector[row1], vector[row2] = vector[row2], vector[row1]
    reverse_matrix[row1], reverse_matrix[row2] = reverse_matrix[row2], reverse_matrix[row1]


def leader_element(column, matrix):
    max_element = 0
    index = 0
    for i in range(column, len(matrix)):
        if max_element < abs(matrix[i][column]):
            max_element = abs(matrix[i][column])
            index = i
    return index


def create_single_matrix(size):
    reverse_matrix = [0] * size

    for i in range(size):
        reverse_matrix[i] = [0] * size
    for i in range(size):
        reverse_matrix[i][i] = 1
    return reverse_matrix


def create_triangle_matrix(matrix, vector):
    count = 0
    reverse_matrix = create_single_matrix(len(matrix))

    for i in range(len(matrix)):
        index = leader_element(i, matrix)
        if index != 0:
            swap_row(matrix, vector, reverse_matrix, i, index)
            count += 1

        for j in range(i + 1, len(matrix)):
            coeficient = -1 * matrix[j][i] / matrix[i][i]
            sum_row(j, i, coeficient, matrix, vector, reverse_matrix)
    return matrix, count, vector, reverse_matrix


def reverse_course(A, B):
    X = [0 for b in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = (B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))) / A[i][i]
    return X


def polynomial_power(matrix):
    matrix1, vector1, matrix2, vector2 = normal_system(matrix)
    triangle_matrix, count, vector3, reverse_matrix = create_triangle_matrix(matrix1, vector1)
    polynomial_power_1 = reverse_course(triangle_matrix, vector3)
    triangle_matrix, count, vector3, reverse_matrix = create_triangle_matrix(matrix2, vector2)
    polynomial_power_2 = reverse_course(triangle_matrix, vector3)

    def polynomial_1_power(x):
        return polynomial_power_1[0] + polynomial_power_1[1] * x

    def polynomial_2_power(x):
        return polynomial_power_2[0] + polynomial_power_2[1] * x + polynomial_power_2[2] * x ** 2

    return polynomial_power_1, polynomial_1_power, polynomial_power_2, polynomial_2_power


def quadratic_errors(matrix, function):
    error = 0
    for i in range(len(matrix)):
        error += (function(matrix[i][0]) - matrix[i][1]) ** 2
    return error


def grafix(function1, function2):
    x = np.linspace(-10, 10, 100)
    plt.plot(x, function1(x))
    plt.plot(x, function2(x))
    plt.show()


if __name__ == '__main__':
    way = "input_MNK.txt"
    matrix = read_matrix(way)
    polynom1, function1, polynom2, function2 = polynomial_power(matrix)
    print(f"Приближающий многочлен первой степени: f = {polynom1[0]} + x * {polynom1[1]}")
    print("Сумма квадратов ошибок приближающего многочлена первой степени:", quadratic_errors(matrix, function1))
    print(f"Приближающий многочлен второй степени: f = {polynom2[0]} + x * {polynom2[1]} - x^2 * {polynom2[2]}")
    print("Сумма квадратов ошибок приближающего многочлена второй степени:", quadratic_errors(matrix, function2))
    grafix(function1, function2)
