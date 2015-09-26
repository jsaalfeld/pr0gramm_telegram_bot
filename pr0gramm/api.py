import json
import logging
import os
from urllib.parse import urlparse
import requests

log = logging.getLogger('pr0Bot.api')


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
        log.info('Logging in...')
        cookie_path = os.path.join(self.tmp_dir, 'cookie.json')

        # TODO re-login after some time -> delete cookie
        if os.path.isfile(cookie_path):
            log.debug('Already logged in via cookie. Reading file.')
            try:
                with open(cookie_path, "r") as tmp_file:
                    self.__login_cookie = json.loads(tmp_file.read())
                return
            except IOError:
                log.warn('Could not open cookie file %s', cookie_path)

        log.debug('Logging in via request.')
        r = requests.post(self.login_url, data={'name': self.__username, 'password': self.__password})

        if r.json()['success']:
            self.__login_cookie = r.cookies
            try:
                with open(cookie_path, 'w') as temp_file:
                    temp_file.write(json.dumps(requests.utils.dict_from_cookiejar(r.cookies)))
            except IOError:
                log.warn('Could not write cookie file %s', cookie_path)
        else:
            log.warn('Login not possible. Only SFW/NSFW images available.')

    def get_top_image(self, flag):
        log.debug('Getting top image for flag %d', flag)

        try:
            r = requests.get(self.items_url,
                             params={'flags': flag, 'promoted': 1},
                             cookies=self.__login_cookie)
            item_cache = r.json()['items'][0]
        except (ConnectionError, TimeoutError):
            log.warn('Could not reach pr0gramm API.')

        log.debug('Got image with id %d', item_cache['id'])

        '''
        r = requests.get(self.item_url, params={'itemId': item_cache['id']})
        item_meta = r.json()
        '''
        return {
            'id': item_cache['id'],
            'image': self.image_url + item_cache['image'],
            'image_ext': os.path.splitext(urlparse(self.image_url + item_cache['image']).path)[1],
            'up': item_cache['up'],
            'down': item_cache['down'],
            'flag': flag
        }
