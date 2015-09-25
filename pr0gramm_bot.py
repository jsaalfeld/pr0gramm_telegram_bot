#!/usr/bin/python

import telegram
import configparser

LAST_UPDATE_ID = None


def main():
    global LAST_UPDATE_ID

    config = configparser.RawConfigParser(allow_no_value=True)
    config_file_name = 'config.cfg'
    config.read(config_file_name)
    telegram_token = config.get('b0t', 'token')

    bot = telegram.Bot(token=telegram_token)

    # try to get latest update id
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        run(bot)


def run(bot):
    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        print(update.message.text)
        LAST_UPDATE_ID += 1


if __name__ == '__main__':
    main()
