from fs.osfs import OSFS
from ..path.model import Path
from ..file.model import File
import pathlib
import yaml


class Directory:
    yaml_tag = '!directory'

    def __init__(self, path, load_depth=0):
        if isinstance(path,Path):
            self.path = path
        else:
            self.path = Path(path)
        if load_depth > 0:
            self.load(load_depth)
        else:
            self.children = None
            

    def load(self, depth):
        self.children = None
        if depth < 0:
            return
        if not self.exists:
            raise DirectoryNotFoundError(self.path.abs)
        if depth == 0:
            return
        self.children = []
        with OSFS('/') as fs:
            for f in fs.listdir(self.path.relative):
                fp = self.path / f
                if fs.isdir(fp.relative):
                    self.children.append(Directory(fp, depth - 1))
                else:
                    self.children.append(File(fp, 0))

    @staticmethod
    def is_dir(path:Path):
        return pathlib.Path(path.abs).is_dir()

    @property
    def exists(self):
        with OSFS('/') as fs:
            return fs.exists(self.path.relative) and Directory.is_dir(self.path)

    def ensure(self):
        if not self.exists:
            with OSFS('/') as fs:
                fs.makedirs(self.path.relative)

    def to_serializable(self):
        return {'path': self.path.abs,
                'name': self.path.name,
                'is_dir': True,
                'children': [c.to_serializable() for c in self.children] if self.children is not None else None
                }

    def __str__(self):
        import json
        return json.dumps(self.to_serializable(), sort_keys=True, separators=(',', ':'), indent=4)
