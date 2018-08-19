from .directory import Directory
from .directory import mv as dmv
from .directory import rm as drm
from .directory import cp as dcp
from .file import File
from .file import mv as fmv
from .file import rm as frm
from .file import cp as fcp


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