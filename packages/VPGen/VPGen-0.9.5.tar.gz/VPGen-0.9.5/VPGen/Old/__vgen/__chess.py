from random import random
from time import perf_counter
from math import sqrt

from . import __area


def __generate(size, periodicity, indent, porosityNumber, radius, minimumDistance, settings):
    indent_length = 0 if periodicity[0] else indent[0]
    indent_width = 0 if periodicity[1] else indent[1]
    indent_height = 0 if periodicity[2] else indent[2]

    indent_x = (indent_length + settings[3]) if not periodicity[0] else 0
    indent_y = (indent_width + settings[4]) if not periodicity[1] else 0
    indent_z = (indent_height + settings[5]) if not periodicity[2] else 0

    maximum_radius = min(min(settings[2] ** 2, settings[3] ** 2) - radius[0] - minimumDistance, radius[1])
    minimum_radius = maximum_radius if maximum_radius < radius[0] else radius[0]

    if settings[0] % 2 == 0:
        periodicity[0] = False
    if settings[1] % 2 == 0:
        periodicity[1] = False
    if settings[2] % 2 == 0:
        periodicity[2] = False

    spheres = set()
    spheres3d = [[[None for _ in range(settings[2])] for _ in range(settings[1])] for _ in range(settings[0])]

    total_volume = size[0] * size[1] * size[2]
    current_volume = float(total_volume)
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
                for k in range(settings[2]):
                    if k == 0 and periodicity[2]:
                        periodicity_z = settings[2] - 1
                    else:
                        periodicity_z = None
                    if (i + j + k) % 2 == 0:
                        if spheres3d[i][j][k] is None:
                            x, y, z = indent_x + settings[3] * i, indent_y + settings[4] * j, indent_z + settings[5] * k
                            max_r = maximum_radius
                            for n, m, t in ((1, 1, -1), (-1, -1, -1), (-1, 1, -1), (1, -1, -1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1), (1, -1, 1)):
                                r, d, c = i + n, j + m, k + t
                                if 0 <= r < settings[0] and 0 <= d < settings[1] and 0 <= c < settings[2]:
                                    if spheres3d[r][d][c] is not None:
                                        max_rt = sqrt((spheres3d[r][d][c][0] - x) ** 2 + (spheres3d[r][d][c][1] - y) ** 2 + (spheres3d[r][d][c][2]) ** 2) - spheres3d[r][d][c][3] - minimumDistance
                                        max_r = min(max_rt, max_r)
                            r = minimum_radius + random() * (max_r - minimum_radius)
                            spheres3d[i][j][k] = (x, y, z, r)
                            if periodicity_x is not None:
                                if spheres3d[periodicity_x][j][k] is None:
                                    spheres3d[periodicity_x][j][k] = (indent_x + settings[3] * periodicity_x,
                                                                 y,
                                                                 z,
                                                                 spheres3d[i][j][k][3])
                            if periodicity_y is not None:
                                if spheres3d[i][periodicity_y][k] is None:
                                    spheres3d[i][periodicity_y][k] = (x,
                                                                 indent_y + settings[4] * periodicity_y,
                                                                 z,
                                                                 spheres3d[i][j][k][3])
                            if periodicity_z is not None:
                                if spheres3d[i][j][periodicity_z] is None:
                                    spheres3d[i][j][periodicity_z] = (x,
                                                                 y,
                                                                 indent_z + settings[5] * periodicity_z,
                                                                 spheres3d[i][j][k][3])
                        spheres.add(tuple(spheres3d[i][j][k]))

                        current_volume -= __area.__get_volume(size[0], size[1], size[2], *spheres3d[i][j][k], indent_length, indent_height, indent_width)
                        current_porosity = 100 * (current_volume / total_volume)

                        if len(spheres) >= porosityNumber:
                            raise KeyboardInterrupt
    except KeyboardInterrupt:
        ...

    end = perf_counter()

    return spheres, current_porosity, end - start
