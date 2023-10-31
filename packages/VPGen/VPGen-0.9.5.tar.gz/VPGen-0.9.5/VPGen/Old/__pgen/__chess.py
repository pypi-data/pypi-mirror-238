from time import perf_counter
from random import random
from math import sqrt

from . import __area


def __generate(size, periodicity, indent, porosityNumber, radius, minimumDistance, settings):
    indent_length = 0 if periodicity[0] else indent[0]
    indent_width = 0 if periodicity[1] else indent[1]

    indent_x = (indent_length + settings[2]) if not periodicity[0] else 0
    indent_y = (indent_width + settings[3]) if not periodicity[1] else 0

    if settings[0] % 2 == 0:
        periodicity[0] = False
    if settings[1] % 2 == 0:
        periodicity[1] = False

    maximum_radius = min(sqrt(settings[2] ** 2 + settings[3] ** 2) - radius[0] - minimumDistance, radius[1])
    minimum_radius = maximum_radius if maximum_radius < radius[0] else radius[0]

    disks = set()
    disks2d = [[None for _ in range(settings[1])] for _ in range(settings[0])]

    total_area = size[0] * size[1]
    current_area = float(total_area)
    current_porosity = 0

    start = perf_counter()
    try:
        for i in range(settings[0]):
            if i == 0 and periodicity[0]:
                periodicity_x = settings[0] - 1
            else:
                periodicity_x = None
            for j in range(settings[1]):
                if j == 0 and periodicity[1]:
                    periodicity_y = settings[1] - 1
                else:
                    periodicity_y = None
                if (i + j) % 2 == 0:
                    if disks2d[i][j] is None:
                        x, y = indent_x + settings[2] * i, indent_y + settings[3] * j
                        max_r = maximum_radius
                        for n, m in ((1, 1), (-1, -1), (-1, 1), (1, -1)):
                            r, d = i + n, j + m
                            if 0 <= r < settings[0] and 0 <= d < settings[1]:
                                if disks2d[r][d] is not None:
                                    max_rt = sqrt((disks2d[r][d][0] - x) ** 2 + (disks2d[r][d][1] - y) ** 2) - disks2d[r][d][2] - minimumDistance
                                    max_r = min(max_rt, max_r)
                        r = minimum_radius + random() * (max_r - minimum_radius)
                        disks2d[i][j] = (x, y, r)
                        if periodicity_x is not None:
                            if disks2d[periodicity_x][j] is None:
                                disks2d[periodicity_x][j] = (indent_x + settings[2] * periodicity_x,
                                                             y,
                                                             disks2d[i][j][2])
                        if periodicity_y is not None:
                            if disks2d[i][periodicity_y] is None:
                                disks2d[i][periodicity_y] = (x,
                                                             indent_y + settings[3] * periodicity_y,
                                                             disks2d[i][j][2])
                    disks.add((disks2d[i][j][0], disks2d[i][j][1], 0, disks2d[i][j][2]))

                    current_area -= __area.__getArea(size[0], size[1], *disks2d[i][j], indent_length, indent_width)
                    current_porosity = 100 * (current_area / total_area)

                if len(disks) >= porosityNumber:
                    raise KeyboardInterrupt
    except KeyboardInterrupt:
        ...

    end = perf_counter()

    return disks, current_porosity, end - start
