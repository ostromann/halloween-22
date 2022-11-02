from email.mime import base
import os
import pygame
from random import choice

from gameplay.utils import import_audio_folder


class SoundPlayer:
    def __init__(self):
        base_path = os.path.join('assets', 'audio', 'sfx')
        pygame.mixer.init()
        self.sounds = {
            # footsteps
            'player_wood': import_audio_folder(os.path.join(base_path, 'player', 'wood')),
            'player_metal': import_audio_folder(os.path.join(base_path, 'player', 'metal')),
            'player_stomp': [pygame.mixer.Sound(os.path.join(base_path, 'player', 'player_stomp.wav'))],
            'enemy_metal': import_audio_folder(os.path.join(base_path, 'enemy', 'metal')),
            'enemy_idle': import_audio_folder(os.path.join(base_path, 'enemy', 'enemy_idle')),
            'enemy_roar': [pygame.mixer.Sound(os.path.join(base_path, 'enemy', 'enemy_roar.wav'))],
            'enemy_attack': [pygame.mixer.Sound(os.path.join(base_path, 'enemy', 'enemy_attack.wav'))],
            # 'enemy_footstep': [pygame.mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'hit.wav'))],
            'voices': import_audio_folder(os.path.join(base_path, 'objects', 'voices')),

            # stomp

            # Ambient Sounds
            'voices': import_audio_folder(os.path.join(base_path, 'objects', 'voices')),
            'toy': import_audio_folder(os.path.join(base_path, 'objects', 'toy')),
            'water': import_audio_folder(os.path.join(base_path, 'objects', 'water')),
            'mechanism': import_audio_folder(os.path.join(base_path, 'objects', 'mechanism')),
            'dog': import_audio_folder(os.path.join(base_path, 'objects', 'dog')),

            # door movement
            'door': [pygame.mixer.Sound(os.path.join(base_path,  'objects', 'door.wav'))],
        }

    def play_random_sound(self, pos, volume, sound_type):
        if sound_type == 'voices':
            volume = 0.2
        elif sound_type == 'player_wood' or 'player_metal':
            volume = 0.7
        elif sound_type == 'enemy_metal':
            volume = 0.6
        elif sound_type == 'enemy_idle':
            volume = 0.3
        elif sound_type == 'door':
            volume = 0.5
        else:
            volume = 0.5
        sound = choice(self.sounds[sound_type])
        Sound(None, pos, sound, volume)


class Sound():
    def __init__(self, player, pos, sound, volume):
        sound.set_volume(volume)
        sound.play()
        # TODO: get distance to player and adjsut loudness
