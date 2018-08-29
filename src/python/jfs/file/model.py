from ..path import Path
from fs.osfs import OSFS
import json
from doufo import DataClass
from ..filesystem import FS
import pathlib

class File:
    def __init__(self, path, load_depth=0):
        if isinstance(path,Path):
            self.path = path
        else:
            self.path = Path(path)
        if load_depth > 0:
            self.load(load_depth)
        else:
            self.contents = None
    
    @property
    def get_fs(self):
        return self.path.father

    @staticmethod
    def is_file(path:Path):
        return pathlib.Path(path.abs).is_file()

    @property
    def exists(self) -> bool:
        with FS(self.get_fs) as fs:
            return fs.exists(self.path.name) and File.is_file(self.path)

    def load(self, depth):
        self.contents = None
        if depth < 0:
            return
        if not self.exists:
            raise FileNotFoundError(self.path.abs)
        if depth == 0:
            return
        with FS(self.get_fs) as fs:
            with fs.open(self.path.abs, 'rb') as fin:
                self.contents = fin.read()

    def save(self, data):
        with FS(self.get_fs) as fs:
            with fs.open(self.path.abs, 'wb') as fout:
                self.contents = fout.write(data)
    

    def to_serializable(self):
        try:
            cont = self.contents.decode() if self.contents else None
        except UnicodeDecodeError:
            cont = '!!binary' + str(self.contents)
        return {'path': self.path.abs,
                'name': self.path.name,
                'is_dir': False,
                'contents': cont}

    def __str__(self):
        import json
        return json.dumps(self.to_serializable(), sort_keys=True, separators=(',', ':'), indent=4)
