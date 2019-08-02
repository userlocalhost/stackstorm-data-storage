import base64
import os
import random
import string
import requests

from st2common.runners.base_action import Action


class UploadDataToSlack(Action):
    CONFIG_KEY_SLACK_TOKEN = 'slack_token'
    SLACK_API_ENDPOINT_URL = 'https://slack.com/api/files.upload'

    def run(self, data, channel, token=None, title='', text='', file_extension='.png'):
        # Get an acess token of Slack from configuration when it's not specified in parameter
        if not token and self.CONFIG_KEY_SLACK_TOKEN in self.config:
            token = self.config[self.CONFIG_KEY_SLACK_TOKEN]

        if not token:
            return (False, 'Failed to get slack access token')

        # call Slack API to upload file to the specified Slack channel
        with TemporaryFile(data, file_extension) as filepath:
            with open(filepath, 'rb') as fp:
                resp = requests.post(url=self.SLACK_API_ENDPOINT_URL, params={
                    'token': token,
                    'channels': channel,
                    'title': title,
                    'initial_comment': text,
                }, files={'file': fp})

        if 200 <= resp.status_code <= 299:
            return (True, resp.json())
        else:
            return (False, resp.content)


class TemporaryFile(object):
    SAVING_DIRECTORY = '/tmp'

    def __init__(self, data, file_extension):
        # generate filepath which is named randomly
        self.filepath = (
            '%s/%s%s' % (self.SAVING_DIRECTORY,
                         ''.join(random.choice(string.ascii_lowercase) for _ in range(10)),
                         file_extension))
        self.data = data

    def __enter__(self):
        with open(self.filepath, 'wb') as fp:
            fp.write(base64.b64decode(self.data))

        return self.filepath

    def __exit__(self, *args, **kwargs):
        # close and remove a generated file
        os.remove(self.filepath)
