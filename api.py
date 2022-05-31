import requests
import os
import json

from support import *


class Api:
    def __init__(self) -> None:
        self.player_data = read_json_file("data/player.json")

        # User
        if self.player_data['username'] != "":
            self.username = self.player_data['username']
            self.token = self.player_data['token']
            self.is_authenticate = True
        else:
            self.username = None
            self.token = None
            self.is_authenticate = False

        self.task = []

    def download_data(self):
        if self.is_authenticate:
            headers = {'Authorization': f'Token {self.token}'}
            self.task.append("Login to API")

            # Delete and create graphics folder
            if os.path.exists('api_graphics'):
                remove_directory('api_graphics')
            os.mkdir('api_graphics')
            self.task.append("Remove all data")

            # Root
            root_responce = requests.get('http://127.0.0.1:8000/api/', headers=headers)
            self.root_data = json.loads(root_responce.content)    

            # Get api data
            self.api_data = {}
            for route in self.root_data:
                route_responce = requests.get(self.root_data[route], headers=headers)
                self.api_data[route] = json.loads(route_responce.content)
                self.task.append(f"Request {route}")

            for graphic in self.api_data['graphics']:
                graphic_item = json.loads(requests.get(graphic['item'], headers=headers).text)
                graphic_item_name = graphic_item['name']
                graphic_image_url = graphic['image']
                graphic_item_category = json.loads(requests.get(graphic_item['category'], headers=headers).text)['name']

                filename = graphic_image_url.split('/')[-1]

                download_path = f'api_graphics/{graphic_item_category}/{graphic_item_name}/'
                image_data = requests.get(graphic_image_url).content
                
                # Create folders weapons/item/
                if not os.path.exists(f'api_graphics/{graphic_item_category}/'):
                    self.task = f'Create api_graphics/{graphic_item_category}/ folder ...'
                    os.mkdir(f'api_graphics/{graphic_item_category}/')
                    
                if not os.path.exists(download_path):
                    self.task = f'Create {download_path} folder ...'
                    os.mkdir(download_path)

                # Download image
                if not os.path.exists(download_path+filename):
                    with open(f'{download_path}{filename}', 'wb') as handler:
                        self.task = f'Downloading {filename} ...'

                        handler.write(image_data)
                        print(f'Downloading {filename} on the {download_path} directory with {graphic_image_url} url ...')
                        self.task.append(f"Downloading {filename} on the {download_path} directory")

        # Get shop data
        shop_data = {}

        for category in self.api_data['categories']:
            shop_data[category['name']] = []

        for item in self.api_data['items']:
            # Replace the category url by category name
            item_category = json.loads(requests.get(item['category'], headers=headers).text)['name']
            item['category'] = item_category

            item['graphics'] = f"api_graphics/{item['category']}/{item['name']}/full.png"
            item['stats'] = {}

            shop_data[item_category].append(item)

        for stat in self.api_data['stats']:
            stat_item = json.loads(requests.get(stat['item'], headers=headers).content)
            stat_item_name = stat_item['name']
            stat_item_category = json.loads(requests.get(stat_item['category'], headers=headers).content)['name']

            print(stat['name'], stat_item_name, stat_item_category)

            for item in shop_data[stat_item_category]:
                if item['name'] == stat_item_name:
                    item['stats'][stat['name']] = stat['value']

        # Write shop.json with shop data
        write_json_file('data/api_shop.json', {})       
        write_json_file('data/api_shop.json', shop_data)
        self.task.append("Download shop data")    
            
    def authenticate(self, username, password):
        body_data = {
            'username': username,
            'password': password
        }

        try:
            responce = requests.post('http://127.0.0.1:8000/api/login', data=body_data)
            responce.raise_for_status()

            self.username = username
            self.token = json.loads(responce.content)['token']
            self.is_authenticate = True

            write_json_file("data/player.json", {
                'username': self.username,
                'token': self.token
            })

            print(self.username, self.token, self.is_authenticate)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.is_authenticate
        

# api = Api()

# api.authenticate('admin', 'print(sd10W)')
# api.download_data()
