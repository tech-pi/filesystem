from fs.osfs import OSFS
from .model import Directory


def mkdir(d:Directory, recreate=True):
    with OSFS('/') as fs:
        fs.makedirs(d.path.relative, recreate=recreate)


def mv(d:Directory, path_new):
    with OSFS('/') as fs:
        fs.movedir(d.path.relative, path_new.relative)


def cp(d:Directory, path_new, create=True):
    with OSFS('/') as fs:
        fs.copydir(d.path.relative, path_new.relative, create)


def rm(d:Directory):
    with OSFS('/') as fs:
        fs.removetree(d.path.relative)