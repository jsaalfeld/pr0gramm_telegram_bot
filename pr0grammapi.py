import requests


class Pr0grammAPI:
    def __init__(self, username, password):
        self.password = password
        self.username = username

        self.image_url = 'http://img.pr0gramm.com/'
        self.api_url = 'http://pr0gramm.com/api/'
        self.login_url = self.api_url + 'user/login/'
        self.items_url = self.api_url + 'items/get'
        self.item_url = self.api_url + 'items/info'

    def login(self):
        # not really useful right now, since we do not save an cookie or auth key
        payload = {'name': self.username, 'password': self.password}

        r = requests.post(self.login_url, data=payload)
        print(r.content)

    def get_new_sfw_image(self):
        r = requests.get(self.items_url, params={'flags': 1, 'promoted': 0})
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
