import os
import shutil
import tempfile
import unittest
import uuid


class RenameTest(unittest.TestCase):
    def setUp(self):
        dir_name = "bren_%s" % str(uuid.uuid1())
        self.tmpdir = os.path.join(tempfile.gettempdir(), dir_name)
        if not os.path.isdir(self.tmpdir):
            os.makedirs(self.tmpdir)
        for i in range(0, 3):
            tmp_file = "tmpfile_%s.jpg" % i
            open(os.path.join(self.tmpdir, tmp_file), 'a').close()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_tmp_files(self):
        self.assertEqual(len(os.listdir(self.tmpdir)), 3)
