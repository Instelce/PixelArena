from email import header
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
            self.headers = {'Authorization': f'Token {self.token}'}
        else:
            self.username = None
            self.token = None
            self.is_authenticate = False

        self.tasks = []

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
            self.headers = {'Authorization': f'Token {self.token}'}
            self.is_authenticate = True

            print(self.username, self.token, self.is_authenticate)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.is_authenticate

    def download_data(self):
        if self.is_authenticate:
            # Root
            root_responce = requests.get('http://127.0.0.1:8000/api/', headers=self.headers)
            self.root_data = json.loads(root_responce.content)    

            # Get api data
            self.api_data = {}
            for route in self.root_data:
                route_responce = requests.get(self.root_data[route], headers=self.headers)
                self.api_data[route] = json.loads(route_responce.content)

            self.tasks.append("Login to API")

            # GRAPHICS -----------------------------------------------
            # Delete and create graphics folder
            if os.path.exists('api_graphics'):
                remove_directory('api_graphics')
            os.mkdir('api_graphics')
            self.tasks.append("Remove all data")

            # Download graphics
            for graphic in self.api_data['graphics']:
                graphic_item = json.loads(requests.get(graphic['item'], headers=self.headers).text)
                graphic_item_name = graphic_item['name']
                graphic_image_url = graphic['image']
                graphic_item_category = json.loads(requests.get(graphic_item['category'], headers=self.headers).text)['name']

                filename = graphic_image_url.split('/')[-1]

                download_path = f'api_graphics/{graphic_item_category}/{graphic_item_name}/'
                image_data = requests.get(graphic_image_url).content
                
                # Create folders category/item/
                if not os.path.exists(f'api_graphics/{graphic_item_category}/'):
                    self.tasks.append(f'Create api_graphics/{graphic_item_category}/ folder ...')
                    os.mkdir(f'api_graphics/{graphic_item_category}/')
                    
                if not os.path.exists(download_path):
                    self.tasks.append(f'Create {download_path} folder ...')
                    os.mkdir(download_path)

                # Download image
                if not os.path.exists(download_path+filename):
                    with open(f'{download_path}{filename}', 'wb') as handler:
                        handler.write(image_data)
                        print(f'Downloading {filename} on the {download_path} directory with {graphic_image_url} url ...')
                        self.tasks.append(f"Downloading {filename} on the {download_path} directory")

            # DATA (shop, inventory) -----------------------------------------------
            player = self.get_player()
            write_json_file("data/player.json", {
                'username': player['username'],
                'token': self.token,
                'coins': player['coins'],
                'inventory': {}
            }) # Reset inventory

            shop_data = {}
            player_inventory = read_json_file("data/player.json")['inventory']

            for category in self.api_data['categories']:
                shop_data[category['name']] = [] # Shop
                player_inventory[category['name']] = [] # Inventory

            # Shop item
            for item in self.api_data['items']:
                temp_item = item.copy()

                # Replace the category url by category name
                item_category = json.loads(requests.get(temp_item['category'], headers=self.headers).text)['name']
                temp_item['category'] = item_category

                # Set the graphics path
                temp_item['graphics'] = f"api_graphics/{temp_item['category']}/{temp_item['name']}/full.png"
                
                temp_item['stats'] = {}

                shop_data[item_category].append(temp_item)

            # Inventory item
            for item in self.api_data['player-items']:
                temp_item = item.copy()

                # Replace the category url by category name
                item_category = json.loads(requests.get(temp_item['category'], headers=self.headers).text)['name']
                temp_item['category'] = item_category

                # Set the graphics path
                temp_item['graphics'] = f"api_graphics/{temp_item['category']}/{temp_item['name']}/full.png"
                
                temp_item['stats'] = {}

                if item['player'] == player['url']:
                    player_inventory[item_category].append(temp_item)

            for stat in self.api_data['items-stats']:
                stat_item = json.loads(requests.get(stat['item'], headers=self.headers).content)
                stat_item_name = stat_item['name']
                stat_item_category = json.loads(requests.get(stat_item['category'], headers=self.headers).content)['name']

                # Item's stats for shop
                for item in shop_data[stat_item_category]:
                    if item['name'] == stat_item_name:
                        item['stats'][stat['name']] = stat['value']
                
                # Item's stats for inventory
                for item in player_inventory[stat_item_category]:
                    if item['name'] == stat_item_name:
                        item['stats'][stat['name']] = stat['value']

            # Write shop.json with shop data
            write_json_file('data/api_shop.json', {})       
            write_json_file('data/api_shop.json', shop_data)
            self.tasks.append("Download shop data")

            # Write player.json with inventory data
            write_json_file("data/player.json", {
                'username': player['username'],
                'token': self.token,
                'coins': player['coins'],
                'inventory': player_inventory
            })

            self.tasks.append("Download inventory data")
            
    def get_player(self):
        if self.is_authenticate:
            players = self.api_data['players']

            for player_data in players:
                if player_data['username'] == self.username:
                    player = player_data

            return player

    def get_item(self, name):
        if self.is_authenticate:
            items = self.api_data['items']

            for item_data in items:
                if item_data['name'] == name:
                    item = item_data
            
            return item

    def add_player_item(self, data):
        try:
            responce = requests.post('http://127.0.0.1:8000/api/add-player-item', headers=self.headers, data=data)
            responce.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


# api = Api()

# api.download_data()
# player = api.get_player()
# print(player)
# sword = api.get_item('sword')
# print(sword)
# api.add_player_item({
#     'name': sword['name'],
#     'price': sword['price'],
#     'category': sword['category'],
#     'player': player['url']
# })