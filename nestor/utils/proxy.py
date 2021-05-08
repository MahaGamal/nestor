from nestor import logging as logger
from nestor.utils.custom_error import HelpException


class Proxy():

    def process_event(self, slackBot, event):
        print("Starting .....", event)

        channel = event.get('channel')
        message = event.get('text')
        user = event.get('user')
        # filter out slack events that are not for us
        if message is None or not message.startswith((slackBot.name, f'<@{slackBot.id}>')):
            return

        logger.info(f'Nestor Message : {str(message)}')
        # make sure our bot is only called for a specified channel
        if channel is None or channel != slackBot.channel.id :
            slackBot.send_message(f'<@{user}> I only run tasks asked from `{slackBot.name}` channel')
            return

        # remove bot name and extract command
        if message.startswith(f'<@{slackBot.id}>'):
            cmd = message.split(f'<@{slackBot.id}>')[1]
            if cmd.startswith(':'):
                cmd = cmd[2:]
            cmd = cmd.strip()
        else:
            cmd = message.split(f'{slackBot.name}')[1]
        # process command
        try:
            pass
        except HelpException:
            pass
