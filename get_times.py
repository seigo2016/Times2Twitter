import slack
import csv
import os
usertoken = os.getenv('SlackBtoken')
client = slack.WebClient(
    token=usertoken)

chlist = []


def channel_list(client):
    channels = client.api_call("channels.list")
    if channels['ok']:
        return channels['channels']
    else:
        return None


ret = channel_list(client)
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
