from ctypes import (
    Structure,
    c_longdouble,
    c_bool,
    c_short,
    c_uint,
    c_int,
    c_bool,
)


class Point(Structure):
    _fields_ = [
        ('x', c_longdouble),
        ('y', c_longdouble),
        ('z', c_longdouble),
    ]

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
    
    def __call__(self) -> tuple:
        return self.x, self.y, self.z
    
    def __getitem__(self, key) -> int:
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise KeyError('Uncorrect key')


class Periodicity(Structure):
    _fields_ = [
        ('x', c_bool),
        ('y', c_bool),
        ('z', c_bool),
    ]
    
    def __call__(self) -> tuple:
        return self.x, self.y, self.z
    
    def __getitem__(self, key) -> int:
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise KeyError('Uncorrect key')


class Radius(Structure):
    _fields_ = [
        ('min', c_longdouble),
        ('max', c_longdouble),
    ]
    
    def __call__(self) -> tuple:
        return self.min, self.max


class Counter(Structure):
    _fields_ = [
        ('type', c_short),
        ('number', c_uint),
        ('porosity', c_longdouble),
    ]
    
    def __call__(self) -> tuple:
        return self.type, self.number, self.porosity


class Domain(Structure):
    _fields_ = [
        ('dimension', c_int),
        ('origin', Point),
        ('size', Point),
        ('indent', Point),
        ('periodicity', Periodicity),
        ('radius', Radius),
        ('counter', Counter),
        ('minimum_distance', c_longdouble),
        ('iterations', c_uint),
        ('exact_count', c_bool),
        ('order', c_short),
        ('heterogenous', c_bool),
    ]

    def toJSON(self):
        return {
            'dimension': self.dimension,
            'origin': self.origin(),
            'size': self.size(),
            'indent': self.indent(),
            'periodicity': self.periodicity(),
            'radius': self.radius(),
            'type': self.counter.type,
            'number': self.counter.number,
            'porosity': self.counter.porosity,
            'minimum_distance': self.minimum_distance,
            'iterations': self.iterations,
            'exact_count': self.exact_count,
            'order': self.order,
            'heterogenous': self.heterogenous,
        }

    @classmethod
    def fromJSON(cls, json):
        return cls(
            c_int(json['dimension']),
            Point(*json['origin']),
            Point(*json['size']),
            Point(*json['indent']),
            Periodicity(*json['periodicity']),
            Radius(*json['radius']),
            Counter(
                c_short(json['type']),
                c_uint(json['number']),
                c_longdouble(json['porosity'])
            ),
            c_longdouble(json['minimum_distance']),
            c_uint(json['iterations']),
            c_bool(json['exact_count']),
            c_short(json['order']),
            c_bool(json['heterogenous']),
        )

class Obstacle(Structure):
    _fields_ = [
        ('center', Point),
        ('radius', c_longdouble),
    ]

    def __repr__(self) -> str:
        return f'{self.center} ({self.radius})'
    
    def __call__(self) -> tuple:
        return self.center, self.radius
