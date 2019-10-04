from slack import RTMClient, WebClient
import csv
import os
import datetime
usertoken = os.getenv('SlackUtoken')
webclient = WebClient(token=usertoken)


def get_chlist():
    chlist = []
    chinfo = {}
    with open("channel.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chlist.append(row['id'])
            chinfo[row['id']] = row['creator']
    return chlist, chinfo


@RTMClient.run_on(event="message")
def get_msg(**payload):
    ch, chinfo = get_chlist()
    data = payload['data']
    web_client = payload['web_client']
    msgch = data['channel']
    if 'user' in data:
        text = data['text']
        user = data['user']
        if chinfo[msgch] == user and msgch in ch:
            username = web_client.users_info(
                token=slack_token,
                user=user)['user']['profile']['display_name']
            msgchname = web_client.channels_info(token=slack_token, channel=msgch)[
                'channel']['name']
            msgdate = datetime.date.fromtimestamp(int(float(data['ts'])))
            if 'files' in data:
                imgurl = webclient.files_sharedPublicURL(
                    token=usertoken,
                    file=data['files'][0]['id'])
                imgsec = imgurl['file']['permalink_public'].split('-')[3]
                imgurlpub = imgurl['file']['url_private'] + \
                    "?pub_secret=" + imgsec
                block = '[{"type":"divider"},{"type":"section","text":{"type":"mrkdwn","text":"*' + str(username) + '* \n' + str(text) + '"},"accessory":{"type":"image","image_url":"' + \
                    str(imgurlpub) + \
                    '","alt_text":"Image"}},{"type":"divider"},{"type": "context","elements": [{"type": "mrkdwn", "text": "#' + str(msgchname) + '  ' + str(
                        msgdate) + '"}]}]'
            else:
                block = '[{"type":"divider"},{"type":"section","text":{"type":"mrkdwn","text":"*' + \
                    str(username) + "*\n" + str(text) + \
                    '"}},{"type":"divider"},{"type": "context","elements": [{"type": "mrkdwn", "text": "#' + str(msgchname) + '  ' + str(
                        msgdate) + '"}]}]'
            web_client.chat_postMessage(
                token=os.getenv('SlackBtoken'),
                channel="#times_all_tl",
                unfurl_media=True,
                unfurl_links=True,
                blocks=block
            )


slack_token = os.getenv('SlackBtoken')
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
