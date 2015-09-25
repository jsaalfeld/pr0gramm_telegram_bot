#!/usr/bin/python

import telegram
import sys
import pr0gramm
import ConfigParser
import datetime
import time


def main(argv):
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	configFileName = 'config.cfg'
	config.read(configFileName)
	configFile = open(configFileName,'w')
	telegram_token = config.get('b0t', 'token')
	pr0gramm_username = config.get('b0t', 'username')
	pr0gramm_password = config.get('b0t', 'password')
	bot = telegram.Bot(token=telegram_token)
	last_update =  datetime.datetime.fromtimestamp(int(config.get('b0t', 'lastupdate')))
	print "I'm the " + bot.getMe().username
	updates = bot.getUpdates()
	for update in updates:
		if update.message.date > last_update:
			print "This Message is new"
			if update.message.text.startswith("/"):
				if update.message.text == "/sfw_beliebt":
					sendTextMessage(bot,update.message.chat.id, "Hier kommt bald ihr foto")
					sendFirstImageFromSFWPopular(bot,update.message.chat.id)
				sendTextMessage(bot,update.message.chat.id,"Valid Command")
			else:
				sendTextMessage(bot,update.message.chat.id,telegram.Emoji.PILE_OF_POO)
			sendTextMessage(bot,update.message.chat.id,"")
		else:
			print "This Message is old"
	thisUpdate = updates[len(updates)-1].message.date
	config.set('b0t', 'lastupdate', int(time.mktime(thisUpdate.timetuple())))
	config.write(configFile)

def sendTextMessage(bot, chat_id, text):
	try:
		bot.sendMessage(chat_id=chat_id, text=text)
	except telegram.error.TelegramError, e:
		print e.message

def sendFirstImageFromSFWPopular(bot, chat_id):
	print "TODO"

if __name__ == '__main__':
	main(sys.argv[1:])