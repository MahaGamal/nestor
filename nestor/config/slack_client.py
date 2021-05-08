import os
from time import sleep 
from slackclient import SlackClient
from nestor import logging

SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

GROUPS_SLACK_TOKEN = os.environ.get('GROUPS_SLACK_TOKEN')
SLACK_GROUP_ID = os.environ.get('SLACK_GROUP_ID')

class SlackBot():
    def __init__(self):
        self.slack_client = SlackClient(SLACK_TOKEN)
        self.connect() or exit(1)
        self.name = self.slack_client.server.username
        self.id = self.slack_client.server.users.find(self.name).id
        logging.info("Bot name: %s\nBot id: %s" % (self.name, self.id))
        self.channel = self.slack_client.server.channels.find(SLACK_CHANNEL)
        
        logging.info("Allowed channel: %s" % str(self.channel))

    def connect(self):
        if self.connected():
            return True
        for i in range(5):
            logging.info("Attempting to connect to slack")
            if self.slack_client.rtm_connect():
                logging.info("Connected to slack")
                return True
            else:
                logging.warn("Failed to connect to slack")
                sleep(3)
        return False

    def connected(self):
        return self.slack_client.server.connected

    def is_private(self, channel):
        """Checks if on a private slack channel"""
        return True if self.id == channel else False

    def read_messages(self):
        events = self.slack_client.rtm_read()
        return events
   
    def send_message(self, text, channel=None):
        channel = self.channel.id
        self.slack_client.rtm_send_message(channel=channel, message=str(text))

    def get_users(self):
        users = self.slack_client.api_call('users.list')
        return users

    def update_usergroup(self, user_ids):
        logging.info('Updating user group to %s', user_ids)
        self.slack_client.api_call('usergroups.users.update?token={0}&usergroup={1}&users={2}'.format(
                                                                                                    GROUPS_SLACK_TOKEN,
                                                                                                    SLACK_GROUP_ID,
                                                                                                    ','.join(user_ids)))
    