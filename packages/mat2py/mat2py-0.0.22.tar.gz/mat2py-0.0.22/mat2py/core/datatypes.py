# type: ignore

__all__ = [
    "iscom",
    "orderfields",
    "deal",
    "uint16",
    "typecast",
    "inferiorto",
    "int32",
    "function_handle",
    "functions",
    "isinterface",
    "findgroups",
    "double",
    "_class",
    "isenum",
    "str2func",
    "javaArray",
    "array2table",
    "cell2struct",
    "cast",
    "fieldnames",
    "single",
    "struct2cell",
    "getfield",
    "rmfield",
    "iscell",
    "logical",
    "isjava",
    "setfield",
    "javaMethod",
    "table2cell",
    "methods",
    "int8",
    "saveobj",
    "properties",
    "swapbytes",
    "substruct",
    "uint64",
    "superclasses",
    "uint8",
    "isnumeric",
    "isobject",
    "istable",
    "superiorfloat",
    "isfield",
    "javaObject",
    "islogical",
    "cell2mat",
    "ismethod",
    "javaObjectEDT",
    "structfun",
    "cellfun",
    "int64",
    "enumeration",
    "splitapply",
    "isinteger",
    "isstruct",
    "table2struct",
    "isa",
    "num2cell",
    "struct2table",
    "superiorto",
    "events",
    "mat2cell",
    "func2str",
    "cell",
    "methodsview",
    "loadobj",
    "celldisp",
    "cellplot",
    "table2array",
    "isprop",
    "int16",
    "cell2table",
    "iscategorical",
    "uint32",
    "arrayfun",
    "struct",
    "isfloat",
    "javaMethodEDT",
    "metaclass",
]

from mat2py.common.backends import numpy as np

from ._internal import M
from ._internal.cell import CellArray, cell
from ._internal.math_helper import mp_type_cast_decorators
from ._internal.struct import StructArray, struct


def iscom(*args):
    raise NotImplementedError("iscom")


def orderfields(*args):
    raise NotImplementedError("orderfields")


def deal(*args):
    raise NotImplementedError("deal")


def uint16(*args):
    raise NotImplementedError("uint16")


def typecast(*args):
    raise NotImplementedError("typecast")


def inferiorto(*args):
    raise NotImplementedError("inferiorto")


def int32(*args):
    raise NotImplementedError("int32")


def function_handle(*args):
    raise NotImplementedError("function_handle")


def functions(*args):
    raise NotImplementedError("functions")


def isinterface(*args):
    raise NotImplementedError("isinterface")


def findgroups(*args):
    raise NotImplementedError("findgroups")


@mp_type_cast_decorators()
def double(dtype):
    return np.complex128 if np.issubdtype(dtype, np.complex_) else np.float64


def _class(*args):
    raise NotImplementedError("_class")


def isenum(*args):
    raise NotImplementedError("isenum")


def str2func(*args):
    raise NotImplementedError("str2func")


def javaArray(*args):
    raise NotImplementedError("javaArray")


def array2table(*args):
    raise NotImplementedError("array2table")


def cell2struct(*args):
    raise NotImplementedError("cell2struct")


def cast(*args):
    raise NotImplementedError("cast")


from ._internal.struct import fieldnames


@mp_type_cast_decorators()
def single(dtype):
    return np.complex64 if np.issubdtype(dtype, np.complex_) else np.float32


def struct2cell(*args):
    raise NotImplementedError("struct2cell")


def getfield(*args):
    raise NotImplementedError("getfield")


def rmfield(*args):
    raise NotImplementedError("rmfield")


def iscell(*args):
    raise NotImplementedError("iscell")


def logical(*args):
    raise NotImplementedError("logical")


def isjava(*args):
    raise NotImplementedError("isjava")


def setfield(*args):
    raise NotImplementedError("setfield")


def javaMethod(*args):
    raise NotImplementedError("javaMethod")


def table2cell(*args):
    raise NotImplementedError("table2cell")


def methods(*args):
    raise NotImplementedError("methods")


def int8(*args):
    raise NotImplementedError("int8")


def saveobj(*args):
    raise NotImplementedError("saveobj")


def properties(*args):
    raise NotImplementedError("properties")


def swapbytes(*args):
    raise NotImplementedError("swapbytes")


def substruct(*args):
    raise NotImplementedError("substruct")


def uint64(*args):
    raise NotImplementedError("uint64")


def superclasses(*args):
    raise NotImplementedError("superclasses")


def uint8(*args):
    raise NotImplementedError("uint8")


def isnumeric(*args):
    raise NotImplementedError("isnumeric")


def isobject(*args):
    raise NotImplementedError("isobject")


def istable(*args):
    raise NotImplementedError("istable")


def superiorfloat(*args):
    raise NotImplementedError("superiorfloat")


def isfield(*args):
    raise NotImplementedError("isfield")


def javaObject(*args):
    raise NotImplementedError("javaObject")


def islogical(*args):
    raise NotImplementedError("islogical")


def cell2mat(*args):
    raise NotImplementedError("cell2mat")


def ismethod(*args):
    raise NotImplementedError("ismethod")


def javaObjectEDT(*args):
    raise NotImplementedError("javaObjectEDT")


def structfun(*args):
    raise NotImplementedError("structfun")


def cellfun(*args):
    raise NotImplementedError("cellfun")


def int64(*args):
    raise NotImplementedError("int64")


def enumeration(*args):
    raise NotImplementedError("enumeration")


def splitapply(*args):
    raise NotImplementedError("splitapply")


def isinteger(*args):
    raise NotImplementedError("isinteger")


def isstruct(*args):
    raise NotImplementedError("isstruct")


def table2struct(*args):
    raise NotImplementedError("table2struct")


def isa(*args):
    raise NotImplementedError("isa")


def num2cell(*args):
    raise NotImplementedError("num2cell")


def struct2table(*args):
    raise NotImplementedError("struct2table")


def superiorto(*args):
    raise NotImplementedError("superiorto")


def events(*args):
    raise NotImplementedError("events")


def mat2cell(*args):
    raise NotImplementedError("mat2cell")


def func2str(*args):
    raise NotImplementedError("func2str")


def methodsview(*args):
    raise NotImplementedError("methodsview")


def loadobj(*args):
    raise NotImplementedError("loadobj")


def celldisp(*args):
    raise NotImplementedError("celldisp")


def cellplot(*args):
    raise NotImplementedError("cellplot")


def table2array(*args):
    raise NotImplementedError("table2array")


def isprop(*args):
    raise NotImplementedError("isprop")


def int16(*args):
    raise NotImplementedError("int16")


def cell2table(*args):
    raise NotImplementedError("cell2table")


def iscategorical(*args):
    raise NotImplementedError("iscategorical")


def uint32(*args):
    raise NotImplementedError("uint32")


def arrayfun(*args):
    raise NotImplementedError("arrayfun")


def isfloat(*args):
    raise NotImplementedError("isfloat")


def javaMethodEDT(*args):
    raise NotImplementedError("javaMethodEDT")


def metaclass(*args):
    raise NotImplementedError("metaclass")
