# type: ignore

__all__ = [
    "uplus",
    "horzcat",
    "mrdivide",
    "eq",
    "plus",
    "_or",
    "gt",
    "mtimes",
    "bitor",
    "le",
    "arith",
    "ismember",
    "bitcmp",
    "kron",
    "unique",
    "mpower",
    "minus",
    "intersect",
    "ctranspose",
    "paren",
    "union",
    "bitand",
    "ge",
    "xor",
    "mldivide",
    "any",
    "transpose",
    "idivide",
    "lt",
    "subsindex",
    "_and",
    "bitxor",
    "setxor",
    "power",
    "uminus",
    "setdiff",
    "ldivide",
    "bitset",
    "subsref",
    "bitget",
    "ismembertol",
    "subsasgn",
    "bitshift",
    "slash",
    "ne",
    "bitmax",
    "colon",
    "uniquetol",
    "punct",
    "times",
    "all",
    "relop",
    "_not",
    "vertcat",
    "rdivide",
]

from mat2py.common.backends import numpy as np

from ._internal.array import M, colon
from ._internal.helper import (
    mp_argout_wrapper_decorators,
    mp_inference_nargout_decorators,
    mp_last_arg_as_kwarg,
)
from ._internal.math_helper import mp_sum_like_decorators


def uplus(*args):
    raise NotImplementedError("uplus")


def horzcat(*args):
    raise M[list(args)]


@mp_argout_wrapper_decorators()
def mrdivide(b, a):
    r"""xA = B => x = B/A = (A'\B')'"""
    a, b = (
        (True, np.reshape(i, 1)[0]) if np.size(i) == 1 else (False, i) for i in (a, b)
    )
    if a[0] or b[0]:
        return M[b[1] / a[1]]
    else:
        return M[np.linalg.solve(a[1].T, b[1].T).T]


def eq(*args):
    raise NotImplementedError("eq")


def plus(*args):
    raise NotImplementedError("plus")


def _or(*args):
    raise NotImplementedError("_or")


def gt(*args):
    raise NotImplementedError("gt")


@mp_argout_wrapper_decorators()
def mtimes(a, b):
    return M[a] @ b


def bitor(*args):
    raise NotImplementedError("bitor")


def le(*args):
    raise NotImplementedError("le")


def arith(*args):
    raise NotImplementedError("arith")


@mp_inference_nargout_decorators()
@mp_last_arg_as_kwarg("row_as_one", ("rows",))
def ismember(a, b, row_as_one=False, nargout=None):
    if row_as_one:
        raise NotImplementedError("ismember")

    if nargout == 1:
        return (M[np.isin(a, b)],)

    a_shape = np.shape(a)
    a = a.reshape(-1)
    b = b.reshape(-1, order="F")
    sort_idx = b.argsort()
    out = sort_idx[np.searchsorted(b, a, sorter=sort_idx)]
    ia = b[out] == a
    out = out + 1
    out[np.logical_not(ia)] = 0

    return M[ia.reshape(*a_shape)], M[out.reshape(*a_shape)]


def bitcmp(*args):
    raise NotImplementedError("bitcmp")


kron = mp_argout_wrapper_decorators()(np.kron)


def unique(x, *args, nargout=3):
    if nargout != 3 or args:
        raise NotImplementedError("unique")
    c, ia, ic = np.unique(
        x.reshape(-1, order="F"), return_index=True, return_inverse=True
    )
    shape = (1, -1) if np.shape(x)[0] == 1 else (-1, 1)
    return M[c.reshape(*shape)], M[ia.reshape(-1, 1) + 1], M[ic.reshape(-1, 1) + 1]


def mpower(*args):
    raise NotImplementedError("mpower")


def minus(*args):
    raise NotImplementedError("minus")


def intersect(*args):
    raise NotImplementedError("intersect")


def ctranspose(*args):
    raise NotImplementedError("ctranspose")


def paren(*args):
    raise NotImplementedError("paren")


def union(*args):
    raise NotImplementedError("union")


def bitand(*args):
    raise NotImplementedError("bitand")


def ge(*args):
    raise NotImplementedError("ge")


def xor(*args):
    raise NotImplementedError("xor")


@mp_argout_wrapper_decorators()
def mldivide(a, b):
    r"""Ax = B => x = A\B"""
    a, b = (
        (True, np.reshape(i, 1)[0]) if np.size(i) == 1 else (False, i) for i in (a, b)
    )
    if a[0] or b[0]:
        return M[b[1] / a[1]]
    else:
        return M[np.linalg.solve(a[1], b[1])]


any = mp_sum_like_decorators(default_if_empty=1)(np.any)


def transpose(*args):
    raise NotImplementedError("transpose")


def idivide(*args):
    raise NotImplementedError("idivide")


lt = np.less


def subsindex(*args):
    raise NotImplementedError("subsindex")


def _and(*args):
    raise NotImplementedError("_and")


def bitxor(*args):
    raise NotImplementedError("bitxor")


def setxor(*args):
    raise NotImplementedError("setxor")


def power(*args):
    raise NotImplementedError("power")


def uminus(*args):
    raise NotImplementedError("uminus")


def setdiff(*args):
    raise NotImplementedError("setdiff")


def ldivide(*args):
    raise NotImplementedError("ldivide")


def bitset(*args):
    raise NotImplementedError("bitset")


def subsref(*args):
    raise NotImplementedError("subsref")


def bitget(*args):
    raise NotImplementedError("bitget")


def ismembertol(*args):
    raise NotImplementedError("ismembertol")


def subsasgn(*args):
    raise NotImplementedError("subsasgn")


def bitshift(*args):
    raise NotImplementedError("bitshift")


def slash(*args):
    raise NotImplementedError("slash")


def ne(*args):
    raise NotImplementedError("ne")


def bitmax(*args):
    raise NotImplementedError("bitmax")


def uniquetol(*args):
    raise NotImplementedError("uniquetol")


def punct(*args):
    raise NotImplementedError("punct")


def times(*args):
    raise NotImplementedError("times")


all = mp_sum_like_decorators(default_if_empty=1)(np.all)


def relop(*args):
    raise NotImplementedError("relop")


_not = np.logical_not


def vertcat(*args):
    return M.__class_getitem__(args)


def rdivide(*args):
    raise NotImplementedError("rdivide")
