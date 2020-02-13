from slack import RTMClient, WebClient
import csv
import os
import datetime
import configparser
from slackeventsapi import SlackEventAdapter

current_dir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(current_dir+'/token.ini')
usertoken = os.getenv('SlackUtoken')
slack_token = os.getenv('SlackBtoken')
# slack_token = config.get("token", 'SlackBtoken')
# usertoken = config.get("token", 'SlackUtoken')
webclient = WebClient(token=usertoken)
rtm_client = RTMClient(token=slack_token)
def get_chlist():
    chlist = []
    chinfo = {}
    with open(current_dir+"/channel.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chlist.append(row['id'])
            chinfo[row['id']] = row['creator']
    return chlist, chinfo


def build_message(username, text, imgurlpub, msgchname, msgdate):
    block = '[{"type":"divider"},{"type":"section","text":{"type":"mrkdwn","text":"*' + str(username) + '* \n' + str(text) + '"},"accessory":{"type":"image","image_url":"' + \
        str(imgurlpub) + \
        '","alt_text":"Image"}},{"type":"divider"},{"type": "context","elements": [{"type": "mrkdwn", "text": "#' + str(msgchname) + '  ' + str(
        msgdate) + '"}]}]'
    return block


@RTMClient.run_on(event="message")
def get_msg(**payload):
    ch, chinfo = get_chlist()
    data = payload['data']
    web_client = payload['web_client']
    msgch = data['channel']
    if 'user' in data and 'thread_ts' not in data:
        user = data['user']
        text = data['text']
        if chinfo[msgch] == user and msgch in ch:
            username = web_client.users_info(
                token=slack_token,
                user=user)['user']['profile']['display_name']
            iconurl = web_client.users_info(
                token=slack_token,
                user=user)['user']['profile']['image_512']
            msgchname = web_client.channels_info(token=slack_token, channel=msgch)[
                'channel']['name']
            msgdate = datetime.date.fromtimestamp(int(float(data['ts'])))
            block = build_message(
                username, text, iconurl, msgchname, msgdate)
            web_client.chat_postMessage(
                token=os.getenv('SlackBtoken'),
                channel="#times_all_tl",
                unfurl_media=True,
                unfurl_links=True,
                blocks=block
            )
    # except Exception as e:
    #     print(e)
    #     pass

def channel_list(client):
    channels = client.api_call("channels.list")
    if channels['ok']:
        return channels['channels']

@RTMClient.run_on(event="channel_joined")
def app_invited(**payload):
    chlist = []
    ret = channel_list(webclient)
    for i in ret:
        if i['name'].find("times_all_tl") is not -1:
            tlch = i
        elif i['name'].find("times") is not -1:
            chlist.append(i)
    with open('channel.csv', 'w') as f:
        writer = csv.DictWriter(f, ['id', 'name', 'is_channel', 'created',
                                    'is_archived', 'is_general', 'unlinked', 'creator', 'name_normalized', 'is_shared', 'is_org_shared', 'is_member', 'is_private', 'is_mpim', 'members', 'topic', 'purpose', 'previous_names', 'num_members'])
        writer.writeheader()
        for i in chlist:
            writer.writerow(i)
    with open('tl.csv', 'w') as f:
        writer = csv.DictWriter(f, ['id', 'name', 'is_channel', 'created',
                                    'is_archived', 'is_general', 'unlinked', 'creator', 'name_normalized', 'is_shared', 'is_org_shared', 'is_member', 'is_private', 'is_mpim', 'members', 'topic', 'purpose', 'previous_names', 'num_members'])
        writer.writeheader()
        writer.writerow(tlch)

rtm_client.start()
