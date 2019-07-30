import os

from st2client.client import Client
from st2client.models import KeyValuePair
from st2common.runners.base_action import Action


class SetKV(Action):
    def run(self, key, value, **kwargs):
        client = Client(api_url=os.environ['ST2_API_URL'])

        # Store value to datastore
        kv_pair = client.keys.update(KeyValuePair(name=key, value=value, **kwargs))

        return (True, kv_pair.serialize())
