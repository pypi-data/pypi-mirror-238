from time import perf_counter
from random import random

from . import __area


def __checkForIntersection(x, y, r, disks, minimumDistance):
    for _x, _y, _, _r in disks:
        if (_x - x) ** 2 + (_y - y) ** 2 <= (_r + r + minimumDistance) ** 2:
            return True
    return False


def __generate(size, periodicity, indent, porosityNumberButton, porosityNumber, radius, minimumDistance):
    indent_length = 0 if periodicity[0] else indent[0]
    indent_width = 0 if periodicity[1] else indent[1]

    disks = set()

    total_area = size[0] * size[1]
    current_area = float(total_area)
    current_porosity = 100

    running = True
    start = perf_counter()

    while running:
        if len(disks) >= porosityNumber and porosityNumberButton == 1 or current_porosity <= porosityNumber and porosityNumberButton == 0:
            running = False

        x = indent_length + random() * size[0]
        y = indent_width + random() * size[1]
        r = radius[0] + random() * (radius[1] - radius[0])
    
        if not __checkForIntersection(x, y, r, disks, minimumDistance):
            need_x = 2 if (x - r < 0 or x + r > size[0] + indent_length) and periodicity[0] else 0
            need_y = 2 if (y - r < 0 or y + r > size[1] + indent_width) and periodicity[1] else 0
    
            if len(disks) + need_x + need_y >= porosityNumber and porosityNumberButton == 1:
                continue
    
            copies = []
            if need_x:
                if x - r < 0:
                    _x = x + size[0]
                elif x + r > size[0] + indent_length:
                    _x = x - size[0]
                copies.append((_x, y))
            if need_y:
                if y - r < 0:
                    _y = y + size[1]
                elif y + r > size[1] + indent_width:
                    _y = y - size[1]
                copies.append((x, _y))
            if need_x and need_y:
                copies.append((_x, _y))
    
            for _x, _y in copies:
                if __checkForIntersection(_x, _y, r, disks, minimumDistance):
                    break
            else:
                copies.append((x, y))
                for _x, _y in copies:
                    disks.add((_x, _y, 0, r))
                    current_area -= __area.__getArea(size[0], size[1], _x, _y, r, indent_length, indent_width)
                # disks.add((x, y, 0, r))
                # current_area -= __area.__getArea(size[0], size[1], x, y, r, indent_length, indent_width)
                current_porosity = 100 * (current_area / total_area)

    running = False
    end = perf_counter()

    return disks, current_porosity, end - start
