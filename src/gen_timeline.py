from slack import RTMClient, WebClient
import csv
import os
import datetime
import configparser
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
slack_token = os.getenv('SlackBtoken')
web_client = WebClient(token=slack_token)
rtm_client = RTMClient(token=slack_token)
# disp = re.compile(r'^!disable$')
mention_pattern = re.compile(r'(<@\w+>|<!here>|<!channel>|<!everyone>)')

def build_message(send_data):
    user_name = send_data['user_name']
    text = send_data['text']
    icon_url = send_data['icon_url']
    message_channel_name = send_data['message_channel_name']
    message_send_date = send_data['message_send_date']
    block = '[{"type":"divider"},{"type":"section","text":{"type":"mrkdwn","text":"*' + str(user_name) + '* \n' + str(text) + '"},"accessory":{"type":"image","image_url":"' + \
        str(icon_url) + \
        '","alt_text":"Image"}},{"type":"divider"},{"type": "context","elements": [{"type": "mrkdwn", "text": "#' + str(message_channel_name) + '  ' + str(
        message_send_date) + '"}]}]'
    return block


# def disable_app(msgch):
#     pass

def get_user_info(client, user_id):
    user_name = client.users_info(token=slack_token,user=user_id)['user']['profile']['display_name']
    return user_name

def get_user_icon(client, user_id):
    icon_url = web_client.users_info(token=slack_token, user=user_id)['user']['profile']['image_512']
    return icon_url

def get_channel_info(client, channel_id):
    # channels = client.channels_list(token=slack_token)
    channel_info = client.conversations_info(token=slack_token, channel=channel_id)
    if channel_info['ok']:
        return channel_info['channel']
    else:
        return None

@RTMClient.run_on(event="message")
def get_msg(**payload):
    try:
        received_data = payload['data']
        web_client = payload['web_client']
        msgch = received_data['channel']
        channel_info = get_channel_info(web_client, msgch)
        if channel_info:
            send_data={}
            user_id = received_data['user']
            if channel_info['creator'] == user_id and 'times' in channel_info['name'] and not 'times_all_tl' in channel_info:
                send_data['text'] = re.sub(mention_pattern, '', received_data['text'])
                if send_data['text']:
                    print(send_data['text'])
                    send_data['user_name'] = get_user_info(web_client, user_id)
                    send_data['icon_url'] = get_user_icon(web_client, user_id)
                    send_data['message_channel_name'] = channel_info['name']
                    send_data['message_send_date'] = datetime.date.fromtimestamp(int(float(received_data['ts'])))
                    block = build_message(send_data)                
                    print(block)
                    web_client.chat_postMessage(
                        token=slack_token,
                        channel="#times_all_tl",
                        unfurl_media=True,
                        unfurl_links=True,
                        blocks=block
                    )
    except Exception as e:
        print(e)

rtm_client.start()
