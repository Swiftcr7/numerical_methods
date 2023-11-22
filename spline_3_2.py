def read_matrix(way):
    with open(way, "r") as file:
        *matrix, vector = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
        return matrix, vector


def make_difference(matrix):
    return [matrix[i + 1][0] - matrix[i][0] for i in range(len(matrix) - 1)]


def make_system_c(matrix, matrix_h):
    result_matrix = [[0] * (len(matrix) - 2) for i in range(len(matrix) - 2)]
    result_vector = [0] * (len(matrix) - 2)
    result_matrix[0][0] = (2 * (matrix_h[0] + matrix_h[1]))
    result_matrix[0][1] = matrix_h[1]
    result_vector[0] = 3 * ((matrix[2][1] - matrix[1][1]) / matrix_h[1] - (matrix[1][1] - matrix[0][1]) / matrix_h[0])
    for j in range(1, len(result_matrix) - 1):
        result_matrix[j][j - 1] = matrix_h[j]
        result_matrix[j][j] = (matrix_h[j] + matrix_h[j + 1]) * 2
        result_matrix[j][j + 1] = matrix_h[j + 1]
        result_vector[j] = 3 * ((matrix[j + 2][1] - matrix[j + 1][1]) / matrix_h[j + 1] - (
                (matrix[j + 1][1] - matrix[j][1]) / matrix_h[j]))
    result_matrix[len(result_matrix) - 1][len(result_matrix) - 2] = matrix_h[len(result_matrix) - 1]
    result_matrix[len(result_matrix) - 1][len(result_matrix) - 1] = 2 * (
            matrix_h[len(result_matrix) - 1] + matrix_h[len(result_matrix)])
    result_vector[len(result_matrix) - 1] = 3 * (
            (matrix[len(result_matrix) + 1][1] - matrix[len(result_matrix)][1]) / matrix_h[len(result_matrix)] - (
            matrix[len(result_matrix)][1] - matrix[(len(result_matrix) - 1)][1]) / matrix_h[
                (len(result_matrix) - 1)])
    return result_matrix, result_vector


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


def spline(matrix, x0):
    A = []
    B = []
    D = []
    matrix_h = make_difference(matrix)
    matrix2, vector = make_system_c(matrix, matrix_h)
    triangle_matrix, count, vector2, reverse_matrix = create_triangle_matrix(matrix2, vector)
    C = reverse_course(triangle_matrix, vector2)
    C = [0] + C
    index = 0
    for i in range(1, len(matrix)):
        if matrix[i - 1][0] < x0 < matrix[i][0]:
            index = i
            break
    if index == 0:
        raise ValueError

    for i in range(1, len(matrix)):
        A.append(matrix[i - 1][1])

    for i in range(1, len(matrix) - 1):
        B.append((matrix[i][1] - matrix[i - 1][1]) / matrix_h[i - 1] - (matrix_h[i - 1] * (C[i] + 2 * C[i - 1]) / 3))
        D.append((C[i] - C[i - 1]) / (3 * matrix_h[i - 1]))
    B.append((matrix[len(matrix) - 1][1] - matrix[len(matrix) - 2][1]) / matrix_h[len(matrix) - 2] - (
            2 * matrix_h[len(matrix) - 2] * C[len(matrix) - 2]) / 3)
    D.append(-1 * C[len(matrix) - 2] / (3 * matrix_h[len(matrix) - 2]))
    result = A[index - 1] + B[index - 1] * (x0 - matrix[index - 1][0]) + C[index - 1] * (
            (x0 - matrix[index - 1][0]) ** 2) + D[index - 1] * ((x0 - matrix[index - 1][0]) ** 3)
    return result


if __name__ == '__main__':
    way = "input_spline.txt"
    matrix, point = read_matrix(way)
    res = spline(matrix, point[0])
    print(f"Результат вычислений в точке {point[0]} =", res)
