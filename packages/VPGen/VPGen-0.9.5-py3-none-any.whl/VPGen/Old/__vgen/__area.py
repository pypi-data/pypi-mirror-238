from math import sqrt, asin, isnan, pi, nan


def __round_neg(x):
    if x < 0:
        return -round(x)
    else:
        return x


def __circle_integral(x0, r, x):
    return (x - x0) * sqrt(__round_neg(r ** 2 - (x - x0) ** 2)) + r ** 2 * asin(round((x - x0) / r, 3))


def __get_circles_area(x0, r, a, b):
    return __circle_integral(x0, r, b) - __circle_integral(x0, r, a)


def __get_area(size_length, size_height, x0, y0, r, indent_length, indent_height):
    x0 -= indent_length
    y0 -= indent_height
    h = y0 if y0 - r < 0 else ((size_height - y0) if y0 + r > size_height else nan)
    local_s = __get_circles_area(x0, r, max(x0 - r, 0), min(x0 + r, size_length))
    if not isnan(h):
        d = sqrt(__round_neg(r ** 2 - h ** 2))
        x1, x2 = max(x0 - d, 0), min(x0 + d, size_length + 2 * size_length)
        local_s -= (__get_circles_area(x0, r, x1, x2) - 4 * h * d) / 2
    return local_s


def __get_volume(size_length, size_height, size_width, x0, y0, z0, r, indent_length, indent_height, indent_width):
    n = 1000
    z0 -= indent_width
    v = 0
    if z0 < 0:
        a = r + z0
        d = a / n
        for i in range(n + 1):
            h = sqrt(__round_neg(r ** 2 - (i * d) ** 2))
            v += d * __get_area(size_length, size_height, x0, y0, h, indent_length, indent_height)
    elif z0 > size_width:
        a = r - z0 + size_width
        d = a / n
        for i in range(n + 1):
            h = sqrt(__round_neg(r ** 2 - (i * d) ** 2))
            v += d * __get_area(size_length, size_height, x0, y0, h, indent_length, indent_height)
    else:
        a = (r if z0 - r > 0 else z0)
        d = a / n
        for i in range(1, n + 1):
            h = sqrt(__round_neg(r ** 2 - (i * d) ** 2))
            v += d * pi * h ** 2  # get_area(size_length, size_height, x0, y0, h, indent_length, indent_height)
        a = (r if z0 + r < size_width else r - size_width + z0)
        d = a / n
        for i in range(1, n + 1):
            h = sqrt(__round_neg(r ** 2 - (i * d) ** 2))
            v += d * pi * h ** 2  # get_area(size_length, size_height, x0, y0, h, indent_length, indent_height)
    return v
