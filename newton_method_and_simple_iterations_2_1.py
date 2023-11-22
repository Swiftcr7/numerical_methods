import numpy as np


def function(x):
    return x ** 3 - 2 * x ** 2 - 10 * x + 15


def expressed_function(Lambda, x):
    return x - Lambda * (x ** 3 - 2 * x ** 2 - 10 * x + 15)


def derivative(func, x):
    h = 0.0000000001
    return (func(x + h) - func(x)) / h


def deretivate_Lambda(Lambda, func, x):
    h = 0.0000000001
    return (func(Lambda, x + h) - func(Lambda, x)) / h


def newton_method(function, x_0, epsilon):
    if function(x_0) * derivative(function, x_0) < 0:
        raise Exception
    x_prev = function(x_0)
    count = 0
    x = 0
    while True:
        if count >= 1:
            if abs(x - x_prev) < epsilon:
                break
            else:
                prom = x
                count += 1
                x = x_prev - function(x_prev) / derivative(function, x_prev)
                x_prev = prom
        else:
            x = x_0 - function(x_0) / derivative(function, x_0)
            count += 1
    return x, count


def simple_iteration(function, a, b, epsilon):
    max = 0
    for i in np.linspace(a, b, 10000):
        if derivative(function, i) > max:
            max = derivative(function, i)
    Lambda = 1 / max
    q = 0
    for j in np.linspace(a, b, 10000):
        if expressed_function(Lambda, j) > b or expressed_function(Lambda, j) < a:
            raise Exception
        if q < deretivate_Lambda(Lambda, expressed_function, j) < 1:
            q = deretivate_Lambda(Lambda, expressed_function, j)
    x_prev = (b + a) / 2
    count = 0
    x = 0
    while True:
        if count >= 1:
            if q / (1 - q) * abs(x - x_prev) <= epsilon:
                break
            else:
                count += 1

                x_prev = x
                x = expressed_function(Lambda, x)
        else:
            x = expressed_function(Lambda, x_prev)
            count += 1
    return x, count


if __name__ == '__main__':
    result1, count = newton_method(function, 5, 1e-6)
    print("Решение методом Ньютона: ", result1)
    print("Количество итераций методом Ньютона: ", count)
    result2, count = simple_iteration(function, 3, 4, 1e-6)
    print("Решение методом простых итераций: ", result1)
    print("Количество итераций методом простых итераций:", count)
    print("Разница между результатом метода Ньютона и результатом метода простых итераций: ", abs(result1 - result2))
