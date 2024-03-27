# python3 -m test.test
# test instantiate - error if exists
# 
import unittest
from src.python.instantiate import instantiate_db
import os
import hashlib
import uuid
import sqlite3

class TestInstantiation(unittest.TestCase):
    def test_create(self):
        unique_id = uuid.uuid4()
        self.db_filename = str(unique_id)[:10] + ".sqlite"
        instantiate_db(self.db_filename)
        self.assertTrue(os.path.isfile(self.db_filename))
        
    def tearDown(self):
        os.remove(self.db_filename)

class TestTable(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()