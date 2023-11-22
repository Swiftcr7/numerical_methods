import math
import numpy as np
import matplotlib.pyplot as plt


def grafix(function1, function2):
    x = np.linspace(-10, 10, 100)
    plt.plot(x, function1(x))
    plt.plot(x, function2(x))
    plt.show()


def function(x):
    return math.sin(x) + x


def difference(y):
    result = []
    count = len(y)
    for i in range(count - 1):
        result.append(y[i + 1] - y[i])
    return result


def newton_polynomial(function, x_values):
    count = len(x_values)
    h = x_values[1] - x_values[0]
    delta_y = []
    for i in x_values:
        delta_y.append(function(i))
    # for i in range(count - 1):
    #     if h != x_values[i] - x_values[i+1]:
    #         raise Exception("No good data")

    result = [delta_y[0]]
    for i in range(1, count):
        delta_y = difference(delta_y)
        result.append(delta_y[0] / (math.factorial(i) * h ** i))

    def calculation_newton_polynomial(x):
        value = result[0]
        for k in range(1, count):
            prom = result[k]
            for j in range(k):
                prom *= (x - x_values[j])
            value += prom
        if function(x) != 0:
            return value, abs(function(x) - value), abs(function(x) - value) / function(x)
        else:
            return value, abs(function(x) - value), abs(function(x) - value)

    return result, calculation_newton_polynomial


def lagrange_polynomial(function, x_values):
    size = len(x_values)
    result = []
    for i in range(size):
        result_value = function(x_values[i])
        for j in range(size):
            if i != j:
                result_value /= (x_values[i] - x_values[j])
        result.append(result_value)

    def calculation_lagrange_polynomial(x):
        value = 0
        for k in range(size):
            prom = result[k]
            for l in range(size):
                if k != l:
                    prom *= (x - x_values[l])
            value += prom
        return value, abs(function(x) - value), (abs(function(x) - value)) / function(x)

    return result, calculation_lagrange_polynomial


if __name__ == '__main__':
    result1, calculation = lagrange_polynomial(function, [0, (math.pi / 8), (math.pi / 3), (3 * math.pi / 8)])
    print("Коэффициенты поллинома Лагранжа")
    print("\n".join("a{0} = {1}".format(i, x) for i, x in enumerate(result1)))
    y, absolute_error, relative_error = calculation(3 * math.pi / 16)
    print("Посчитанный результат с помощью поллинома Лагранжа: ", y)
    print("Абсолютнвя погрешность: ", absolute_error)
    print("Относительная погрешность: ", relative_error)
    polinom1 = lambda x: result1[0] * (x - (math.pi / 8)) * (x - (math.pi / 3)) * (x - (3 * math.pi / 8)) + result1[
        1] * (x - 0) * (x - (math.pi / 3)) * (x - (3 * math.pi / 8)) + result1[2] * (x - (math.pi / 8)) * (x - 0) * (
                                 x - (3 * math.pi / 8)) + result1[3] * (x - (math.pi / 8)) * (x - (math.pi / 3)) * (
                                 x - 0)

    result2, calculation = newton_polynomial(function, [i / 8 * math.pi for i in range(4)])
    print("Коэффициенты поллинома Ньютона")
    print("\n".join("a{0} = {1}".format(i, x) for i, x in enumerate(result2)))
    y, absolute_error, relative_error = calculation(3 * math.pi / 16)
    print("Посчитанный результат с помощью поллинома Ньютона: ", y)
    print("Абсолютнвя погрешность: ", absolute_error)
    print("Относительная погрешность: ", relative_error)

    polinom2 = lambda x: result2[0] + result2[1] * (x - 0) + result2[2] * (x - 0) * (x - math.pi / 8) + result2[3] * (
            x - math.pi / 8) * (x - math.pi * 2 / 8)
    grafix(polinom1, polinom2)
