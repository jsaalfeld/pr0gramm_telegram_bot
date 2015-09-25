import json
import os
import requests


class Pr0grammAPI:
    def __init__(self, username, password, tmp_dir):
        self.__password = password
        self.__username = username
        self.__login_cookie = None

        self.tmp_dir = tmp_dir

        self.image_url = 'http://img.pr0gramm.com/'
        self.api_url = 'http://pr0gramm.com/api/'
        self.login_url = self.api_url + 'user/login/'
        self.items_url = self.api_url + 'items/get'
        self.item_url = self.api_url + 'items/info'

    def login(self):
        cookie_path = os.path.join(self.tmp_dir, 'cookie.json')

        # TODO re-login after some time -> delete cookie
        if os.path.isfile(cookie_path):
            with open(cookie_path, "r") as tmp_file:
                self.__login_cookie = json.loads(tmp_file.read())
            return

        r = requests.post(self.login_url, data={'name': self.__username, 'password': self.__password})

        if r.json()['success']:
            self.__login_cookie = r.cookies
            with open(cookie_path, 'w') as temp_file:
                temp_file.write(json.dumps(requests.utils.dict_from_cookiejar(r.cookies)))
        else:
            print('could not login. only SFW images available')

    def get_new_sfw_image(self):
        r = requests.get(self.items_url,
                         params={'flags': 1, 'promoted': 0},
                         cookies=self.__login_cookie)
        item_cache = r.json()['items'][0]

        '''
        r = requests.get(self.item_url, params={'itemId': item_cache['id']})
        item_meta = r.json()
        '''
        return {
            'id': item_cache['id'],
            'image': self.image_url + item_cache['image'],
            'up': item_cache['up'],
            'down': item_cache['down']
        }
