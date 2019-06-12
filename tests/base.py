import os
import tempfile
import unittest

from app import create_app


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({
            'WTF_CSRF_ENABLED': False,
            'DEBUG': False,
            'TESTING': True,
            'DATABASE': self.db_path,
        })
        self.app.secret_key = 'shhhh'
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
