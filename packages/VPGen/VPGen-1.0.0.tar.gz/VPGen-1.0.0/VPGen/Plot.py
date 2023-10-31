try:
    from vtk import (
        vtkRenderWindow,
        vtkRenderer,
        vtkRenderWindowInteractor,
        vtkSphereSource,
        vtkPolyDataMapper,
        vtkActor,
        vtkInteractorStyleTrackballCamera,
        vtkPoints,
        vtkCellArray,
        vtkPolyData,
        vtkAxesActor,
        vtkOrientationMarkerWidget,
        vtkTextProperty,
    )
    USE_VTK = True
except ModuleNotFoundError:
    USE_VTK = False
try:
    from matplotlib import pyplot, patches
    USE_MATPLOTLIB = True
except ModuleNotFoundError:
    USE_MATPLOTLIB = False

from .Classes import Domain


def plot2d(domain: Domain, obstacles: tuple, savefig: str=None, indent: bool=True) -> None:
    '''
    Creates plot of obstacles (circles).

    domain: Domain - geometry
    obstacles: tuple - tuple of obstacles
    savefig: str - name of filename to save or will show if None
    indent: bool - show indent or not

    return - None
    '''

    if not USE_MATPLOTLIB:
        print('No matplotlib?')
        return

    if domain.dimension != 2:
        print('plot2d!')

    ax, fig = pyplot.subplots()

    for obstacle in obstacles:
        fig.add_patch(
            patches.Circle(
                (obstacle.center.x, obstacle.center.y), obstacle.radius
            )
        )
    fig.set_xlim(
        domain.origin.x + (domain.indent.x if indent else 0),
        domain.origin.x + domain.indent.x + (domain.indent.x if not indent else 0) + domain.size.x
    )
    fig.set_ylim(
        domain.origin.y + (domain.indent.y if indent else 0),
        domain.origin.y + domain.indent.y + (domain.indent.y if not indent else 0) + domain.size.y
    )

    if savefig is None:
        try:
            pyplot.show()
        except Exception as error:
            print('pyplot.show() error:', str(error))
            ax.savefig('_error.png')
    else:
        ax.savefig(savefig + '.png')


def plot3d(domain: Domain, obstacles:tuple) -> None:
    '''
    Creates plot of obstacles (spheres).

    domain: Domain - geometry
    obstacles: tuple - tuple of obstacles

    return - None
    '''

    if not USE_VTK:
        print('No vtk?')
        return

    if domain.dimension != 3:
        print('plot3d!')

    # TODO make using vtk

    ps = [
        [domain.origin.x, domain.origin.x + domain.size.x],
        [domain.origin.y, domain.origin.y + domain.size.y],
        [domain.origin.z, domain.origin.z + domain.size.z],
    ]

    points = vtkPoints()
    for i in range(2):
        for j in range(2):
            for k in range(2):
                points.InsertNextPoint(ps[0][i], ps[1][j], ps[2][k])

    lines = vtkCellArray()
    insertFace([1, 0, 2, 3], lines)
    insertFace([5, 4, 6, 7], lines)
    insertLine([0, 4], lines)
    insertLine([1, 5], lines)
    insertLine([2, 6], lines)
    insertLine([3, 7], lines)

    outline = vtkPolyData()
    outline.SetPoints(points)
    outline.SetLines(lines)

    outlineMapper = vtkPolyDataMapper()
    outlineMapper.SetInputData(outline)

    outlineActor = vtkActor()
    outlineActor.SetMapper(outlineMapper)

    outlineActor.GetProperty().SetColor(1, 1, 1)

    renderer = vtkRenderer()

    for obstacle in obstacles:
        renderer.AddActor(
            createSphereActor(obstacle.center, obstacle.radius)
        )
    renderer.AddActor(outlineActor)

    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    
    interactor = vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
    interactor.SetRenderWindow(renderWindow)

    textProperty = vtkTextProperty()
    textProperty.SetColor(1, 1, 1)
    textProperty.SetBold(False)
    textProperty.SetItalic(False)
    textProperty.SetShadow(False)

    axesActor = vtkAxesActor()
    axesActor.GetXAxisCaptionActor2D().SetCaptionTextProperty(textProperty)
    axesActor.GetYAxisCaptionActor2D().SetCaptionTextProperty(textProperty)
    axesActor.GetZAxisCaptionActor2D().SetCaptionTextProperty(textProperty)
    
    orientationMarker = vtkOrientationMarkerWidget()
    orientationMarker.SetOrientationMarker(axesActor)
    orientationMarker.SetInteractor(interactor)
    orientationMarker.EnabledOn()
    orientationMarker.InteractiveOn()
    orientationMarker.SetOutlineColor(1, 1, 1)

    renderer.ResetCamera()

    interactor.Initialize()
    interactor.Start()


def createSphereActor(center, radius):
    source = vtkSphereSource()
    source.SetCenter(*center())
    source.SetRadius(radius)
    source.Update()

    mapper = vtkPolyDataMapper()
    mapper.SetInputData(source.GetOutput())

    actor = vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetColor(1, 1, 1)

    return actor


def insertFace(ids, lines):
    lines.InsertNextCell(5)
    for id in ids + [ids[0]]:
        lines.InsertCellPoint(id)


def insertLine(ids, lines):
    lines.InsertNextCell(2)
    for id in ids:
        lines.InsertCellPoint(id)
