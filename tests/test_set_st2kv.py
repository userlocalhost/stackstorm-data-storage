import mock

from base import StorageBaseTestCase
from set_st2kv import SetKV
from st2client.models import KeyValuePair


class SetKVTest(StorageBaseTestCase):
    __test__ = True
    action_cls = SetKV

    @mock.patch('set_st2kv.Client')
    def test_run_action(self, mock_client):
        def side_effect(kv_pair):
            mock_resp = mock.Mock()
            mock_resp.serialize.return_value = 'hogefuga'

            # store specified value to check
            self.kv_pair = kv_pair

            return mock_resp

        mock_client_object = mock.Mock()
        mock_client_object.keys.update.side_effect = side_effect
        mock_client.return_value = mock_client_object

        # Making an action and run it
        (is_success, resp_data) = self.get_action_instance().run(key='key', value='value', ttl=10)

        # This checks that action calls expected method
        self.assertTrue(is_success)
        self.assertEqual(resp_data, 'hogefuga')

        # This checks that action makes KeyValuePiar object with expected parameters
        self.assertIsInstance(self.kv_pair, KeyValuePair)
        self.assertEqual(self.kv_pair.name, 'key')
        self.assertEqual(self.kv_pair.value, 'value')
        self.assertEqual(self.kv_pair.ttl, 10)
