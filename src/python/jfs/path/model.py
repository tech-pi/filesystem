"""
Abstract of path object.
Features:
    An unified model for posix/windows/url/url_quoted paths.
"""

import pathlib 
import fs.path as fp
from doufo import DataClass
from doufo import Maybe
from urllib.parse import quote_plus,unquote_plus,urlparse

def _unified_protocol(p:str) ->str:
    if not p.endswith('@'):
        return p + '@'
    return p


def _divide_protocol(p: str) -> (str, str):
    n = p.find('@')
    if n >= len(p) - 1:
        return p[:], ''
    if n == -1:
        return None, p
    else:
        return p[:n + 1], p[n + 1:]

def _decode_url(p: str):
        return unquote_plus(unquote_plus(p))

def _unified_path(p)-> str:
        if isinstance(p, Path):
            return p._p
        if not isinstance(p, str):
            raise TypeError(
                "{} is not convertable to {}.".format(type(p), __class__))
        protocol, raw_path = _divide_protocol(p)
        raw_path = _decode_url(raw_path)
        raw_path = fp.normpath(raw_path)
        if protocol is None:
            return raw_path
        return protocol + raw_path

class Path:
    def __init__(self,path,protocol=None):
        if protocol is not None:
            path = _unified_protocol(protocol) + path
        self._p = _unified_path(path)
               
    @property
    def protocol(self) -> str:
        return _divide_protocol(self._p)[0]

    @property
    def raw(self) -> str:
        return _divide_protocol(self._p)[1]

    def raw_path(self) -> 'Path':
        """
        Returns raw path object, i.e. no protocol.
        """
        return Path(self.raw, None)

    @property
    def route(self) -> str:
        "Alias of self.raw_path"
        return self.raw

    @property
    def _r(self):
        return pathlib.Path(self.route)

    @property
    def abs(self) -> str:
        #return fp.abspath(self.route)
        if fp.isabs(self.route):
            return self.route
        else:
            from fs.osfs import OSFS
            with OSFS('.') as fs:
                return fs.getsyspath(self.route)

    def absolute(self) ->'Path':
        return Path(self.abs,self.protocol)

    @property
    def relative(self) ->str:
        return fp.relpath(self.route)

    @property
    def isroot(self) -> bool:
        return self.route == '/'
    
    @property
    def isabs(self):
        return fp.isabs(self.route)

    @property
    def name(self) ->str:
        return fp.basename(self.route)

    @property
    def father(self) ->str:
        return fp.dirname(self.abs)

    def father_path(self) ->'Path':
        return Path(self.father,self.protocol)

    def parts(self):
        return self._r.parts

    def is_exist(self):
        return self._r.exists()

    def join(self,name):
        return Path(fp.combine(self.route,name),self.protocol)

    def __truediv__(self, name):
        return self.join(name)

    def __add__(self, suffix):
        return Path(self.route + suffix, self.protocol)

    def __str__(self):
        return self._p

    def __hash__(self):
        return hash(self._p)

    def __eq__(self, path):
        return self._p == Path(path)._p

    @property
    def suffix(self):
        return self._r.suffix

    @property
    def suffixes(self):
        return self._r.suffixes

    