# python3 -m test.test
# test instantiate - error if exists
# 
import unittest
from src.python.instantiate import instantiate_db
import os
import hashlib
import uuid

class TestInstantiation(unittest.TestCase):
    def test_create(self):
        unique_id = uuid.uuid4()
        self.db_filename = str(unique_id)[:10] + ".sqlite"
        instantiate_db(self.db_filename)
        self.assertTrue(os.path.isfile(self.db_filename))
        
    def tearDown(self):
        os.remove(self.db_filename)

class TestInstantiation(unittest.TestCase):
    def test_create(self):
        unique_id = uuid.uuid4()
        self.db_filename = str(unique_id)[:10] + ".sqlite"
        instantiate_db(self.db_filename)
        self.assertTrue(os.path.isfile(self.db_filename))
        
    def tearDown(self):
        os.remove(self.db_filename)

if __name__ == '__main__':
    unittest.main()