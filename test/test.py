# python3 -m test.test
# test instantiate - error if exists
# 
import unittest
from src.python.instantiate import instantiate_db
from src.python.add_record import *
import os
import hashlib
import uuid
import sqlite3

class TestInstantiation(unittest.TestCase):
    # test creation of sqlite db
    def test_create(self):
        unique_id = uuid.uuid4()
        self.db_filename = str(unique_id)[:10] + ".sqlite"
        instantiate_db(self.db_filename)
        self.assertTrue(os.path.isfile(self.db_filename))
        
    def tearDown(self):
        os.remove(self.db_filename)

class TestTable(unittest.TestCase):
    # test creation of table with appropriate columns
    def setUp(self):
        unique_id = uuid.uuid4()
        self.db_filename = str(unique_id)[:10] + ".sqlite"
        instantiate_db(self.db_filename)

    def test_columns(self):
        connection = sqlite3.connect(self.db_filename)
        cursor = connection.execute('select * from simdata')
        names = list(map(lambda x: x[0], cursor.description))

        expected_columns = ["project",
                            "codename",
                            "path_to_source_code",
                            "path_to_executable",
                            "executable_version",
                            "executable_hash",
                            "run_timestamp",
                            "source_code_git_commit",
                            "path_to_input_file",
                            "input_file_hash",
                            "output_path_prefix",
                            "output_files",
                            "vis_output_prefix",
                            "vis_files",
                            "info",
                            "backup_paths",
                            "json_info"]
        for col in expected_columns:
            self.assertTrue(col in names)
        for col in names:
            self.assertTrue(col in expected_columns)
        
    def tearDown(self):
        os.remove(self.db_filename)

class GetInfo(unittest.TestCase):
    # get info about code, work with timestamps, etc
    def test_datetime_manip(self):

        with self.assertRaises(ValueError):
            check_and_correct_timestamp("22_12")
        
        dt_corrected = check_and_correct_timestamp("22_12_4")
        self.assertTrue(dt_corrected == "2022_12_04_00_00_00")
        
        dt_corrected = check_and_correct_timestamp("1992_12_4_17_44_23")
        self.assertTrue(dt_corrected == "1992_12_04_17_44_23")
        
        with self.assertRaises(ValueError):
            check_and_correct_timestamp("1992_12_4_37_44_23")
        with self.assertRaises(ValueError):
            check_and_correct_timestamp("1992_12_74_17_44_23")
        with self.assertRaises(ValueError):
            check_and_correct_timestamp("1992_22_4_07_44_23")
        with self.assertRaises(ValueError):
            check_and_correct_timestamp("1992_12_4_07_94_23")
        with self.assertRaises(ValueError):
            check_and_correct_timestamp("1992_12_4_07_14_93")

if __name__ == '__main__':
    unittest.main()