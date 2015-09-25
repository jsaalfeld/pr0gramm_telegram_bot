import os
from urllib.parse import urlparse
import requests
import telegram
import time
from pr0gramm.api import Pr0grammAPI


class Pr0grammBot:
    def __init__(self, config):
        self.__api = Pr0grammAPI(username=config.get('b0t', 'username'),
                                 password=config.get('b0t', 'password'),
                                 tmp_dir=config.get('b0t', 'tmp_dir'))
        self.__bot = telegram.Bot(token=config.get('b0t', 'token'))
        self.__tmp_dir = config.get('b0t', 'tmp_dir')
        self.__tmp_image = ''

        # available commands with their corresponding bot method
        # scope the with __ so they are mangled by python
        self.available_commands = {
            'sfw_beliebt': '__send_top_sfw_image'
        }

        self.__api.login()

        # try to get latest update id
        try:
            self.__LAST_UPDATE_ID = self.__bot.getUpdates()[-1].update_id
        except IndexError:
            self.__LAST_UPDATE_ID = None

    def __download_tmp_image(self, url):
        r = requests.get(url, stream=True)

        ext = os.path.splitext(urlparse(url).path)[1]

        if r.status_code == 200:
            self.__tmp_image = os.path.join(self.__tmp_dir, str(int(time.time())) + ext)
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
                os.remove(self.__tmp_image)
                self.__tmp_image = ''
            except AttributeError:
                print("could not call method", self.available_commands[text])

    def __send_top_sfw_image(self, chat_id):
        self.__bot.sendChatAction(chat_id=chat_id, action='upload_photo')
        data = self.__api.get_top_sfw_image()

        self.__download_tmp_image(data['image'])
        if self.__tmp_image is not '':
            with open(self.__tmp_image, 'rb') as img:
                # TODO add caption -> tags, up and downvotes
                self.__bot.sendPhoto(chat_id=chat_id, photo=img)

    def run(self):
        for update in self.__bot.getUpdates(offset=self.__LAST_UPDATE_ID, timeout=10):
                self.__parse_message(update)

                # update last update id to make sure we mark messages as completed on telegram servers
                self.__LAST_UPDATE_ID = update.update_id + 1
