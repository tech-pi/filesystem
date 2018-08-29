from .directory import Directory
from .directory import mv as dmv
from .directory import rm as drm
from .directory import cp as dcp
from .file import File
from .file import mv as fmv
from .file import rm as frm
from .file import cp as fcp
import rx


def mv(sor, tar, overwrite=True):
    if isinstance(sor, Directory):
        dmv(sor, tar)
    else:
        fmv(sor, tar, overwrite)


def cp(sor, tar, overwrite=True):
    if isinstance(sor, Directory):
        dcp(sor, tar, overwrite)
    else:
        fcp(sor, tar, overwrite)


def rm(sor):
    if isinstance(sor, Directory):
        drm(sor)
    else:
        frm(sor)

def search(d:Directory,filter_func=None):
    if filter_func is None:
        def filter_func(x): return True
    return (rx.Obervable.from_().filter(filter_func))