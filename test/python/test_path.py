import unittest
from unittest.mock import MagicMock
from jfs.api import Path
from dxl.data import List
import pytest
import itertools

INPUTS1 = List(['/','/tmp', '%2Ftmp', '%252Ftmp', './tmp', '/tmp/a/..'])
OUTPUTS1 = List(['/', '/tmp', '/tmp', '/tmp', 'tmp', '/tmp'])
INPUTS2 = ['/', 'tmp', '/tmp','/tmp/']
OUTPUTS2 = ['/', '/home/twj2417/filesystem/test/python/tmp', '/tmp','/tmp']
OUTPUTS22 = ['', 'tmp', 'tmp', 'tmp']
OUTPUTS222 = [True,False,False,False]
OUTPUTS2222 = [True,False,True,True]
INPUTS3 = ['/', 'a', '/a/b', '/a/b/']
OUTPUTS3 = ['', 'a', 'b', 'b']
INPUTS4 = ['a/b', '/a/b', '/a/b/', 'a/b/']
OUTPUTS4 = ['/home/twj2417/filesystem/test/python/a', '/a', '/a', '/home/twj2417/filesystem/test/python/a']
INPUTS5 = ['a', 'a.txt', '/a/b.pdf', './b.zip']
OUTPUTS5 = ['','.txt','.pdf','.zip']
INPUTS6 = ['a', 'a.txt', '/a/b.tar.gz']
OUTPUTS6 = [[],['.txt'],['.tar','.gz']]
INPUTS7 = ['a', 'a/b', '/a/b', './a', '/a/b/c/..']
OUTPUTS7 = ['a', 'a/b', '/a/b', './a', '/a/b']


class TestPath:
    @pytest.mark.parametrize('input, output',list(zip(INPUTS1,OUTPUTS1)))
    def test_route(self,input,output):
        assert Path(input).route ==output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS2,OUTPUTS2)))
    def test_abs(self,input,output):
        assert Path(input).abs == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS2,OUTPUTS2)))
    def test_absolute(self,input,output):
        assert Path(input).absolute().route == output     

    @pytest.mark.parametrize('input, output',list(zip(INPUTS2,OUTPUTS22)))    
    def test_relative(self,input,output):
        assert Path(input).relative == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS3,OUTPUTS3)))
    def test_name(self, input, output):
        assert Path(input).name == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS4,OUTPUTS4)))
    def test_father(self,input,output):
        assert Path(input).father == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS4,OUTPUTS4)))
    def test_fatherpath(self,input,output):    
        assert Path(input).father_path().route ==output        

    @pytest.mark.parametrize('input, output',list(zip(INPUTS5,OUTPUTS5)))
    def test_suffix(self,input,output):   
        assert Path(input).suffix == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS6,OUTPUTS6)))
    def test_suffixes(self,input,output):    
        assert Path(input).suffixes == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS2,OUTPUTS222)))
    def test_isroot(self,input,output):
        assert Path(input).isroot == output

    @pytest.mark.parametrize('input, output',list(zip(INPUTS2,OUTPUTS2222)))
    def test_isabs(self,input,output):
        assert Path(input).isabs == output
   
    @pytest.mark.parametrize('xi,xo',list(zip(INPUTS7,OUTPUTS7)))
    def test_eq(self,xi,xo):
        assert Path(xi) == Path(xo)

class Test_Path(unittest.TestCase):
    def test_parts(self):
        with self.subTest(0):
            p = Path('/tmp/base')
            self.assertEqual(p.parts(), ('/', 'tmp', 'base'))
        with self.subTest(1):
            p = Path('a/b')
            self.assertEqual(p.parts(), ('a', 'b'))

    def test_div(self):
        with self.subTest(0):
            p = Path('/tmp')
            p = p / 'sub'
            self.assertEqual(p.route, '/tmp/sub')
        with self.subTest(1):
            p = Path('/tmp')
            p = p / 'sub/'
            self.assertEqual(p.route, '/tmp/sub')
    
    def test_dot(self):
        self.assertEqual(Path('.').route, '')

    def test_join_dot(self):
        self.assertEqual((Path('.') / 'a').route, 'a')

    def test_empty_protocol(self):
        self.assertEqual(Path('a', '').route, 'a')