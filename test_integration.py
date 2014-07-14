import os
import shutil
import unittest

import brickowl2rebrickable
import low_level

TEMP_DIR = 'temp'
COMPARISON_DIR = 'golden_master'

class TestIntegration(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEMP_DIR):
           shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)

    def test(self):
        orders = ['5121927', '6284979', '8817894', '8827569']

        brickowl2rebrickable.brickowl2rebrickable(None, orders, output_dir=TEMP_DIR)

        for file in os.listdir(COMPARISON_DIR):
            file = os.path.join(COMPARISON_DIR, file)
            new_file = os.path.join(TEMP_DIR, os.path.split(file)[1])
            new_md5 = low_level.md5sum_file(new_file)
            old_md5 = low_level.md5sum_file(file)
            self.assertEqual(new_md5, old_md5, "{0} and {1} are not equal".format(file, new_file))

    def tearDown(self):
        if os.path.exists(TEMP_DIR):
           shutil.rmtree(TEMP_DIR)