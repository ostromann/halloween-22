from gameplay.utils import *
from settings import ENEMY_VOLUME_DECAY


class Noisemeter():
    def __init__(self, sensitivity_list, noise_threshold1, noise_threshold2):
        self.noise_sources = {}
        # List of sprite types that should get reported
        self.sensitivity_list = sensitivity_list
        self.noise_threshold1 = noise_threshold1
        self.noise_threshold2 = noise_threshold2

    def update_noise_sources(self, sprite):
        '''
        Update the noise_sources dict.
        '''
        source = sprite.source
        if source not in self.noise_sources.keys():
            self.noise_sources[source] = sprite.volume
        else:
            self.noise_sources[source] = max(
                self.noise_sources[source], sprite.volume)

    def get_loudest_source(self, use_sensitivity_list=False):
        if use_sensitivity_list:
            return key_with_maxval(filter_dict_by_keys(self.noise_sources, self.sensitivity_list))
        else:
            return key_with_maxval(self.noise_sources)

    def decay_noise_sources(self, dt):
        for key, val in self.noise_sources.items():
            self.noise_sources[key] = max(
                [0, val - (self.noise_decay * dt) ** 4])  # TODO: Eye-balling this bezier curve

    def get_loudest_source_above_threshold(self, use_sensitivity_list=False):
        pass
