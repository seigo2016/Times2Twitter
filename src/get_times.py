from slack import WebClient, RTMClient
import csv
import os
import configparser
# current_dir = os.path.dirname(os.path.abspath(__file__))
# config = configparser.ConfigParser()
# config.read(current_dir+'/dev_token.ini')
slack_token = os.getenv('SlackBtoken')
web_client = WebClient(token=slack_token)
rtm_client = RTMClient(token=slack_token)
chlist = []


def channel_list(client):
    channels = client.channels_list(token=slack_token)
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
