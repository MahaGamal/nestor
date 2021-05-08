from nestor import logging
from os import getenv
from time import sleep
from nestor.config.slack_client import SlackBot
from nestor.utils.proxy import Proxy
from nestor import logging as logger
import traceback

SLACK_PULL_RATE = float(getenv('SLACK_PULL_RATE', 0.3))

def run():
    try:
        bot = SlackBot()
    except Exception as err:
        logging.error(f'Failed to init slack bot.. \
        Shutting down.\nErr: {err}')
    else:
        bot.send_message('_starting..._')
        logger.info('_starting..._')
        proxy = Proxy()
        bot.send_message("*All right, I'm ready, ask me anything!*")
        while True:
            bot.connect()
            events = bot.read_messages()
            for event in events:
                try:
                    proxy.process_event(bot, event)
                except Exception as e:
                    logger.exception(e)
                    msg = f"{e.__class__.__name__}:{e} \n {traceback.format_exc()}"
                    bot.send_message(msg)
            sleep(SLACK_PULL_RATE)
