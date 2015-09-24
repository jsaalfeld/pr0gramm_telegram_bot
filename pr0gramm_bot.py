#!/usr/bin/python

import telegram
import sys
import pr0gramm

def main(argv):
	print str(argv)
	if len(argv) == 3:
		telegram_token = argv[0]
		pr0gramm_username = argv[1]
		pr0gramm_password = argv[2]
		bot = telegram.Bot(token=telegram_token)
		print bot.getMe()
	else:
		print_help()
def print_help():
	print 'To start this bot you must pass 3 parameters'
	print 'your telegram token'
	print 'your pr0gramm username'
	print 'your pr0gramm password'

if __name__ == '__main__':
	main(sys.argv[1:])