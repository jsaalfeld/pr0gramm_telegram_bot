#!/usr/bin/python

import telegram
import sys
import pr0gramm
import ConfigParser


def main(argv):
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read('config.cfg')
	telegram_token = config.get('b0t', 'token')
	pr0gramm_username = config.get('b0t', 'username')
	pr0gramm_password = config.get('b0t', 'password')
	bot = telegram.Bot(token=telegram_token)
	print "I'm the " + bot.getMe().username
	updates = bot.getUpdates()
	for update in updates:
		print update.message.chat.id
		bot.sendMessage(chat_id=update.message.chat.id, text="lol")
	print [u.message.text for u in updates]


def print_help():
	print 'To start this bot you must pass 3 parameters'
	print 'your telegram token'
	print 'your pr0gramm username'
	print 'your pr0gramm password'


if __name__ == '__main__':
	main(sys.argv[1:])