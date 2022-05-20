from csv import reader
import os
import json
import pygame

from settings import TILE_SIZE


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, image_files in os.walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            new_surf.blit(surface, (0, 0), pygame.Rect(
                x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surf)
    return cut_tiles


def read_json_file(path):
    with open(path, 'r') as f:
        cache = f.read()
        data = eval(cache)
    return data

def write_json_file(path, data):
    json_object = json.dumps(data, indent=4)
    with open(path, 'w') as f:
        f.write(json_object)
    return data


def remove_directory(dir):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            remove_directory(path)
        else:
            os.unlink(path)
    os.rmdir(dir)