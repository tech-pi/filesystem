from fs.osfs import OSFS
from .model import File


def touch(f : File):
    with OSFS('/') as fs:
        fs.create(f.path.relative)


def mv(f : File, path_new, overwrite=True):
    with OSFS('/') as fs:
        fs.move(f.path.relative, path_new.relative, overwrite)


def cp(f : File, path_new, overwrite=True):
    with OSFS('/') as fs:
        fs.copy(f.path.relative, path_new.relative, overwrite)


def rm(f : File):
    with OSFS('/') as fs:
        fs.remove(f.path.relative)
