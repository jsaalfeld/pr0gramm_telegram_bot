import telegram
from pr0grammapi import Pr0grammAPI


class Pr0grammBot:
    def __init__(self, config):
        self.__api = Pr0grammAPI(config.get('b0t', 'username'), config.get('b0t', 'password'))
        self.__bot = telegram.Bot(token=config.get('b0t', 'token'))

        # available commands with their corresponding bot method
        self.available_commands = {
            'sfw_beliebt': '_send_top_sfw_image'
        }

        # try to get latest update id
        try:
            self.__LAST_UPDATE_ID = self.__bot.getUpdates()[-1].update_id
        except IndexError:
            self.__LAST_UPDATE_ID = None

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
                getattr(self, self.available_commands[text])(chat_id)
            except AttributeError:
                print("could not call method", self.available_commands[text])

    def __send_top_sfw_image(self, chat_id):
        self.__bot.sendChatAction(chat_id=chat_id, action='upload_photo')
        data = self.__api.get_new_sfw_image()

        # TODO download photo temporally and send the image
        self.__bot.sendMessage(chat_id=chat_id, text=data['image'])

    def run(self):
        for update in self.__bot.getUpdates(offset=self.__LAST_UPDATE_ID, timeout=10):
                self.__parse_message(update)

                # update last update id to make sure we mark messages as completed on telegram servers
                self.__LAST_UPDATE_ID = update.update_id + 1
