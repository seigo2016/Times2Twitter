from slack import WebClient, RTMClient
import csv
import os
import configparser
current_dir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(current_dir+'/token.ini')
usertoken = os.getenv('SlackUtoken')
slack_token = os.getenv('SlackBtoken')
# slack_token = config.get("token", 'SlackBtoken')
# usertoken = config.get("token", 'SlackUtoken')
web_client = WebClient(token=usertoken)
rtm_client = RTMClient(token=slack_token)
chlist = []


def channel_list(client):
    channels = client.api_call("channels.list")
    if channels['ok']:
        return channels['channels']
    else:
        return None


ret = channel_list(web_client)
for i in ret:
    if i['name'].find("times_all_tl") is not -1:
        tlch = i
    elif i['name'].find("times") is not -1:
        chlist.append(i)

with open(current_dir + '/channel.csv', 'w') as f:
    writer = csv.DictWriter(f, ['id', 'name', 'is_channel', 'created',
                                'is_archived', 'is_general', 'unlinked', 'creator', 'name_normalized', 'is_shared', 'is_org_shared', 'is_member', 'is_private', 'is_mpim', 'members', 'topic', 'purpose', 'previous_names', 'num_members'])
    writer.writeheader()
    for i in chlist:
        writer.writerow(i)
with open(current_dir + '/tl.csv', 'w') as f:
    writer = csv.DictWriter(f, ['id', 'name', 'is_channel', 'created',
                                'is_archived', 'is_general', 'unlinked', 'creator', 'name_normalized', 'is_shared', 'is_org_shared', 'is_member', 'is_private', 'is_mpim', 'members', 'topic', 'purpose', 'previous_names', 'num_members'])
    writer.writeheader()
    writer.writerow(tlch)
