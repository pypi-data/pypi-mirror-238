# type: ignore

__all__ = [
    "plotyy",
    "figtoolset",
    "getscribecontextmenu",
    "getobj",
    "scribeeventhandler",
    "setscribecontextmenu",
    "putdowntext",
    "gtext",
    "scribetextdlg",
    "doresize",
    "prepdrag",
    "scriberestoresavefcns",
    "zoom",
    "scribeclearmode",
    "domymenu",
    "ylabel",
    "getscribeobjectdata",
    "enddrag",
    "texlabel",
    "setscribeobjectdata",
    "polar",
    "getcolumn",
    "plotedit",
    "semilogx",
    "jpropeditutils",
    "basicfitdatastat",
    "plot",
    "box",
    "axis",
    "title",
    "loglog",
    "dokeypress",
    "semilogy",
    "doclick",
    "middrag",
    "text",
    "pan",
    "subplot",
    "xlabel",
    "rbbox",
    "grid",
    "moveaxis",
    "getorcreateobj",
]
from mat2py.common.backends import numpy as np

from ._internal import M


def plotyy(*args):
    raise NotImplementedError("plotyy")


def figtoolset(*args):
    raise NotImplementedError("figtoolset")


def getscribecontextmenu(*args):
    raise NotImplementedError("getscribecontextmenu")


def getobj(*args):
    raise NotImplementedError("getobj")


def scribeeventhandler(*args):
    raise NotImplementedError("scribeeventhandler")


def setscribecontextmenu(*args):
    raise NotImplementedError("setscribecontextmenu")


def putdowntext(*args):
    raise NotImplementedError("putdowntext")


def gtext(*args):
    raise NotImplementedError("gtext")


def scribetextdlg(*args):
    raise NotImplementedError("scribetextdlg")


def doresize(*args):
    raise NotImplementedError("doresize")


def prepdrag(*args):
    raise NotImplementedError("prepdrag")


def scriberestoresavefcns(*args):
    raise NotImplementedError("scriberestoresavefcns")


def zoom(*args):
    raise NotImplementedError("zoom")


def scribeclearmode(*args):
    raise NotImplementedError("scribeclearmode")


def domymenu(*args):
    raise NotImplementedError("domymenu")


def ylabel(*args):
    raise NotImplementedError("ylabel")


def getscribeobjectdata(*args):
    raise NotImplementedError("getscribeobjectdata")


def enddrag(*args):
    raise NotImplementedError("enddrag")


def texlabel(*args):
    raise NotImplementedError("texlabel")


def setscribeobjectdata(*args):
    raise NotImplementedError("setscribeobjectdata")


def polar(*args):
    raise NotImplementedError("polar")


def getcolumn(*args):
    raise NotImplementedError("getcolumn")


def plotedit(*args):
    raise NotImplementedError("plotedit")


def semilogx(*args):
    raise NotImplementedError("semilogx")


def jpropeditutils(*args):
    raise NotImplementedError("jpropeditutils")


def basicfitdatastat(*args):
    raise NotImplementedError("basicfitdatastat")


def plot(*args):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    while args:
        x, y, *args = args
        if args and isinstance(args[0], str):
            style, *args = args
            style = (style,)
        else:
            style = tuple()
        x = M[x].reshape(-1)
        y = M[y].reshape(-1)

        ax.plot(x, y, *style)
    return fig


def box(*args):
    raise NotImplementedError("box")


def axis(*args):
    raise NotImplementedError("axis")


def title(*args):
    raise NotImplementedError("title")


def loglog(*args):
    raise NotImplementedError("loglog")


def dokeypress(*args):
    raise NotImplementedError("dokeypress")


def semilogy(*args):
    raise NotImplementedError("semilogy")


def doclick(*args):
    raise NotImplementedError("doclick")


def middrag(*args):
    raise NotImplementedError("middrag")


def text(*args):
    raise NotImplementedError("text")


def pan(*args):
    raise NotImplementedError("pan")


def subplot(*args):
    raise NotImplementedError("subplot")


def xlabel(*args):
    raise NotImplementedError("xlabel")


def rbbox(*args):
    raise NotImplementedError("rbbox")


def grid(*args):
    raise NotImplementedError("grid")


def moveaxis(*args):
    raise NotImplementedError("moveaxis")


def getorcreateobj(*args):
    raise NotImplementedError("getorcreateobj")
