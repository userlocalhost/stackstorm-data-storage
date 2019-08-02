import os

from st2tests.base import BaseActionTestCase


class StorageBaseTestCase(BaseActionTestCase):
    def setUp(self):
        super(StorageBaseTestCase, self).setUp()

        # clear property values which might be set at any tests
        self.kv_pair = None

        # set environment variables which is set in a StackStorm node by default
        os.environ['ST2_API_URL'] = 'http://localhost/api/v1'
