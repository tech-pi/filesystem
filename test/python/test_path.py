import unittest
from unittest.mock import MagicMock
from tfs import Path
from ruamel.yaml import YAML
yaml = YAML()


def subtests(tc: unittest.TestCase, inputs, outputs, func, offset=0):
    for i, args in enumerate(zip(inputs, outputs)):
        with tc.subTest(i + offset):
            func(*args)


def subtests_ae(tc: unittest.TestCase, inputs, outputs, func, offset=0):
    subtests(tc, inputs, outputs,
             lambda xi, xo: tc.assertEqual(func(xi), xo), offset)

class TestPath(unittest.TestCase):
    # def test_str_root(self):
    #     p = Path('/')
    #     self.assertEqual(p.abs, '/')

    # def test_str_basic(self):
    #     p = Path('/tmp')
    #     self.assertEqual(p.abs, '/tmp')

    # def test_url(self):
    #     p = Path('%2Ftmp')
    #     self.assertEqual(p.abs, '/tmp')

    # def test_parts(self):
    #     p = Path('/tmp/base')
    #     self.assertEqual(p.parts, ('/', 'tmp', 'base'))

    # def test_parent(self):
    #     p = Path('/tmp/base')
    #     self.assertEqual(p.father, '/tmp')

    # def test_name(self):
    #     p = Path('/tmp/base')
    #     self.assertEqual(p.name, 'base')

    # ''' the same test case？'''
    # def test_name_dir(self):
    #     p = Path('/tmp/base/')
    #     self.assertEqual(p.name, 'base')

    # @unittest.skip
    # def test_brief(self):
    #     p = Path('/tmp/test')
    #     self.assertEqual(p.brief, {
    #         'name': 'test',
    #         'path': '/tmp/test'
    #     })

    # @unittest.skip
    # def test_detail(self):
    #     p = Path('/tmp/test')
    #     self.assertEqual(p.detail, {
    #         'name': 'test',
    #         'path': '/tmp/test',
    #         'parent': '/tmp',
    #         'url': '%2Ftmp%2Ftest',
    #         'suffix': '',
    #         'parts': ('/', 'tmp', 'test')
    #     })

    # def test_exists(self):
    #     def postive():
    #         fs = MagicMock()
    #         fs_exists = MagicMock(return_value=True)
    #         fs.exists = fs_exists
    #         p = Path('/tmp/temp.txt')
    #         assert p.check_exists(fs) == True

    #     def negtive():
    #         fs = MagicMock()
    #         fs_exists = MagicMock(return_value=False)
    #         fs.exists = fs_exists
    #         p = Path('/tmp/temp.txt')
    #         assert p.check_exists(fs) == False
    #     postive()
    #     negtive()

    # def test_copy_init(self):
    #     p = Path('/tmp/file')
    #     p2 = Path(p)
    #     assert p.abs == p2.abs

    # def test_div(self):
    #     p = Path('/tmp')
    #     p = p / 'sub'
    #     assert p.abs == '/tmp/sub'

    # @unittest.skip
    # def test_yaml_dump(self):
    #     p = Path('/tmp/test')
    #     assert yaml.dump(p) == "!path '/tmp/test'\n"

    # @unittest.skip
    # def test_yaml_load(self):
    #     p = yaml.load("!path '/tmp/test'\n")
    #     assert p.abs == "/tmp/test"


    def test_s(self):
        inputs = ['/', '/tmp', '%2Ftmp', '%252Ftmp', './tmp', '/tmp/a/..']
        outputs = ['/', '/tmp', '/tmp', '/tmp', 'tmp', '/tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).s)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).raw, len(inputs))

    def test_absolute_and_a(self):
        inputs = ['/', 'tmp', '/tmp']
        outputs = ['/', '/tmp', '/tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).a)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).absolute().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).absolute(),
                                                      Path),
                 len(inputs) * 2)

    def test_relative(self):
        inputs = ['/', 'tmp', '/tmp', '/tmp/']
        outputs = ['', 'tmp', 'tmp', 'tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).r)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).relative().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).relative(),
                                                      Path),
                 len(inputs) * 2)

    def test_name_and_n(self):
        inputs = ['/', 'a', '/a/b', '/a/b/']
        outputs = ['', 'a', 'b', 'b']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).n)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).name().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).name(), Path),
                 len(inputs) * 2)

    def test_parts(self):
        with self.subTest(0):
            p = Path('/tmp/base')
            self.assertEqual(p.parts(), ('/', 'tmp', 'base'))
        with self.subTest(1):
            p = Path('a/b')
            self.assertEqual(p.parts(), ('a', 'b'))

    def test_father_and_f(self):
        inputs = ['a/b', '/a/b', '/a/b/', 'a/b/']
        outputs = ['a', '/a', '/a', 'a']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).f)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).father().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).father(), Path),
                 len(inputs) * 2)

    def test_div(self):
        with self.subTest(0):
            p = Path('/tmp')
            p = p / 'sub'
            self.assertEqual(p.s, '/tmp/sub')
        with self.subTest(1):
            p = Path('/tmp')
            p = p / 'sub/'
            self.assertEqual(p.s, '/tmp/sub')

    def test_eq(self):
        ips = ['a', 'a/b', '/a/b', './a', '/a/b/c/..']
        ops = ['a', 'a/b', '/a/b', './a', '/a/b']
        subtests(self, ips, ops,
                 lambda xi, xo: self.assertTrue(Path(xi) == Path(xo)))

    def test_dot(self):
        self.assertEqual(Path('.').s, '')

    def test_join_dot(self):
        self.assertEqual((Path('.') / 'a').s, 'a')

    def test_empty_protocol(self):
        self.assertEqual(Path('a', '').s, 'a')