from csv import reader
from os import walk
import pygame


# def import_csv_layout(path):
# 	terrain_map = []
# 	with open(path) as level_map:
# 		layout = reader(level_map, delimiter=',')
# 		for row in layout:
# 			terrain_map.append(list(row))
# 		return terrain_map


# def import_folder(path, scale=None):
#   surface_list = []

#   for _, __, img_files in walk(path):
#     for image in img_files:
#       full_path = path + '/' + image
#       image_surf = pygame.image.load(full_path).convert_alpha()
#       if scale:
#         image_surf = pygame.transform.scale(image_surf, (128, 128))
#       surface_list.append(image_surf)
#   return surface_list

# def surf_rotate()


def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    # pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)


def get_distance_direction_a_to_b(a, b):
    '''
    Get distance and direction from vector a to vector b.
    '''
    a = pygame.math.Vector2(a)
    b = pygame.math.Vector2(b)
    distance = (b - a).magnitude()

    if distance > 0:
        direction = (b - a).normalize()
    else:
        direction = pygame.math.Vector2()
    return (distance, direction)


def key_with_maxval(d):
    """ a) create a list of the dict's keys and values; 
        b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def filter_dict_by_keys(d, keys):
    return {k: d[k] for k in keys}

# def get_closest_sprite_of_group(sprite, group):
#     '''
#     Get the closest sprite from a group of sprites
#     '''
#     dist_sprites = []  # list of distances and sprites
#     for other_sprite in group:
#         distance, _ = get_distance_direction_a_to_b(
#             sprite.pos, other_sprite.pos)
#         dist_sprites.append((distance, other_sprite))

#     return sorted(dist_sprites, key=lambda x: x[0])[0][1]
