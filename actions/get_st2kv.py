import os

from st2client.client import Client
from st2common.runners.base_action import Action


class GetKV(Action):
    def run(self, key, **kwargs):
        client = Client(api_url=os.environ['ST2_API_URL'])

        # Retrieve value from datastore
        kv_pair = client.keys.get_by_id(key, params=kwargs)

        return (True, kv_pair.serialize())
