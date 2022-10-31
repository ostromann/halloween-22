from os import walk
import os
import pygame


def import_image_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            surface_list.append(pygame.image.load(
                os.path.join(path, image)).convert_alpha())

    return surface_list


def import_audio_folder(path):
    sound_list = []

    for _, _, audio_files in walk(path):
        for audio in audio_files:
            sound_list.append(pygame.mixer.Sound(os.path.join(path, audio)))

    return sound_list


def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


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
