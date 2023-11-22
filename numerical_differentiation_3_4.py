def read_matrix(way):
    with open(way, "r") as file:
        *matrix, vector = [[float(j) for j in i.split()] for i in file.read().split('\n') if len(i) != 0]
        return matrix, vector


def numerical_differentiation(matrix, x):
    index = 0
    for i in range(1, len(matrix) - 2):
        if matrix[i][0] <= x <= matrix[i + 1][0]:
            index = i
            break
    left_handed_differentiation = (matrix[index + 1][1] - matrix[index ][1]) / (matrix[index + 1][0] - matrix[index][0])
    right_handed_differentiation = (matrix[index + 2][1] - matrix[index + 1][1]) / (
                matrix[index + 2][0] - matrix[index + 1][0])
    differentiation_1 = left_handed_differentiation + ((right_handed_differentiation - left_handed_differentiation) / (
                matrix[index + 2][0] - matrix[index][0])) * (2 * x - matrix[index][0] - matrix[index + 1][0])
    differentiation_2 = 2 * (right_handed_differentiation - left_handed_differentiation) / (
                matrix[index + 2][0] - matrix[index][0])
    return differentiation_1, differentiation_2


if __name__ == '__main__':
    way = "input_numerical_differentiation.txt"
    matrix, vector = read_matrix(way)
    differentiation1, differentiation2 = numerical_differentiation(matrix, vector[0])
    print("Производная первого порядка", differentiation1)
    print("Производная второго порядка", differentiation2)
