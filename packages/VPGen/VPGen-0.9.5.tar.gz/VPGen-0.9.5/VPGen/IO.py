from json import load, dump
from ctypes import CDLL, POINTER, CFUNCTYPE, c_void_p, c_longdouble, c_int

from .Classes import Domain, Obstacle


def loadLibrary(filename: str) -> CDLL:
    '''
    Loads shared library with random algorithm written in c++.

    filename: str - path to library

    return - ctypes.CDLL
    '''
    lib = CDLL(filename)
    lib.generate.argtypes = (Domain, CALLBACK_TYPE)
    lib.generate.restype = POINTER(c_longdouble * 2)
    return lib


def loadGeometry(filename: str) -> dict:
    '''
    Loads dict with domain settings from file.

    filename: str - path to .json file with domain settings

    return - Domain
    '''
    with open(filename) as file:
        data = load(file)
    return data


def saveDomain(filename: str, domain: Domain) -> None:
    if not filename.endswith('.json'):
        filename += '.json'
    
    with open(filename, 'w') as file:
        dump(domain.toJSON())


def saveObstacles(filename: str, obstacles: tuple[Obstacle]) -> None:
    if not filename.endswith('.json'):
        filename += '.json'
    
    with open(filename, 'w') as file:
        dump([[obstacle.center.x, obstacle.center.y, obstacle.center.z, obstacle.radius] for obstacle in obstacles], file, indent=4)


CALLBACK_TYPE = CFUNCTYPE(c_void_p, c_int, c_longdouble)
