from ctypes import POINTER
from time import perf_counter
from os.path import abspath, dirname
from platform import system

from .IO import loadGeometry, loadLibrary, CALLBACK_TYPE
from .Classes import Domain, Obstacle, Point
from .Old import generateGeometry


def createDomain(data: dict) -> Domain:
    '''
    Creates 'Domain' from 'dict'.

    data: dict - dict with domain settings

    return - Domain
    '''
    # return Domain(
    #         c_int(data['dimension']),
    #         Point(*data['origin']),
    #         Point(*data['size']),
    #         Point(*data['indent']),
    #         Periodicity(*data['periodicity']),
    #         Radius(
    #             c_longdouble(min(data['radius'])),
    #             c_longdouble(max(data['radius']))
    #         ),
    #         Counter(
    #             c_short(data['type']),
    #             c_uint(data['number']),
    #             c_longdouble(data['porosity'])
    #         ),
    #         c_longdouble(data['minimum_distance']),
    #         c_uint(data['iterations']),
    #         c_bool(data['exact_count']),
    #         c_short(data['order']),
    #         c_bool(data['heterogenous']),
    #     )
    return Domain.fromJSON(data)


def generateFromFile(filename: str) -> tuple:
    '''
    Generates from file with domain settings and return tuple of obstacles, number of obstacles, porosity, generating time.

    filename: str - path to .json file with domain settings

    return - tuple
    '''
    domain = createDomain(loadGeometry(filename))
    return generate(domain)


def generate(domain: Domain, callback_function=lambda *_: None) -> tuple:
    '''
    Generates from domain and return tuple of obstacles, number of obstacles, porosity, generating time.

    domain: Domain - geometry
    callback_function: callable - function that called every iteration, must be (int, float) -> None

    return - tuple
    '''
    try:
        lib = loadLibrary(LIB_PATH)
        LIBRARY_LOADED = True
    except Exception as error:
        print(f'[Error] {error}')
        LIBRARY_LOADED = False

    if LIBRARY_LOADED and domain.order == 0:
        callback_function = CALLBACK_TYPE(callback_function)

        start = perf_counter()
        obstacles_number, porosity = lib.generate(domain, callback_function).contents
        end = perf_counter()

        obstacles_number = int(obstacles_number)
        lib.getObstacles.restype = POINTER(Obstacle * obstacles_number)
        obstacles = lib.getObstacles().contents
        return obstacles, obstacles_number, porosity, end - start
    else:
        geometry_data = {
            'size': list(domain.size()),
            'heterogenous': domain.heterogenous,
            'dimension': domain.dimension,
            'periodicity': list(domain.periodicity()),
            'indent': list(domain.indent()),
            'radius': list(domain.radius()),
            'porosityNumberButton': 1-domain.counter.type,
            'porosityNumber': domain.counter.porosity if domain.counter.type == 1 and domain.order == 0 else domain.counter.number,
            'minimumDistance': domain.minimum_distance,
            'order': domain.order,
        }
        obstacles, porosity, time, heterogenous, size, dimension = generateGeometry(geometry_data)
        obstacles = list(obstacles)
        for i, obstacle in enumerate(obstacles):
            obstacles[i] = Obstacle(Point(*obstacle[:3]), obstacle[3])
    return obstacles, len(obstacles), porosity, time


LIBRARY_DIRECTORY = dirname(abspath(__file__))
LIB_PATH = LIBRARY_DIRECTORY
SYSTEM = system()
if SYSTEM == 'Linux':
    LIB_PATH += '/VPGen.so'
elif SYSTEM == 'Windows':
    LIB_PATH += '/VPGen.dll'
else:
    raise OSError('Only Linux/Windows')
