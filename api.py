import requests
import os
import json

from support import *


# Root
root_responce = requests.get('http://127.0.0.1:8000/api/')
responce_data = json.loads(root_responce.content)
print(responce_data)

# Categories
category_responce = requests.get(responce_data['categories'])
category_data = json.loads(category_responce.content)
categories = []
for category in category_data:
    categories.append(category['name'])

# Items
items_responce = requests.get(responce_data['items'])
items_data = json.loads(items_responce.content)

for item_index, graphic in enumerate(items_data):
    category = json.loads(requests.get(graphic['category']).text)['name']
    graphic['category'] = category

# Graphics
graphics_responce = requests.get(responce_data['graphics'])
graphics_data = json.loads(graphics_responce.content)

for graphic in graphics_data:
    graphic_item = json.loads(requests.get(graphic['item']).text)['name']
    graphic_image_url = graphic['image']
    print(graphic_item, graphic_image_url)

os.mkdir('api_graphics')


