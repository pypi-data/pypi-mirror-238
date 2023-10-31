from math import sqrt

from . import __chess, __inline, __random


def __convert(geometry_data):
    geometry_data['size'] = float(geometry_data['size'][0]), float(geometry_data['size'][1])
    geometry_data['porosityNumber'] = float(geometry_data['porosityNumber'])
    geometry_data['radius'] = float(geometry_data['radius'][0]), float(geometry_data['radius'][1])
    geometry_data['minimumDistance'] = float(geometry_data['minimumDistance'])
    geometry_data['periodicity'] = geometry_data['periodicity'][:2]
    geometry_data['indent'] = float(geometry_data['indent'][0]), float(geometry_data['indent'][1])


def __calculate_lines_indents(size_length, size_height, obstacles, periodicity_length, periodicity_height):
    lines_x = round(sqrt(obstacles * size_length / size_height))
    lines_y = round(sqrt(obstacles * size_height / size_length))
    while (lines_x - 1) * lines_y >= obstacles:
        lines_x -= 1
    while lines_x * lines_y < obstacles:
        if lines_x * (lines_y + 1) - obstacles > lines_y:
            lines_x += 1
        else:
            lines_y += 1
    bottom = lines_x + (1 if not periodicity_length else -1)
    if bottom != 0:
        lines_indent_x = size_length / bottom
    else:
        lines_indent_x = size_length
    bottom = lines_y + (1 if not periodicity_height else -1)
    if bottom != 0:
        lines_indent_y = size_height / bottom
    else:
        lines_indent_y = size_height
    return lines_x, lines_y, lines_indent_x, lines_indent_y


def __generate(geometry_data):

    __convert(geometry_data)

    if geometry_data['order'] == 0:
        generator = __random

    elif geometry_data['order'] == 1:
        generator = __chess
        geometry_data['settings'] = __calculate_lines_indents(*geometry_data['size'], 2 * geometry_data['porosityNumber'] - 1, *geometry_data['periodicity'])

        del geometry_data['porosityNumberButton']

    elif geometry_data['order'] == 2:
        generator = __inline
        geometry_data['settings'] = __calculate_lines_indents(*geometry_data['size'], geometry_data['porosityNumber'], *geometry_data['periodicity'])

        del geometry_data['porosityNumberButton']

    else:
        raise TypeError

    del geometry_data['order']

    disks, porosity, time = generator.__generate(**geometry_data)

    return disks, porosity, time
