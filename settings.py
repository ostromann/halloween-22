# Debug Settings
ENEMY_DEBUG = False
PLAYER_DEBUG = False
FPS_DEBUG = False

# game setup
HEIGHT = 480  # 360  # 480
WIDTH = 720  # 480  # 720
FPS = 60
# INPUT = 'ps4'
# CONTROLLER_DEADZONE = 0.3


TILESIZE = 20
WALL_WIDTH = 20

player_data = {
    'stomp_volume': 40,
    'movement': {
        'idle': {
            'speed': 0,
            'footstep_distance': 0.1,
            'footstep_volume': 2
        },
        'walk': {
            'speed': 1,
            'footstep_distance': 20,
            'footstep_volume': 16
        },
        'run': {
            'speed': 2,
            'footstep_distance': 40,
            'footstep_volume': 26

        },
        'sneak': {
            'speed': 0.5,
            'footstep_distance': 20,
            'footstep_volume': 8
        }
    }
}

ENEMY_IDLE_NOISE_PROBABILITY = 0.9
enemy_data = {
    'max_attack_time': 10000,
    'waypoint_radius': 20,
    'attack_radius': 5,
    'idle_duration_range': [500, 2000],
    'inspect_duration': 2000,
    'roar_duration': 1000,
    'curious_noise_threshold': 4,
    'attack_noise_threshold': 16,
    'noise_decay': 2,
    'noise_sensitivity_list': ['player', 'player_metal', 'player_stomp', 'player_item'],
    'movement': {
        'idle': {
            'speed': 0,
            'footstep_distance': 30,
            'footstep_volume': 5
        },
        'walk': {
            'speed': 1,
            'footstep_distance': 30,
            'footstep_volume': 8
        },
        'run': {
            'speed': 2,
            'footstep_distance': 60,
            'footstep_volume': 20
        },
    }

}

level_data = {
    0: {
        'intro_text': [
            'You wake up from a nightmare',
            'A perfect darkness fills your room',
            'You try to orientate yourself',
            '...',
            'Hold [W,A,S,D] to move.',
            'Press [ENTER] to continue.'
        ],
        'intro_audio': None,
        'outro_text': [

        ],
        'outro_audio': None
    },
    1: {
        'intro_text': [
            'You reach the light switch and flick it',
            'But still, all you see is darkness',
            '...',
            'You hear a familiar sound from the hallway',
            'It\'s your dog\'s squeaking toy.',
            '...',
            'Press [SPACE] to stomp',
            'Hold [LSHIFT] to run',
        ],
        'intro_audio': None,
        'outro_text': [
        ],
        'outro_audio': None
    },
    2: {
        'intro_text': [
            'Your dog\'s bed is empty',
            'Only the squeaking toy is left behind',
            '...',
            'A trapdoor swings open and you fall through',
            'You can hear the rumble of a mechanism',
            'There must be a way back!',
            '...',
            'Press [E] to pull an object.',
            'Press [E] again to let loose.',
        ],
        'intro_audio': None,
        'outro_text': [
        ],
        'outro_audio': None
    },

    3: {
        'intro_text': [
            'You enter a vast space',
            'Soon you realize, you\'re not alone',
            'Heavy steps echo in the darkness',
            '...',
            'Water drops through some cracks in the walls',
            'These could be your way out!',
            '...',
            'Hold [LCTRL] to sneak',
        ],
        'intro_audio': None,
        'outro_text': [],
        'outro_audio': None
    },
    4: {
        'intro_text': [
            'You\'ve evaded the dreadful beast',
            'Now you find yourself in some kind of prison',
            '...',
            'And there, from behind the bars',
            'You can hear your dog barking',
            '...',
            'But once again, there is someone else here.'
        ],
        'intro_audio': None,
        'outro_text': [],
        'outro_audio': None
    },

}

# FOOTSTEP_DISTANCE = 20  # 40  # 120 for enemy?  # 40 for player
# FOOTSTEP_VOLUME = 15
FOOTSTEP_FADEOUT = 20
LINE_DURATION = 1500  # 1500  # 1500  # Debug 5 # 1500

OBJECT_PULLING_RADIUS = 25

FADEOUT_DECAY_TIME = 0.005

# SOUNDBEAM SETTINGS
SOUNDBEAM_COLLISION_TOLERANCE = 2
SOUNDBEAM_FORCE = 8
SOUNDBEAM_SIZE = 5  # 3  # 2 for 300 x 300
SOUNDBEAM_SIZE_GAIN = 0
SOUNDBEAM_MAX_SIZE_GAIN = 1
SOUNDBEAM_NUMBERS = 256
SOUNDBEAM_SPEED = 2
SOUNDBEAM_ATTENUATION = 20
SOUNDBEAM_MAX_LOUDNESS = 40
SOUNDBEAM_DIFFRACTION_FACTOR = 0


COLLISION_TYPES = {
    "soundbeam": 1,
    "obstacle": 2,
}

OBJECT_CATEGORIES = {
    "soundbeam":   0b01,
    "obstacle":    0b10,
}

CATEGORY_MASKS = {
    "soundbeam":   0b10,
    "obstacle":    0b11,
}
