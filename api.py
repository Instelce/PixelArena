import requests
import os
import json

from support import *


class Api:
    def __init__(self) -> None:

        # User
        self.username = None
        self.token = None
        self.is_authenticate = False

        self.task = None

    def download_data(self):
        if self.is_authenticate:
            headers = {'Authorization': f'Token {self.token}'}
            print(headers)

            # Delete and create graphics folder
            if os.path.exists('api_graphics'):
                remove_directory('api_graphics')
            os.mkdir('api_graphics')

            # Root
            root_responce = requests.get('http://127.0.0.1:8000/api/', headers=headers)
            self.root_data = json.loads(root_responce.content)    

            # Categories
            category_responce = requests.get(self.root_data['categories'], headers=headers)
            self.category_data = json.loads(category_responce.content)

            # Items
            items_responce = requests.get(self.root_data['items'], headers=headers)
            self.items_data = json.loads(items_responce.content)
                
            # Graphics
            graphics_responce = requests.get(self.root_data['graphics'], headers=headers)
            graphics_data = json.loads(graphics_responce.content)

            for graphic in graphics_data:
                graphic_item = json.loads(requests.get(graphic['item'], headers=headers).text)
                graphic_item_name = graphic_item['name']
                graphic_image_url = graphic['image']
                graphic_item_category = json.loads(requests.get(graphic_item['category'], headers=headers).text)['name']

                filename = graphic_image_url.split('/')[-1]

                print(filename, graphic_image_url)
                print(graphic_item_name, graphic_item_category)

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
                        print(f'Downloading {filename} ...')

        # Get shop data
        shop_data = {}

        for category in self.category_data:
            shop_data[category['name']] = []

        for item_index, item in enumerate(self.items_data):
            # Replace the category url by category name
            item_category = json.loads(requests.get(item['category'], headers=headers).text)['name']
            item['category'] = item_category

            item['graphics'] = f"api_graphics/{item['category']}/{item['name']}/full.png"

            shop_data[item_category].append(item)    

        write_json_file('data/api_shop.json', {})       
        write_json_file('data/api_shop.json', shop_data)       
            
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

            print(self.username, self.token, self.is_authenticate)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        

api = Api()

api.authenticate('admin', '')
api.download_data()
