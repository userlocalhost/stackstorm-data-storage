# stackstorm-data-storage

[![CircleCI](https://circleci.com/gh/userlocalhost/stackstorm-data-storage.svg?style=svg)](https://circleci.com/gh/userlocalhost/stackstorm-data-storage)

This is an automation pack to be able to store freely-selected typed data and retrieve it via a predetermined communication channel (like Slack).
This picture describes summary of the functionalities that this pack provides.

![system summary](https://raw.githubusercontent.com/userlocalhost/stackstorm-data-storage/docs/images/system_summary.png)

## Rule

| Rule | Description |
|:---- |:----------- |
| save_data_into_datastore | Create a webhook API to be able to save uploaded data into datastore<br/> (This is equivalent to (1) and (2) processing in the beginning picture) |

## Action / Workflow

| Action | Description |
|:------ |:----------- |
| show_image_to_slack | Upload image data which is stored in the datastore to Slack<br/> (This is equivalent to (3) and (4) processing in the beginning picture) |

# Setup

You can install and setup running environment as below.
```
$ st2 pack install https://github.com/userlocalhost/stackstorm-data-storage.git
$ st2 run packs.setup_virtualenv packs=data_storage
```

## Installing depending pack

This pack depends on [st2](https://github.com/StackStorm-Exchange/stackstorm-st2) pack. So it's necessary to install that pack like this.

```
$ st2 pack install st2
```

## Configuration

To post image data to Slack, you have to set slack_token which is dispatched by [the configuration of Slack Apps](https://slack.com/apps/manage).

When you want to register it on a system-wide basis, you can set it through "st2 pack config" command as below.
```
$ st2 pack config data_storage
```

Then, st2 pack configure utility asks you for typing the access_token to use. In this case, the registered value could be seen by everyone who could see the StackStorm configurations which are stored in `/opt/stackstorm/configs`.

Otherwise, you can register the access_token using datastore as below. In this case, nobody can see and use this value except for you.
```
$ st2 key set --scope user --encrypt slack_token "${SLACK_TOKEN_VALUE}"
```

# Example of use

This describes an example way to use the functions which this pack provides.

## (1) Uploading an image to the datastore via calling Webhook

![qr_picture.png](https://raw.githubusercontent.com/userlocalhost/stackstorm-data-storage/docs/images/qr_picture.png)

After saving above image as `qr_picture.png`, you can upload it to the StackStorm by calling webhook API as below.
```
FILEPATH='./qr_picture.png'
SENDING_DATA=$(jq -n --arg filename "wifiqr_201909" \
                     --arg filedata "$(base64 ${FILEPATH} | tr -d '\n')" \
                     '{key: $filename, data: $filedata}')

curl -X POST http://localhost:9101/v1/webhooks/save_data_into_datastore \
     -H "Content-Type: application/json" \
     --data "${SENDING_DATA}"
```

Then, uploaded image would be stored in the datastore with specified key-name.

## (2) Post stored image to slack

You can post stored image file to any specified Slack channels, in the range of the permission of the account which is associated with the slack_token, by calling `show_image_to_slack` workflow as below.

```
$ st2 run data_storage.show_image_to_slack key='wifiqr_201909' channel='#fuga' title="posting image title" text="hoge"
```

Then, you could see a new post that shows the example image on a specified channel by the account you configured, like this.

![example of executing show_image_to_slack workflow](https://raw.githubusercontent.com/userlocalhost/stackstorm-data-storage/docs/images/ss_example.png)
