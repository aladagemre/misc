"""
Implements regression in Biostatistics book.
"""
import math
import matplotlib.pyplot as plt
from sympy.statistics.distributions import Sample

def get_line(x_values, y_values):
    """
    Returns the regression line that fits to the data points.
    @return a, b

    """

    # Make sure x and y values match.
    n = len(x_values)
    assert n == len(y_values)

    # Calculate some params in advance.
    sum_y = sum(y_values)
    sum_x = sum(x_values)
    sum_xy = sum(x*y for x,y in zip(x_values, y_values))
    sum_x2 = sum([x**2 for x in x_values ])

    # Calculate a (intercept)
    a_num = (sum_y * sum_x2 - sum_x * sum_xy)
    a_den = n * sum_x2 - sum_x ** 2

    a = a_num / float(a_den)

    # Calculate b (slope)
    b_num = n * sum_xy - sum_x * sum_y
    b_den = n * sum_x2 - sum_x ** 2

    b = b_num / float(b_den)

    return a, b


def estimate_line(a, b, x_values):
    """
    Estimates the line points for the line a + bx for x_values.
    """
    return [a + b*x for x in x_values]

def calculate_correlation(x_values, y_values):
    """
    Calculates correlation coefficient.
    """
    mean_x = sum(x_values)/float(len(x_values))
    mean_y = sum(y_values)/float(len(y_values))

    numerator = 0.0

    xsum = 0.0
    ysum = 0.0

    for i in range(len(x_values)):
        numerator += (x_values[i] - mean_x) * (y_values[i] - mean_y)

    for i in range(len(x_values)):
        xsum += (x_values[i] - mean_x)**2
    for i in range(len(y_values)):
        ysum += (y_values[i] - mean_y)**2

    denum = math.sqrt(xsum * ysum)

    return numerator / denum

def compare_slope(x1, y1, x2, y2):
    a1, b1 = get_line(x1, y1)
    a2, b2 = get_line(x2, y2)

    estimate1 = estimate_line(a1, b1, x1)
    estimate2 = estimate_line(a2, b2, x2)

    # For Line 1
    n1 = len(x1)
    total = 0.0
    for i in range(len(x1)):
        total += (y1[i] - estimate1[i])**2
    s_yx1 = math.sqrt( total / (n1-2) )

    s_x1 = Sample(x1).stddev()
    s_a1 = s_yx1 * math.sqrt( 1.0/n1 + Sample(x1).mean()**2 / ((n1-1)*s_x1**2) )
    s_b1 = (1.0 / math.sqrt(n1-1)) * (s_yx1 / s_x1)




    # For Line 2

    n2 = len(x2)
    total = 0.0
    for i in range(len(x2)):
        total += (y2[i] - estimate2[i])**2
    s_yx2 = math.sqrt( total / (n2-2) )

    s_x2 = Sample(x2).stddev()
    s_a2 = s_yx2 * math.sqrt( 1.0/n2 + Sample(x2).mean()**2 / ((n2-1)*s_x2**2) )
    s_b2 = (1.0 / math.sqrt(n2-1)) * (s_yx2 / s_x2)

    if n1 == n2:
        s_a1_a2 = math.sqrt(s_a1**2 + s_a2**2)
        s_b1_b2 = math.sqrt(s_b1**2 + s_b2**2)
    else:
        # TODO
        pass

    # Calculate t
    t_b = (b1 - b2) / s_b1_b2
    t_a = (a1 - a2) / s_a1_a2

    return t_a, t_b


def base_function(x, y, name):
    a, b = get_line(x, y)
    estimated = estimate_line(a, b, x)
    r = calculate_correlation(x, y)
    formula = "y = %.3f + %.3f x" % (a, b)
    coeff = "r = %.3f" % r

    plt.grid()
    plt.plot(x, estimated)
    plt.scatter(x, y)
    plt.title(name)
    plt.xlabel(formula + " ; " + coeff)
    plt.savefig(name + ".png")


def main():
    """Test case"""
    x = [31, 32, 33, 34, 35, 35, 40, 41, 42, 46]
    y = [7.8, 8.3, 7.6, 9.1, 9.6, 9.8, 11.8, 12.1, 14.7, 13.0]
    base_function(x, y, "main")

def q81a():
    """
    Question 8.1-a
    """
    x = [30, 30, 40, 40]
    y = [37, 47, 50, 60]
    base_function(x, y, "Q-8.1-a")

def q81b():
    """
    Question 8.1-b
    """
    x = [30, 30, 40, 40, 20, 20, 50, 50]
    y = [37, 47, 50, 60, 25, 35, 62, 72]
    base_function(x, y, "Q-8.1-b")

def q81c():
    """
    Question 8.1-c
    """
    x = [30, 30, 40, 40, 20, 20, 50, 50, 10, 10, 60, 60]
    y = [37, 47, 50, 60, 25, 35, 62, 72, 13, 23, 74, 84]
    base_function(x, y, "Q-8.1-c")

def q82a():
    """
    Question 8.2-a
    """
    x = [15, 15, 20, 20, 25, 25, 30, 30, 60]
    y = [19, 29, 25, 35, 31, 41, 37, 47, 40]
    base_function(x, y, "Q-8.2-a")

def q82b():
    """
    Question 8.2-b
    """
    x = [20, 20, 30, 30, 40, 40, 40, 40, 50, 50, 60, 60]
    y = [21, 31, 18, 28, 15, 25, 75, 85, 65, 75, 55, 65]
    base_function(x, y, "Q-8.2-b")


def q86a():
    """
    Question 8.6-a
    """
    x = [49, 47, 50, 76, 77, 99, 98, 103, 118, 105, 100, 98]
    y = [-30, -22, -29, -22, -15, -10, -11, -10, -1, -4, -13, -14]
    base_function(x, y, "Q-8.6-37kcal")

def q86b():
    """
    Question 8.6-b
    """
    x = [32, 32, 32, 51, 53, 51, 52, 74, 72, 74, 98, 97]
    y = [-32, -20, -17, -10, -20, -18, -21, 4, -16, -14, 6, -7]
    base_function(x, y, "Q-8.6-33kcal")


def q86():

    x1 = [49, 47, 50, 76, 77, 99, 98, 103, 118, 105, 100, 98]
    y1 = [-30, -22, -29, -22, -15, -10, -11, -10, -1, -4, -13, -14]

    a, b = get_line(x1, y1)
    estimated = estimate_line(a, b, x1)

    plt.grid()
    plt.plot(x1, estimated)
    plt.scatter(x1, y1)

    x2 = [32, 32, 32, 51, 53, 51, 52, 74, 72, 74, 98, 97]
    y2 = [-32, -20, -17, -10, -20, -18, -21, 4, -16, -14, 6, -7]

    a, b = get_line(x2, y2)
    estimated = estimate_line(a, b, x2)

    plt.plot(x2, estimated)
    plt.scatter(x2, y2)
    plt.title('37 and 33 kcal together')

    plt.savefig("q86.png")

    print compare_slope(x1, y1, x2, y2)



if __name__ == "__main__":
    q81a()
    plt.clf()
    q81b()
    plt.clf()
    q81c()
    plt.clf()
    q82a()
    plt.clf()
    q82b()
    plt.clf()
    q86a()
    plt.clf()
    q86b()
    plt.clf()
    q86()





