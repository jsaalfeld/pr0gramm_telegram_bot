#!/usr/bin/python

import telegram
import configparser
import pr0grammapi

LAST_UPDATE_ID = None


# TODO: refactor this bot to an class for more flexibility
def main():
    global LAST_UPDATE_ID

    config = configparser.RawConfigParser(allow_no_value=True)
    config_file_name = 'config.cfg'
    config.read(config_file_name)
    telegram_token = config.get('b0t', 'token')

    api = pr0grammapi.Pr0grammAPI(config.get('b0t', 'username'), config.get('b0t', 'password'))
    bot = telegram.Bot(token=telegram_token)

    # try to get latest update id
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        run(bot, api)


def run(bot, api):
    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        text = update.message.text
        chat_id = update.message.chat_id

        print(text)

        if text.startswith('/'):
            if text == '/sfw_beliebt':
                bot.sendChatAction(chat_id=chat_id, action='upload_photo')
                data = api.get_new_sfw_image()
                bot.sendMessage(chat_id=chat_id, text=data['image'])

        LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()
