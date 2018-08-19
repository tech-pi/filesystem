import unittest
from unittest.mock import MagicMock
from jfs.path import Path
# from ruamel.yaml import YAML
# yaml = YAML()


def subtests(tc: unittest.TestCase, inputs, outputs, func, offset=0):
    for i, args in enumerate(zip(inputs, outputs)):
        with tc.subTest(i + offset):
            func(*args)


def subtests_ae(tc: unittest.TestCase, inputs, outputs, func, offset=0):
    subtests(tc, inputs, outputs,
             lambda xi, xo: tc.assertEqual(func(xi), xo), offset)

             
class TestPath(unittest.TestCase):
    def test_route(self):
        inputs = ['/', '/tmp', '%2Ftmp', '%252Ftmp', './tmp', '/tmp/a/..']
        outputs = ['/', '/tmp', '/tmp', '/tmp', 'tmp', '/tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).route)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).raw, len(inputs))

    def test_absolute_and_abs(self):
        inputs = ['/', 'tmp', '/tmp']
        outputs = ['/', '/home/twj2417/filesystem/test/python/tmp', '/tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).abs)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).absolute().route,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).absolute(),
                                                      Path),
                 len(inputs) * 2)

    def test_relative(self):
        inputs = ['/', 'tmp', '/tmp', '/tmp/']
        outputs = ['', 'tmp', 'tmp', 'tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).relative)

    def test_name(self):
        inputs = ['/', 'a', '/a/b', '/a/b/']
        outputs = ['', 'a', 'b', 'b']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).name)

    def test_parts(self):
        with self.subTest(0):
            p = Path('/tmp/base')
            self.assertEqual(p.parts(), ('/', 'tmp', 'base'))
        with self.subTest(1):
            p = Path('a/b')
            self.assertEqual(p.parts(), ('a', 'b'))

    def test_father_and_fatherpath(self):
        inputs = ['a/b', '/a/b', '/a/b/', 'a/b/']
        outputs = ['/home/twj2417/filesystem/test/python/a', '/a', '/a', '/home/twj2417/filesystem/test/python/a']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).father)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).father_path().route,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).father_path(), Path),
                 len(inputs) * 2)

    def test_suffix(self):
        inputs = ['a', 'a.txt', '/a/b.pdf', './b.zip']
        outputs = ['','.txt','.pdf','.zip']
        subtests_ae(self,inputs,outputs,lambda x:Path(x).suffix)

    def test_suffixes(self):
        inputs = ['a', 'a.txt', '/a/b.tar.gz']
        outputs = [[],['.txt'],['.tar','.gz']]
        subtests_ae(self,inputs,outputs,lambda x:Path(x).suffixes)

    def test_div(self):
        with self.subTest(0):
            p = Path('/tmp')
            p = p / 'sub'
            self.assertEqual(p.route, '/tmp/sub')
        with self.subTest(1):
            p = Path('/tmp')
            p = p / 'sub/'
            self.assertEqual(p.route, '/tmp/sub')

    def test_isroot(self):
        inputs = ['/', 'tmp/', '/tmp']
        outputs = [True,False,False]
        subtests_ae(self,inputs,outputs,lambda x:Path(x).isroot)

    def test_isabs(self):
        inputs = ['/', 'tmp/', '/tmp','.']
        outputs = [True,False,True,False]
        subtests_ae(self,inputs,outputs,lambda x:Path(x).isabs)
   
    def test_eq(self):
        ips = ['a', 'a/b', '/a/b', './a', '/a/b/c/..']
        ops = ['a', 'a/b', '/a/b', './a', '/a/b']
        subtests(self, ips, ops,
                 lambda xi, xo: self.assertTrue(Path(xi) == Path(xo)))

    def test_dot(self):
        self.assertEqual(Path('.').route, '')

    def test_join_dot(self):
        self.assertEqual((Path('.') / 'a').route, 'a')

    def test_empty_protocol(self):
        self.assertEqual(Path('a', '').route, 'a')