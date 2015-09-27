#!/usr/bin/env python

from pr0gramm.bot import Pr0grammBot
from pr0gramm.bot import Pr0grammAPI
import unittest
import configparser
import telegram
import os

class TestStringMethods(unittest.TestCase):
	def test_get_image(self):
		config = configparser.RawConfigParser(allow_no_value=True)
		config_file_name = 'config.cfg'
		config.read(config_file_name)
		'''
		bot = Pr0grammBot(config)
		if not os.path.exists(config.get('b0t', 'tmp_dir')):
			os.makedirs(config.get('b0t', 'tmp_dir'))
		'''
		api = Pr0grammAPI(username=config.get('b0t', 'username'),
		                  password=config.get('b0t', 'password'),
		                  tmp_dir=config.get('b0t', 'tmp_dir'))
		self.assertIn('http://img.pr0gramm.com', api.get_top_image(1)['image'])

	#Works just lokally with valid token
	'''
	def test_bot_signing(self):
		config = configparser.RawConfigParser(allow_no_value=True)
		config_file_name = 'config.cfg'
		config.read(config_file_name)
		bot = telegram.Bot(token=config.get('b0t', 'token'))
		self.assertEqual(bot.getMe().username, 'der_pr0gramm_bot')
	'''

if __name__ == '__main__':
	unittest.main()
