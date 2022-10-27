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
            'enemy_metal': import_audio_folder(os.path.join(base_path, 'enemy', 'metal')),
            'enemy_low_call': [pygame.mixer.Sound(os.path.join(base_path, 'enemy', 'enemy_idle.wav'))],
            # 'enemy_footstep': [pygame.mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'hit.wav'))],

            # stomp


            # door movement
            'door': [pygame.mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'objects', 'door.wav'))],
        }

    def play_random_sound(self, pos, volume, sound_type):
        sound = choice(self.sounds[sound_type])
        Sound(None, pos, sound, volume)


class Sound():
    def __init__(self, player, pos, sound, volume):
        sound.set_volume(0.5)
        sound.play()
        # TODO: get distance to player and adjsut loudness
