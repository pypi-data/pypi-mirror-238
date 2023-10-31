from random import random
from time import perf_counter
from math import pi

from . import __area


def __check_for_intersection(x, y, z, r, spheres, minimal_distance):
    for _x, _y, _z, _r in spheres:
        if (_x - x) ** 2 + (_y - y) ** 2 + (_z - z) ** 2 <= (_r + r + minimal_distance) ** 2:
            return True
    return False


def __generate(size, periodicity, indent, porosityNumberButton, porosityNumber, radius, minimumDistance):
    print(size, periodicity, indent)
    indent_length = 0 if periodicity[0] else indent[0]
    indent_width = 0 if periodicity[1] else indent[1]
    indent_height = 0 if periodicity[2] else indent[2]

    spheres = set()

    total_volume = size[0] * size[1] * size[2]
    current_volume = float(total_volume)
    spheres_area = 0
    current_porosity = 100

    volume_calc = False
    running = True
    start = perf_counter()

    while running:
        if len(spheres) >= porosityNumber and porosityNumberButton == 1 or current_porosity <= porosityNumber and porosityNumberButton:
            running = False
        r = radius[0] + random() * (radius[1] - radius[0])

        if periodicity[0]:
            x = random.random() * size[0]
        else:
            x = indent_length + r + random() * (size[0] - 2 * r)

        if periodicity[1]:
            y = random() * size[1]
        else:
            y = indent_width + r + random() * (size[1] - 2 * r)

        if periodicity[2]:
            z = random() * size[2]
        else:
            z = indent_height + r + random() * (size[2] - 2 * r)

        if not __check_for_intersection(x, y, z, r, spheres, minimumDistance):
            need_x = 2 if (x - r < 0 or x + r > size[0] + 2 * indent_length) and periodicity[0] else 0
            need_y = 2 if (y - r < 0 or y + r > size[1] + 2 * indent_width) and periodicity[1] else 0
            need_z = 2 if (z - r < 0 or z + r > size[2] + 2 * indent_height) and periodicity[2] else 0
            if len(spheres) + need_x + need_y + need_z + (2 if need_x and need_y and need_z else 0) >= porosityNumber and porosityNumberButton == 1:
                continue
            copies = []
            if need_x:
                if x - r < 0:
                    _x = x + size[0]
                elif x + r > size[0] + indent_length:
                    _x = x - size[0]
                copies.append((_x, y, z))
            if need_y:
                if y - r < 0:
                    _y = y + size[1]
                elif y + r > size[1] + indent_width:
                    _y = y - size[1]
                copies.append((x, _y, z))
                if need_x:
                    copies.append((_x, _y, z))
            if need_z:
                if z - r < 0:
                    _z = z + size[2]
                elif z + r > size[2] + indent_height:
                    _z = z - size[2]
                copies.append((x, y, _z))
                if need_x:
                    copies.append((_x, y, _z))
                if need_y:
                    copies.append((x, _y, _z))
                if need_x and need_y:
                    copies.append((_x, _y, _z))
            for _x, _y, _z in copies:
                if __check_for_intersection(_x, _y, _z, r, spheres, minimumDistance):
                    break
            else:
                for _x, _y, _z in copies:
                    spheres.add((_x, _y, _z, r))
                    if volume_calc:
                        current_volume -= __area.__get_volume(size[0], size[1], size[2], _x, _y, _z, r, indent_length, indent_width, indent_height)
                spheres.add((x, y, z, r))
                if volume_calc:
                    current_volume -= __area.__get_volume(size[0], size[1], size[2], x, y, z, r, indent_length, indent_width, indent_height)
                else:
                    current_volume -= 4 / 3 * pi * r ** 3
                    spheres_area += 4 * pi * r ** 2
                current_porosity = 100 * (current_volume / total_volume)

    end = perf_counter()

    return spheres, current_porosity, end - start
