# type: ignore

__all__ = [
    "unmkpp",
    "xyzchk",
    "griddata",
    "interp1",
    "roots",
    "poly",
    "splncore",
    "griddatan",
    "tsearchn",
    "convhulln",
    "interp2",
    "interp1q",
    "delaunayn",
    "rectint",
    "polyarea",
    "pchip",
    "ppval",
    "polyval",
    "interp3",
    "polyvalm",
    "interpft",
    "voronoin",
    "delaunay",
    "spline",
    "boundary",
    "qhull",
    "automesh",
    "pwch",
    "dsearchn",
    "xyzvchk",
    "inpolygon",
    "mkpp",
    "polyfit",
    "polyder",
    "interpn",
    "polyint",
    "convhull",
    "xychk",
]

from mat2py.core._internal.helper import mp_inference_nargout_decorators


def unmkpp(*args):
    raise NotImplementedError("unmkpp")


def xyzchk(*args):
    raise NotImplementedError("xyzchk")


def griddata(*args):
    raise NotImplementedError("griddata")


def interp1(*args):
    raise NotImplementedError("interp1")


def roots(*args):
    raise NotImplementedError("roots")


def poly(*args):
    raise NotImplementedError("poly")


def splncore(*args):
    raise NotImplementedError("splncore")


def griddatan(*args):
    raise NotImplementedError("griddatan")


def tsearchn(*args):
    raise NotImplementedError("tsearchn")


def convhulln(*args):
    raise NotImplementedError("convhulln")


def interp2(*args):
    raise NotImplementedError("interp2")


def interp1q(*args):
    raise NotImplementedError("interp1q")


def delaunayn(*args):
    raise NotImplementedError("delaunayn")


def rectint(*args):
    raise NotImplementedError("rectint")


def polyarea(*args):
    raise NotImplementedError("polyarea")


def pchip(*args):
    raise NotImplementedError("pchip")


def ppval(*args):
    raise NotImplementedError("ppval")


def polyval(*args):
    raise NotImplementedError("polyval")


def interp3(*args):
    raise NotImplementedError("interp3")


def polyvalm(*args):
    raise NotImplementedError("polyvalm")


def interpft(*args):
    raise NotImplementedError("interpft")


def voronoin(*args):
    raise NotImplementedError("voronoin")


def delaunay(*args):
    raise NotImplementedError("delaunay")


def spline(*args):
    raise NotImplementedError("spline")


def boundary(*args):
    raise NotImplementedError("boundary")


def qhull(*args):
    raise NotImplementedError("qhull")


def automesh(*args):
    raise NotImplementedError("automesh")


def pwch(*args):
    raise NotImplementedError("pwch")


def dsearchn(*args):
    raise NotImplementedError("dsearchn")


def xyzvchk(*args):
    raise NotImplementedError("xyzvchk")


@mp_inference_nargout_decorators()
def inpolygon(*args, nargout=None, **kwargs):
    from mat2py.toolbox.matlab.polyfun import inpolygon as _inpolygon

    return _inpolygon(*args, **kwargs, nargout=nargout)


def mkpp(*args):
    raise NotImplementedError("mkpp")


def polyfit(*args):
    raise NotImplementedError("polyfit")


def polyder(*args):
    raise NotImplementedError("polyder")


def interpn(*args):
    raise NotImplementedError("interpn")


def polyint(*args):
    raise NotImplementedError("polyint")


def convhull(*args):
    raise NotImplementedError("convhull")


def xychk(*args):
    raise NotImplementedError("xychk")
