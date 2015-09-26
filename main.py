#!/usr/bin/python

import configparser
import logging
import os
from pr0gramm.bot import Pr0grammBot

log = logging.getLogger('pr0Bot.main')


def main():
    logging.basicConfig(level=logging.INFO)
    log.info('Starting up pr0gramm bot...')

    log.info('Reading config file...')
    config = configparser.RawConfigParser(allow_no_value=True)
    config_file_name = 'config.cfg'
    read_files = config.read(config_file_name)

    if not read_files:
        log.critical('No config file found. Exit!')
        exit(1)

    if not os.path.exists(config.get('b0t', 'tmp_dir')):
        try:
            os.makedirs(config.get('b0t', 'tmp_dir'))
            raise OSError
        except OSError as e:
            log.critical('Could not create tmp directory %s', e)
            exit(1)

    if not os.access(config.get('b0t', 'tmp_dir'), os.W_OK):
        log.warn('Temporary directory (%s) is not writable', config.get('b0t', 'tmp_dir'))

    bot = Pr0grammBot(config)

    while True:
        bot.run()


if __name__ == '__main__':
    main()
