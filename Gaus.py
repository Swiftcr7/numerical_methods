def MatryxPrint(A, B, selected):
    for row in range(len(B)):
        print("(", end='')
        for col in range(len(A[row])):
            print("\t{1:10.8f}{0}".format(" " if (selected is None
                                                  or selected != (row, col)) else "*", A[row][col]), end='')
        print("\t) * (\tX{0}) = (\t{1:10.2f})".format(row + 1, B[row]))


def print_matr(mas):
    for i in mas:
        for i2 in i:
            print(i2, end=' ')
        print()


def read_matrix(way):
    with open(way, "r") as file:
        *matrix, vector = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
        return matrix, vector


def sum_row(row1, row2, coeficient, matrix, vector, reverse_matrix):
    # for i in range(row1, len(matrix)):
    #     matrix[row2][i] = matrix[row2][i] + matrix[row1][i] * coeficient
    #     print(matrix[row2][i])
    #     vector[row2] = vector[i] + vector[row1] * coeficient
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
        else:
            raise ValueError
        for j in range(i + 1, len(matrix)):
            coeficient = -1 * matrix[j][i] / matrix[i][i]
            sum_row(j, i, coeficient, matrix, vector, reverse_matrix)
    return matrix, count, vector, reverse_matrix


def determinator(matrix, count):
    determinator = 1
    for i in range(len(matrix)):
        determinator *= matrix[i][i]
    determinator *= (-1) ** count
    return determinator


def check_matrix(matrix):
    size = len(matrix)
    for i in matrix:
        if size != len(i):
            raise ValueError


def check_vector(size, vector):
    if len(vector) != size:
        raise ValueError


def reverse_course(A, B):
    X = [0 for b in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = (B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))) / A[i][i]
    return X


def inverse_matrix(matrix, reverse_matrix):
    result = []
    for i in range(len(reverse_matrix)):
        array = []
        for j in range(len(reverse_matrix)):
            array.append(reverse_matrix[j][i])
        result.append(reverse_course(matrix, array))
    return result


if __name__ == '__main__':
    s = "input.txt"
    try:
        a, b = read_matrix(s)
        check_matrix(a)
        check_vector(len(a), b)
        triangle_matrix, count, vector, reverse_matrix = create_triangle_matrix(a, b)
        det = determinator(triangle_matrix, count)
        if det == 0:
            raise ValueError
        print("Детерминант:")
        print(det)
        X = reverse_course(triangle_matrix, vector)
        print("Получили ответ:")
        print("\n".join("X{0} =\t{1:10.8f}".format(i + 1, x) for i, x in enumerate(X)))
        Y = inverse_matrix(triangle_matrix, reverse_matrix)
        print("Получили обратную матрицу:")
        trans_Y = [[Y[j][i] for j in range(len(Y))] for i in range(len(Y[0]))]
        print_matr(trans_Y)
    except ValueError:
        print("Uncorrect matrix or vector")
        exit()
