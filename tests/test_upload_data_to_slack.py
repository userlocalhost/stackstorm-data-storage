import base64
import json
import mock
import os

from base import StorageBaseTestCase
from base import FakeResponse
from upload_data_to_slack import UploadDataToSlack
from upload_data_to_slack import TemporaryFile


class UploadDataToSlackTest(StorageBaseTestCase):
    __test__ = True
    action_cls = UploadDataToSlack

    @mock.patch('upload_data_to_slack.requests.post')
    def test_post_image_to_slack(self, mock_post):
        mock_post.return_value = FakeResponse(json.dumps({'ok': True}), 200)

        (is_success, resp_data) = self.get_action_instance().run(**{
            'data': 'hogefuga',
            'channel': '#general',
            'token': 'test-token',
        })
        self.assertTrue(is_success)
        self.assertTrue(resp_data['ok'])

    @mock.patch('upload_data_to_slack.requests.post')
    def test_post_image_to_slack_with_failure(self, mock_post):
        mock_post.return_value = FakeResponse('Some messages', 400)

        (is_success, resp_data) = self.get_action_instance().run(**{
            'data': 'hogefuga',
            'channel': '#general',
            'token': 'test-token',
        })
        self.assertFalse(is_success)
        self.assertEqual(resp_data, 'Some messages')

    def test_post_image_to_slack_without_token(self):
        (is_success, resp_data) = self.get_action_instance().run(**{
            'data': 'hogefuga',
            'channel': '#general',
        })
        self.assertFalse(is_success)
        self.assertEqual(resp_data, 'Failed to get slack access token')

    def test_temprary_file(self):
        data = base64.b64encode('hogefuga')

        with TemporaryFile(data, '.txt') as filepath:
            self.assertTrue(os.path.exists(filepath))
            self.assertEqual(filepath[-4:], '.txt')
            self.assertEqual(open(filepath, 'r').read(), 'hogefuga')

        # This confirms that file of filepath would be deleted outside of with statement
        self.assertFalse(os.path.exists(filepath))
