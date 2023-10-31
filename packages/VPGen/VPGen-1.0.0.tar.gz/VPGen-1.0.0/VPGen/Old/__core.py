try:
    import gmsh

    def __initialize_gmsh():
        __finalize_gmsh()
        gmsh.initialize()

    def __finalize_gmsh():
        if gmsh.isInitialized():
            gmsh.finalize()

    def __get_2d():
        return gmsh.model.occ.addRectangle, addDisk

    def __get_3d():
        return gmsh.model.occ.addBox, gmsh.model.occ.addSphere

    def addDisk(x, y, z, r):
        return gmsh.model.occ.addDisk(x, y, z, r, r)

    def __heterogenousBooleanOperations(domainDimTag, obstacleDimTags):
        obstacleDimTags = gmsh.model.occ.intersect(obstacleDimTags, domainDimTag, removeTool=False)[0]
        return gmsh.model.occ.cut(domainDimTag, obstacleDimTags, removeTool=False)[0], obstacleDimTags

    def __nonHeterogenousBooleanOperations(domainDimTag, obstacleDimTags):
        return gmsh.model.occ.cut(domainDimTag, obstacleDimTags)[0], []

    def __mark_2d_boundaries(size, eps=1e-3):
        for xmin, xmax, ymin, ymax, tag in (
            (0, 1, 1, 1, 1),  # top
            (1, 1, 0, 1, 2),  # right
            (0, 1, 0, 0, 3),  # bottom
            (0, 0, 0, 1, 4),  # left
        ):
            tags = gmsh.model.getEntitiesInBoundingBox(size[0]*xmin-eps, size[1]*ymin-eps, -eps, size[0]*xmax+eps, size[1]*ymax+eps, eps,dim=1)
            gmsh.model.addPhysicalGroup(1, tuple(tag for _, tag in tags), tag=tag)

        # topTags = gmsh.model.getEntitiesInBoundingBox(-eps, size[1]-eps, -eps, size[0]+eps, size[1]+eps, eps,dim=1)
        # gmsh.model.addPhysicalGroup(1, tuple(tag for _, tag in topTags), tag=1)

        # rightTags = gmsh.model.getEntitiesInBoundingBox(size[0]-eps, -eps, -eps, size[0]+eps, size[1]+eps, eps,dim=1)
        # gmsh.model.addPhysicalGroup(1, tuple(tag for _, tag in rightTags), tag=2)

        # bottomTags = gmsh.model.getEntitiesInBoundingBox(-eps, -eps, -eps, size[0]+eps, eps, eps,dim=1)
        # gmsh.model.addPhysicalGroup(1, tuple(tag for _, tag in bottomTags), tag=3)

        # leftTags = gmsh.model.getEntitiesInBoundingBox(-eps, -eps, -eps, eps, size[1]+eps, eps,dim=1)
        # gmsh.model.addPhysicalGroup(1, tuple(tag for _, tag in leftTags), tag=4)

        obstacleTags = gmsh.model.getEntitiesInBoundingBox(eps, eps, -eps, size[0]-eps, size[1]-eps, eps,dim=1)
        gmsh.model.addPhysicalGroup(1, tuple(tag for _, tag in obstacleTags), tag=5)

    def __mark_3d_boundaries(size, eps=1e-3):
        for xmin, xmax, ymin, ymax, zmin, zmax, tag in (
            (0, 1, 0, 1, 1, 1, 1),  # top
            (1, 1, 0, 1, 0, 1, 2),  # right
            (0, 1, 0, 1, 0, 0, 3),  # bottom
            (0, 0, 0, 1, 0, 1, 4),  # left
            (0, 1, 1, 1, 0, 1, 5),  # front
            (0, 1, 0, 0, 0, 1, 6),  # back
        ):
            tags = gmsh.model.getEntitiesInBoundingBox(size[0]*xmin-eps, size[1]*ymin-eps, size[2]*zmin-eps, size[0]*xmax+eps, size[1]*ymax+eps, size[2]*zmax+eps,dim=2)
            gmsh.model.addPhysicalGroup(2, tuple(tag for _, tag in tags), tag=tag)

        obstacleTags = gmsh.model.getEntitiesInBoundingBox(eps, eps, eps, size[0]-eps, size[1]-eps, size[2]-eps,dim=2)
        gmsh.model.addPhysicalGroup(2, tuple(tag for _, tag in obstacleTags), tag=7)

    def __set_options(meshSize, algorithm2d, algorithm3d):
        if algorithm2d is not None:
            gmsh.option.setNumber('Mesh.Algorithm', algorithm2d)
        if algorithm3d is not None:
            gmsh.option.setNumber('Mesh.Algorithm3D', algorithm3d)
        if meshSize is not None:
            gmsh.option.setNumber('Mesh.MeshSizeFactor', meshSize)
        gmsh.option.setNumber('Mesh.MshFileVersion', 2.2)

    def __generate_mesh(dim, refine=0):
        gmsh.model.mesh.generate(dim=dim)
        for _ in range(refine):
            gmsh.model.mesh.refine()
        if refine > 0:
            gmsh.model.mesh.generate(dim=dim)

    def __sync():
        gmsh.model.occ.synchronize()

    def __run_fltk():
        gmsh.fltk.initialize()
        gmsh.fltk.unlock()
        gmsh.fltk.run()
        gmsh.fltk.awake()
        gmsh.fltk.finalize()

    def __add_physical_group(dim, tags, tag):
        gmsh.model.addPhysicalGroup(dim, tags, tag=tag)

    def __get_nodes():
        nodes = gmsh.model.mesh.get_nodes()[:2]
        return tuple(nodes[0]), tuple(nodes[1])

    def __get_elements(dim, tag, meshElementType):
        elements = gmsh.model.mesh.getElements(dim=dim, tag=tag)
        index = tuple(elements[0]).index(meshElementType)
        return tuple(elements[1][index]), tuple(elements[2][index])

    def __load_file(fileName):
        gmsh.open(fileName)

except ModuleNotFoundError:
    pass
