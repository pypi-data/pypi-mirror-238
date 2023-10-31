try:
    import gmsh
    USE_GMSH = True
except ModuleNotFoundError:
    USE_GMSH = False

from . import __core, __pgen, __vgen
# import __core, __pgen, __vgen


def generateGeometry(geometry_data):
    dimension = geometry_data['dimension']
    heterogenous = geometry_data['heterogenous']

    del geometry_data['dimension']
    del geometry_data['heterogenous']

    if dimension == 2:
        obstacles, porosity, time = __pgen.__generate(geometry_data)
        size = (
            geometry_data['size'][0] + (0 if geometry_data['periodicity'][0] else (2 * geometry_data['indent'][0])),
            geometry_data['size'][1] + (0 if geometry_data['periodicity'][1] else (2 * geometry_data['indent'][1]))
        )

    elif dimension == 3:
        obstacles, porosity, time = __vgen.__generate(geometry_data)
        size = (
            geometry_data['size'][0] + (0 if geometry_data['periodicity'][0] else (2 * geometry_data['indent'][0])),
            geometry_data['size'][1] + (0 if geometry_data['periodicity'][1] else (2 * geometry_data['indent'][1])),
            geometry_data['size'][2] + (0 if geometry_data['periodicity'][2] else (2 * geometry_data['indent'][2]))
        )

    else:
        raise ValueError('[generateGeometry] Wrong dimension')

    return obstacles, porosity, time, heterogenous, size, dimension


def generateGeometrySkeleton(obstacles, heterogenous, size, dimension, fltk=False):
    if not USE_GMSH:
        raise ImportError('GMSH is not found!')

    __core.__initialize_gmsh()

    if dimension == 2:
        domainType, obstacleType = __core.__get_2d()
    elif dimension == 3:
        domainType, obstacleType = __core.__get_3d()
    else:
        raise ValueError('[generateGeometrySkeleton] Wrong dimension')

    booleanOperations = __core.__heterogenousBooleanOperations if heterogenous else __core.__nonHeterogenousBooleanOperations

    domainDimTag = ((dimension, domainType(0, 0, 0, *size)),)
    obstacleDimTags = tuple((dimension, obstacleType(*obstacle)) for obstacle in obstacles)

    domainDimTag, obstacleDimTags = booleanOperations(domainDimTag, obstacleDimTags)

    __core.__sync()

    #   if dim == 0 --> 3 algorithm2d
    # elif dim == 1 --> 2 algorithm2d
    # else 'what?'

    __core.__set_options(None, 3-dimension, None)
    __core.__generate_mesh(dim=2, refine=dimension)

    if fltk:
        __core.__run_fltk()

    nodeTags, nodeCoords = __core.__get_nodes()

    domains = []
    if dimension == 2:
        elementTags, elementNodeTags = __core.__get_elements(2, domainDimTag[0][1], 2)
        domains.append((elementTags, elementNodeTags, (0, 0, 1)))
        for _, tag in obstacleDimTags:
            elementTags, elementNodeTags = __core.__get_elements(2, tag, 2)
            domains.append((elementTags, elementNodeTags, (1, 0, 0)))

    elif dimension == 3:
        for _, tag in gmsh.model.getEntities(dim=2):
            if gmsh.model.getType(2, tag) == 'Plane':
                elementTags, elementNodeTags = __core.__get_elements(2, tag, 2)
                domains.append((elementTags, elementNodeTags, (0, 0, 1)))
            color = (1, 0, 0) if heterogenous else (0, 0, 1)
            if gmsh.model.getType(2, tag) == 'Sphere':
                elementTags, elementNodeTags = __core.__get_elements(2, tag, 2)
                domains.append((elementTags, elementNodeTags, color))
        # for _, tag in obstacleDimTags:
        #     elementTags, elementNodeTags = __core.__get_elements(2, tag, 2)
        #     domains.append((elementTags, elementNodeTags, (1, 0, 0)))

    else:
        ...

    __core.__finalize_gmsh()

    return (nodeTags, nodeCoords), domains


def generateMesh(obstacles, heterogenous, size, dimension, folder, meshSize=1, algorithm2d=2, algorithm3d=10, fltk=False):
    if not USE_GMSH:
        raise ImportError('GMSH is not found!')

    __core.__initialize_gmsh()

    if dimension == 2:
        domainType, obstacleType = __core.__get_2d()
    elif dimension == 3:
        domainType, obstacleType = __core.__get_3d()
    else:
        raise ValueError('[generateMesh] Wrong dimension')

    booleanOperations = __core.__heterogenousBooleanOperations if heterogenous else __core.__nonHeterogenousBooleanOperations

    domainDimTag = ((dimension, domainType(0, 0, 0, *size)),)
    obstacleDimTags = tuple((dimension, obstacleType(*obstacle)) for obstacle in obstacles)

    domainDimTag, obstacleDimTags = booleanOperations(domainDimTag, obstacleDimTags)

    __core.__sync()

    __core.__add_physical_group(dim=dimension, tags=(domainDimTag[0][1],), tag=1)
    if obstacleDimTags:
        __core.__add_physical_group(dim=dimension, tags=tuple(tag for _, tag in obstacleDimTags), tag=2)
    if dimension == 2:
        __core.__mark_2d_boundaries(size)
    elif dimension == 3:
        __core.__mark_3d_boundaries(size)

    __core.__set_options(meshSize, algorithm2d, algorithm3d)
    __core.__generate_mesh(dim=dimension, refine=0)

    if fltk:
        __core.__run_fltk()

    gmsh.write(folder + '/temp.msh')

    meshElementType = 2 if dimension == 2 else 4

    nodeTags, nodeCoords = __core.__get_nodes()
    elementTags, elementNodeTags = __core.__get_elements(-1, -1, meshElementType)

    __core.__finalize_gmsh()

    return (nodeTags, nodeCoords), (elementTags, elementNodeTags)


def loadMesh(fileName, dimension):
    if not USE_GMSH:
        raise ImportError('GMSH is not found!')

    __core.__initialize_gmsh()

    __core.__load_file(fileName)

    meshElementType = 2 if dimension == 2 else 4

    nodeTags, nodeCoords = __core.__get_nodes()
    elementTags, elementNodeTags = __core.__get_elements(-1, -1, meshElementType)

    __core.__finalize_gmsh()

    return (nodeTags, nodeCoords), (elementTags, elementNodeTags)
