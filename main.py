#!/usr/bin/python

import configparser
import os
from pr0gramm.bot import Pr0grammBot


def main():
    config = configparser.RawConfigParser(allow_no_value=True)
    config_file_name = 'config.cfg'
    config.read(config_file_name)

    if not os.path.exists(config.get('b0t', 'tmp_dir')):
        os.makedirs(config.get('b0t', 'tmp_dir'))

    bot = Pr0grammBot(config)

    while True:
        bot.run()


if __name__ == '__main__':
    main()
