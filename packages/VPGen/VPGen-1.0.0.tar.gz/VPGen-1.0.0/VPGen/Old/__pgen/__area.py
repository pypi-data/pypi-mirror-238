from math import sqrt, asin, isnan, nan


def __circleIntegral(x0, r, x):
    return (x - x0) * sqrt(round(r ** 2 - (x - x0) ** 2, 3)) + r ** 2 * asin(round((x - x0) / r, 3))


def __getCirclesArea(x0, r, a, b):
    return __circleIntegral(x0, r, b) - __circleIntegral(x0, r, a)


def __getArea(size_length, size_height, x0, y0, r, indent_length, indent_height):
    x0 -= indent_length
    y0 -= indent_height
    h = y0 if y0 - r < 0 else ((size_height - y0) if y0 + r > size_height else nan)
    local_s = __getCirclesArea(x0, r, max(x0 - r, 0), min(x0 + r, size_length))
    if not isnan(h):
        d = sqrt(r ** 2 - h ** 2)
        x1, x2 = max(x0 - d, 0), min(x0 + d, size_length + 2 * size_length)
        local_s -= (__getCirclesArea(x0, r, x1, x2) - 4 * h * d) / 2
    return local_s
