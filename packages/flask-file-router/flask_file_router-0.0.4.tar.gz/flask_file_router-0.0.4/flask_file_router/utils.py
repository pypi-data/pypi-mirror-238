import os
import functools


def normalizepath(path):
    return os.path.normpath(path).replace("\\", "/")


def pipe(arr):
    return functools.reduce(lambda a, b: b(a), arr)
