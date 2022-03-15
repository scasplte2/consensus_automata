import math
from fractions import Fraction
import time
import numpy as np
import matplotlib.pyplot as plt


def byte_length(i):
    return (i.bit_length() + 7) // 8


def rational_approximation(arg: Fraction, max_denominator: int, max_iter: int):
    q = arg.numerator // arg.denominator
    r = arg.numerator % arg.denominator
    if arg < 0:
        sign = -1
    else:
        sign = 1
    x = Fraction(r, arg.denominator).__abs__()
    a = 0
    b = 1
    c = 1
    d = 1
    j = 0
    not_done = True
    output = Fraction(0)
    while b <= max_denominator and d <= max_denominator and j <= max_iter and not_done:
        med = Fraction(a + c, b + d)
        if x == med:
            if b + d <= max_denominator:
                output = Fraction(sign * (a + c), b + d)
            elif d > b:
                output = Fraction(sign * c, d)
            else:
                output = Fraction(sign * a, b)
            not_done = False
        elif x > med:
            a = a + c
            b = b + d
        else:
            c = a + c
            d = b + d
        j = j + 1
    if not_done:
        if b > max_denominator:
            output = Fraction(sign * c, d)
        else:
            output = Fraction(sign * a, b)
    return Fraction(q * output.denominator + output.numerator, output.denominator)


def modified_lentz_method(max_iter: int, prec: int, a, b):
    big_factor = pow(10, prec + 10)
    tiny_factor = Fraction(1, big_factor)
    truncation_error = Fraction(1, pow(10, prec + 1))
    fj = b(0)
    if fj == Fraction(0):
        fj = tiny_factor
    cj = fj
    dj = Fraction(0)
    error = True
    iii = 1
    while iii < max_iter + 1 and error:
        dj = b(iii) + a(iii) * dj
        if dj == Fraction(0):
            dj = tiny_factor
        cj = b(iii) + a(iii) / cj
        if cj == Fraction(0):
            cj = tiny_factor
        dj = Fraction(dj.denominator, dj.numerator)
        deltaj = cj * dj
        fj = fj * deltaj
        if iii > 1:
            error = (deltaj - Fraction(1)).__abs__() > truncation_error
        iii = iii + 1
    return fj


def exp(x: Fraction, max_iter: int, prec: int):
    def a(j: int):
        if j == 0:
            return Fraction(0)
        elif j == 1:
            return Fraction(1)
        elif j == 2:
            return Fraction(-1) * x
        else:
            return Fraction(-j + 2) * x

    def b(j: int):
        if j == 0:
            return Fraction(0)
        elif j == 1:
            return Fraction(1)
        else:
            return Fraction(j - 1) + x

    if x == Fraction(0):
        return Fraction(1)
    else:
        return modified_lentz_method(max_iter, prec, a, b)


def log1p(x: Fraction, max_iter: int, prec: int):
    def a(j: int):
        if j == 0:
            return Fraction(0)
        elif j == 1:
            return x
        else:
            return Fraction(j - 1) * Fraction(j - 1) * x

    def b(j: int):
        if j == 0:
            return Fraction(0)
        elif j == 1:
            return Fraction(1)
        else:
            return Fraction(j) - Fraction(j - 1) * x

    if x == Fraction(0):
        return Fraction(1)
    else:
        return modified_lentz_method(max_iter, prec, a, b)


def print_frac(frac: Fraction):
    print(float(frac.numerator) / float(frac.denominator))


start_time = time.time()
res = exp(Fraction(1), 10000, 38)
print("--- %s seconds ---" % (time.time() - start_time))

print(math.e)
print_frac(res)
print(res.__str__())
print(rational_approximation(res, 100000, 10000).__str__())
print((log1p(Fraction(-1, 2), 10000, 38)).__str__())


def regression(prec: int, stake: int, net_stake: int, coefficient: Fraction):
    alpha = Fraction(stake, net_stake)
    return Fraction(1) - exp(coefficient * alpha, 10000, prec)



label_bool = True
plot_reg1 = False
plot_reg2 = False
plot_reg3 = True

if plot_reg1:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    precision = 38
    k_max = 500
    i_max = 10
    for i in range(1, i_max):
        data = np.empty((0, 4))
        for stake in range(5, 51, 5):
            start_time = time.time()
            thr_len = []
            coefficient = Fraction(math.log1p(float(-i)/float(i_max)))
            # coefficient = log1p(Fraction(-i, i_max), 10000, 15)
            for k in range(k_max):
                thr = regression(precision, stake * pow(10, precision) // 100 - k_max + k, pow(10, precision), coefficient)
                thr_len.append(byte_length(thr.numerator) + byte_length(thr.denominator))
            exec_time = (time.time() - start_time)
            print(str(stake * pow(10, precision) // 100 / pow(10, precision)) + " " + str(sum(thr_len) / len(thr_len)) + " " + Fraction(i, i_max).__str__() + " " + "%s" % exec_time)
            new_data = np.array([float(stake * pow(10, precision) // 100 / pow(10, precision)), float(i) / i_max, sum(thr_len) / len(thr_len), float(exec_time)])
            data = np.vstack((data, new_data))
        if label_bool:
            label_bool = False
            ax.scatter(data[:, 0], float(i) / i_max, data[:, 3], color="blue", label="Execution time of " + str(k_max) + " exp operations in seconds")
            ax.scatter(data[:, 0], float(i) / i_max, data[:, 2] / 1000, color="red", label="Avg. byte length of threshold divided by 1000")
        else:
            ax.scatter(data[:, 0], float(i) / i_max, data[:, 3], color="blue")
            ax.scatter(data[:, 0], float(i) / i_max, data[:, 2] / 1000, color="red")
    plt.legend()
    ax.set_xlabel("Relative Stake")
    ax.set_ylabel("f")
    plt.title("Exp operation experiment, precision = "+str(precision))
    plt.show()


if plot_reg2:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    f = Fraction(99, 100)
    k_max = 500
    i_max = 40
    for i in range(10, i_max):
        data = np.empty((0, 4))
        for stake in range(5, 51, 5):
            start_time = time.time()
            thr_len = []
            coefficient = Fraction(math.log1p(f.numerator/f.denominator))
            # coefficient = log1p(Fraction(-i, i_max), 10000, 15)
            for k in range(k_max):
                thr = regression(i, stake * pow(10, i) // 100 - k_max + k, pow(10, i), coefficient)
                thr_len.append(byte_length(thr.numerator) + byte_length(thr.denominator))
            exec_time = (time.time() - start_time)
            print(str(stake * pow(10, i) // 100 / pow(10, i)) + " " + str(sum(thr_len) / len(thr_len)) + " " + str(i) + " " + "%s" % exec_time)
            new_data = np.array([float(stake * pow(10, i) // 100 / pow(10, i)), f.numerator/f.denominator, sum(thr_len) / len(thr_len), float(exec_time)])
            data = np.vstack((data, new_data))
        if label_bool:
            label_bool = False
            ax.scatter(data[:, 0], i, data[:, 3], color="blue", label="Execution time of " + str(k_max) + " exp operations in seconds")
            ax.scatter(data[:, 0], i, data[:, 2] / 1000, color="red", label="Avg. byte length of threshold divided by 1000")
        else:
            ax.scatter(data[:, 0], i, data[:, 3], color="blue")
            ax.scatter(data[:, 0], i, data[:, 2] / 1000, color="red")
    plt.legend()
    ax.set_xlabel("Relative Stake")
    ax.set_ylabel("Precision")
    plt.title("Exp operation experiment, f = "+f.__str__())
    plt.show()


if plot_reg3:
    fig = plt.figure()
    ax = fig.add_subplot()
    f = Fraction(99, 100)
    k_max = 500
    i_max = 38
    for i in range(i_max, i_max+1):
        data = np.empty((0, 4))
        for stake in range(5, 51, 5):
            start_time = time.time()
            thr_len = []
            coefficient = Fraction(math.log1p(f.numerator/f.denominator))
            # coefficient = log1p(Fraction(-i, i_max), 10000, 15)
            for k in range(k_max):
                thr = regression(i, stake * pow(10, i) // 100 - k_max + k, pow(10, i), coefficient)
                thr_len.append(byte_length(thr.numerator) + byte_length(thr.denominator))
            exec_time = (time.time() - start_time)
            print(str(stake * pow(10, i) // 100 / pow(10, i)) + " " + str(sum(thr_len) / len(thr_len)) + " " + str(i) + " " + "%s" % exec_time)
            new_data = np.array([float(stake * pow(10, i) // 100 / pow(10, i)), f.numerator/f.denominator, sum(thr_len) / len(thr_len), float(exec_time)])
            data = np.vstack((data, new_data))
        if label_bool:
            label_bool = False
            ax.scatter(data[:, 0], data[:, 3], color="blue", label="Execution time of " + str(k_max) + " exp operations in seconds")
            ax.scatter(data[:, 0], data[:, 2] / 1000, color="red", label="Avg. byte length of threshold divided by 1000")
        else:
            ax.scatter(data[:, 0], data[:, 3], color="blue")
            ax.scatter(data[:, 0], data[:, 2] / 1000, color="red")
    plt.legend()
    ax.set_xlabel("Relative Stake")
    plt.title("Exp operation experiment, f = "+f.__str__())
    plt.show()
