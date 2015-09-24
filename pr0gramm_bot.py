#!/usr/bin/python

import telegram
import sys

def main():
	print("lol")
	if len(sys.argv) == 3:
		telegram_token = sys.argv[0]
		pr0gramm_username = sys.argv[1]
		pr0gramm_password = sys.argv[2]
		bot = telegram.bot(sys.argv[0])
	else:
		print_help()
def print_help():
	print 'To start this bot you must pass 3 parameters'
	print 'your telegram token'
	print 'your pr0gramm username'
	print 'your pr0gramm password'

if __name__ == '__main__':
	main()