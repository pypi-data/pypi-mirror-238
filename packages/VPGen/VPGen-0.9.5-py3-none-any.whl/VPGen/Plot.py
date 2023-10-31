try:
    from vtk import (
        vtkRenderWindow,
        vtkRenderer,
        vtkRenderWindowInteractor,
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

    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.addRenderer(renderer)
