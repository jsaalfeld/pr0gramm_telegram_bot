import logging
import os
import requests
import telegram
import time
from pr0gramm.api import Pr0grammAPI

log = logging.getLogger('pr0Bot.bot')


class Pr0grammBot:
    def __init__(self, config):
        self.__api = Pr0grammAPI(username=config.get('b0t', 'username'),
                                 password=config.get('b0t', 'password'),
                                 tmp_dir=config.get('b0t', 'tmp_dir'))
        self.__bot = telegram.Bot(token=config.get('b0t', 'token'))
        self.__tmp_dir = config.get('b0t', 'tmp_dir')
        self.__tmp_image = ''
        # already downloaded and send files. sorted by flag.
        #  if we get an new image for an flag the old one will be replaced
        self.__cache = {}

        # available commands with their corresponding bot method
        # scope the with __ so they are mangled by python
        self.available_commands = {
            'sfw_beliebt': '__send_top_sfw_image',
            'nsfw_beliebt': '__send_top_nsfw_image',
            'nsfl_beliebt': '__send_top_nsfl_image'
        }
        log.info('Available commands: %s', self.available_commands.keys())

        self.__api.login()
        # try to get latest update id
        try:
            log.debug('Trying to get latest update ID from telegram API')
            self.__LAST_UPDATE_ID = self.__bot.getUpdates()[-1].update_id
        except IndexError:
            self.__LAST_UPDATE_ID = None

        log.debug('Latest update ID: %s', self.__LAST_UPDATE_ID)

    def __image_is_cached(self, data):
        if data['flag'] not in self.__cache:
            return False

        if data['id'] == self.__cache[data['flag']]['p_id']:
            return True

        return False

    def __download_tmp_image(self, data):
        if self.__image_is_cached(data):
            return

        r = requests.get(data['image'], stream=True)

        if r.status_code == 200:
            self.__tmp_image = os.path.join(self.__tmp_dir, str(int(time.time())) + data['image_ext'])
            with open(self.__tmp_image, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    def __parse_message(self, update):
        text = update.message.text
        chat_id = update.message.chat_id

        print(text)

        if not text.startswith('/'):
            return

        # strip / from command for automatic command calls
        text = text[1:]

        if text in self.available_commands:
            try:
                getattr(self, '_' + self.__class__.__name__ + self.available_commands[text])(chat_id)

                # clean up send image
                if os.path.isfile(self.__tmp_image):
                    os.remove(self.__tmp_image)
                self.__tmp_image = ''
            except AttributeError:
                print("could not call method", self.available_commands[text])

    def __send_image(self, chat_id, data):
        try:
            if not self.__image_is_cached(data):
                f = open(self.__tmp_image, 'rb')
            else:
                f = self.__cache[data['flag']]['t_id']

            # TODO add caption -> tags, up and downvotes
            if data['image_ext'] == '.webm' or data['image_ext'] == '.gif':
                # TODO convert webm to mp4
                file_id = self.__bot.sendDocument(chat_id=chat_id, document=f).document.file_id
            else:
                file_id = self.__bot.sendPhoto(chat_id=chat_id, photo=f).photo[-1].file_id

            if not self.__image_is_cached(data):
                self.__cache[data['flag']] = {}
                self.__cache[data['flag']]['p_id'] = data['id']
                self.__cache[data['flag']]['t_id'] = file_id
                f.close()

            return
        except telegram.TelegramError as e:
            print(e)
        except IOError as e:
            print(e)
        except AttributeError:
            print('could not obtain file id')

        self.__bot.sendMessage(chat_id=chat_id, text='Whoops. ¯\_(ツ)_/¯')

    def __send_top_sfw_image(self, chat_id):
        self.__bot.sendChatAction(chat_id=chat_id, action='upload_photo')
        data = self.__api.get_top_image(1)
        self.__download_tmp_image(data)
        self.__send_image(chat_id=chat_id, data=data)

    def __send_top_nsfw_image(self, chat_id):
        self.__bot.sendChatAction(chat_id=chat_id, action='upload_photo')
        data = self.__api.get_top_image(2)
        self.__download_tmp_image(data)
        self.__send_image(chat_id=chat_id, data=data)

    def __send_top_nsfl_image(self, chat_id):
        self.__bot.sendChatAction(chat_id=chat_id, action='upload_photo')
        data = self.__api.get_top_image(4)
        self.__download_tmp_image(data)
        self.__send_image(chat_id=chat_id, data=data)

    def run(self):
        for update in self.__bot.getUpdates(offset=self.__LAST_UPDATE_ID, timeout=10):
            self.__parse_message(update)

            # update last update id to make sure we mark messages as completed on telegram servers
            self.__LAST_UPDATE_ID = update.update_id + 1
