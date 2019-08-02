import mock

from base import StorageBaseTestCase
from get_st2kv import GetKV


class GetKVTest(StorageBaseTestCase):
    __test__ = True
    action_cls = GetKV

    @mock.patch('get_st2kv.Client')
    def test_run_action(self, mock_client):
        # Preparing for mock processing to check that action calls expected methods correctly
        mock_resp = mock.Mock()
        mock_resp.serialize.return_value = 'hogefuga'

        mock_client_object = mock.Mock()
        mock_client_object.keys.get_by_id.return_value = mock_resp
        mock_client.return_value = mock_client_object

        # Making an action and run it
        (is_success, resp_data) = self.get_action_instance().run(key='key')

        # This checks that action calls expected method
        self.assertTrue(is_success)
        self.assertEqual(resp_data, 'hogefuga')
