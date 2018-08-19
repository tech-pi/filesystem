import pytest
import unittest
from jfs.path import Path
from jfs.file import File,touch,mv,cp,rm
import tempfile
import shutil


class TestFile(unittest.TestCase):
    def setUp(self):
        dpath = tempfile.mkdtemp()
        dpath1 = tempfile.mkdtemp()
        pdr = Path(dpath)
        pf1 = File(pdr / 'tmp.txt')
        touch(pf1)
        pf2 = File(pdr / 'tmp2.txt')
        touch(pf2)
        pf3 = File(pdr / 'tmp4.txt')
        touch(pf3)
        with open(str(pf3.path), 'w') as fout:
            print('test3', file=fout)
        self.root = dpath
        self.root1 = dpath1

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_exists(self):
        def pos():
            file1 = File((Path(self.root) / 'tmp.txt').abs)         
            assert (file1.exists)

        def neg():
            file1 = File((Path(self.root) / 'tmpx.txt').abs)
            assert not (file1.exists)
        pos()
        neg()

    def test_is_file(self):
        def pos():
            file1 = File((Path(self.root) + '/tmp.txt'))
            assert (file1.is_file)
        def neg1():
            fil2=File((Path(self.root) + '/tmpx.txt'))
            assert not file2.is_file
        def neg2():
            fil3=File(Path(self.root + '/sub1'))
            assert not file3.is_file
        pos
        neg1
        neg2

    def test_create_file(self):
        file1 = File(self.root + '/tmp3.txt')
        touch(file1)
        assert file1.exists

    def test_delete_file(self):
        file1 = File(self.root + '/tmp2.txt')
        rm(file1)
        assert not file1.exists

    def test_copy_file(self):
        file1 = File(self.root + '/tmp2.txt')
        cp(file1,Path(self.root1+'/tmp2.txt'))
        file2 = File(self.root1+'/tmp2.txt')
        assert file2.exists and file1.exists

    def test_move_file(self):
        file1 = File(self.root + '/tmp2.txt')
        mv(file1,Path(self.root1+'/tmp2.txt'))
        file2 = File(self.root1+'/tmp2.txt')
        assert file2.exists and not file1.exists
