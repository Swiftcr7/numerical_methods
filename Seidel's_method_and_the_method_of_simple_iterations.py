from copy import deepcopy


def read_matrix(way):
    with open(way, "r") as file:
        *matrix, vector = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
        return matrix, vector


def prepare_matrix_vector(matrix, vector):
    copy_matrix = deepcopy(matrix)
    copy_vector = vector[:]
    size = len(matrix)
    for i in range(size):
        d = copy_matrix[i][i]
        for j in range(size):
            copy_matrix[i][j] /= (-1 * d)
        copy_vector[i] /= d
        copy_matrix[i][i] = 0
    return copy_matrix, copy_vector


def matrix_norm(matrix):
    return max([sum(abs(i) for i in j) for j in matrix])


def subtraction_matrix(matrix1, matrix2):
    return list(map(lambda x, y: x - y, matrix1, matrix2))


def sum_matrix(matrix1, matrix2):
    return list(map(lambda x, y: x + y, matrix1, matrix2))


def composition_matrix(matrix, vector):
    return [sum(map(lambda x, y: x * y, matrix[i], vector)) for i in range(len(matrix))]


def method_of_simple_iterations(matrix, vector, epsilon):
    prepare_matrix, prepare_vector = prepare_matrix_vector(matrix, vector)
    print(prepare_matrix)
    print(prepare_vector)
    alpha = matrix_norm(prepare_matrix)
    x_1 = prepare_vector[:]
    size = len(prepare_matrix)
    x_2 = [0 for i in range(size)]
    iteration = 10000
    count = 0
    for i in range(iteration):
        if max(abs_matrix(subtraction_matrix(x_1, x_2))) < epsilon:
            break
        else:
            count += 1
            x_2 = x_1[:]
            x_1 = sum_matrix(composition_matrix(prepare_matrix, x_1), prepare_vector)
    return x_1, count


def abs_matrix(matrix):
    return [abs(i) for i in matrix]


def method_Seidel(matrix, vector, epsilon):
    prepare_matrix, prepare_vector = prepare_matrix_vector(matrix, vector)
    alpha = matrix_norm(prepare_matrix)
    x_1 = prepare_vector[:]
    size = len(prepare_matrix)
    size_matrix = len(prepare_matrix)
    print(alpha)
    x_2 = [0 for i in range(size)]
    count = 0
    while True:
        if max(abs_matrix(subtraction_matrix(x_1, x_2))) <= epsilon:
            break
        else:
            count += 1
            x_2 = x_1[:]
            for i in range(size_matrix):
                res = 0
                for j in range(size_matrix):
                    res += x_1[j] * prepare_matrix[i][j]
                res += prepare_vector[i]
                x_1[i] = res
    return x_1, count


if __name__ == '__main__':
    s = "input3.txt"
    matrix, vector = read_matrix(s)

    res1, j = method_of_simple_iterations(matrix, vector, 1e-8)
    res2, i = method_Seidel(matrix, vector, 1e-8)
    print("Получили ответ методом простых итераций:")
    print("количество", j)
    print("\n".join("X{0} =\t{1:10.8f}".format(i + 1, x) for i, x in enumerate(res1)))
    print("количество", i)
    print("Получили ответ методом Зейделя:")
    print("\n".join("X{0} =\t{1:10.8f}".format(i + 1, x) for i, x in enumerate(res2)))
    print(subtraction_matrix(composition_matrix(matrix, res1), vector))
