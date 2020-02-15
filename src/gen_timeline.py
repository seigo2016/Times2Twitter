from slack import RTMClient, WebClient
import csv
import os
import datetime
import configparser
from slackeventsapi import SlackEventAdapter
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(current_dir+'/token.ini')
slack_token = config.get("token", 'SlackBtoken')
web_client = WebClient(token=slack_token)
rtm_client = RTMClient(token=slack_token)
p = re.compile(r'^!leave$')
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
    try:
        ch, chinfo = get_chlist()
        data = payload['data']
        web_client = payload['web_client']
        msgch = data['channel']
        if 'user' in data and 'thread_ts' not in data:
            user = data['user']
            text = data['text']
            if chinfo[msgch] == user and msgch in ch:
                if p.match(text):
                    print(text)
                username = web_client.users_info(
                    token=slack_token,
                    user=user)['user']['profile']['display_name']
                iconurl = web_client.users_info(
                    token=slack_token,
                    user=user)['user']['profile']['image_512']
                msgchname = web_client.channels_info(token=slack_token, channel=msgch)['channel']['name']
                msgdate = datetime.date.fromtimestamp(int(float(data['ts'])))
                block = build_message(
                    username, text, iconurl, msgchname, msgdate)
                web_client.chat_postMessage(
                    token=slack_token,
                    channel="#times_all_tl",
                    unfurl_media=True,
                    unfurl_links=True,
                    blocks=block
                )
    except Exception as e:
        print(e)

def channel_list(client):
    channels = client.channels_list(token=slack_token)
    print(channels)
    if channels['ok']:
        return channels['channels']
    else:
        return None


@RTMClient.run_on(event="channel_joined")
def app_invited(**payload):
    chlist = []
    ret = channel_list(web_client)
    for i in ret:
        if i['name'].find("times_all_tl") is not -1:
            tlch = i
        elif i['name'].find("times") is not -1:
            chlist.append(i)
    with open(current_dir + '/channel.csv', 'w') as f:
        writer = csv.DictWriter(f, ['id', 'name', 'is_channel', 'created', 'creator', "is_archived", "is_general", "name_normalized", "is_shared",
        "is_org_shared", "is_member", "is_private", "is_mpim", "members", "topic", "purpose", "previous_names", "num_members", "unlinked",
        "pending_connected_team_ids", "is_ext_shared", "is_group", "pending_shared", "is_pending_ext_shared", "shared_team_ids", "parent_conversation", "is_im"])
        writer.writeheader()
        for i in chlist:
            writer.writerow(i)
    with open(current_dir + '/tl.csv', 'w') as f:
        writer = csv.DictWriter(f, ['id', 'name', 'is_channel', 'created', 'creator', "is_archived", "is_general", "name_normalized", "is_shared",
        "is_org_shared", "is_member", "is_private", "is_mpim", "members", "topic", "purpose", "previous_names", "num_members", "unlinked",
        "pending_connected_team_ids", "is_ext_shared", "is_group", "pending_shared", "is_pending_ext_shared", "shared_team_ids", "parent_conversation", "is_im"])
        writer.writeheader()
        writer.writerow(tlch)

def app_leave():

rtm_client.start()
