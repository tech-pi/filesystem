import pytest
import unittest
from jfs.api import Path,Directory,mkdir,mv,cp,rm
import tempfile
import shutil

class TestFile(unittest.TestCase):
    def setUp(self):
        dpath = tempfile.mkdtemp()
        dpath1 = tempfile.mkdtemp()
        pdr = Path(dpath)
        pf1 = Directory(pdr / 'sub1')
        mkdir(pf1)
        pf2 = Directory(pdr / 'sub2')
        mkdir(pf2)
        pd6 = pdr / 'sub6' 
        mkdir(Directory(pd6))
        pd7 = Directory(pd6 / 'sub7')
        mkdir(pd7)
        self.root = dpath
        self.root1 = Path(dpath1)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_exists(self):
        def pos():
            dir1 = Directory((Path(self.root) / 'sub1').abs)         
            assert (dir1.exists)

        def neg():
            dir1 = Directory((Path(self.root) / 'sub7').abs)
            assert not (dir1.exists)
        pos()
        neg()

    def test_create_directory(self):
        dir1 = Directory(self.root + '/sub3')
        mkdir(dir1)
        assert dir1.exists

    def test_is_dir(self):
        def pos():
            dir1 = Directory(self.root + '/sub1')
            assert dir1.is_dir
        def neg1():
            dir1 = Directory(self.root + '/subx')
            assert not dir1.is_dir
        def neg2():
            dir1 = Directory(self.root + '/tmp.txt')
            assert not dir1.is_dir
        pos()
        neg1()
        neg2()

    def test_delete_directory(self):
        dir1 = Directory(self.root + '/sub2')
        rm(dir1)
        assert not dir1.exists

    def test_copy_directory(self):
        dir1 = Directory(self.root + '/sub6')
        cp(dir1,Path(self.root1+'/sub9'))
        dir2 = Directory(self.root1+'/sub9')
        assert dir2.exists and dir1.exists

    def test_move_directory(self):
        dir1 = Directory(self.root + '/sub6')
        mv(dir1,Path(self.root1))
        dir2 = Directory(self.root1)
        assert dir2.exists and Directory(self.root1+'/sub7') and not dir1.exists