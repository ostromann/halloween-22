# Debug Settings
ENEMY_DEBUG = False
PLAYER_DEBUG = False
FPS_DEBUG = True

# game setup
WIDTH = 720  # 480  # 720
HEIGHT = 480  # 360  # 480
FPS = 60
# INPUT = 'ps4'
# CONTROLLER_DEADZONE = 0.3


TILESIZE = 20
WALL_WIDTH = 20

player_data = {
    'stomp_volume': 30,
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
    'noise_sensitivity_list': ['player', 'player_item'],
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
            'Cold sweat runs down your neck',
            'A perfect darkness fills your room',
            'Use [W,A,S,D] to move.'
            'Press [ENTER] to continue.'
        ],
        'intro_audio': None,
        'outro_text': [

        ],
        'outro_audio': None
    },
    1: {
        'intro_text': [
            'You groped your way for the light switch',
            'The lamps light up, but still only darkness',
            'Suddenly, you hear an all familiar sound from the hallway',
            'It\'s your dog\'s squeaking toy.',
            'Use [SPACE] to stomp',
            'Use [LSHIFT] to run'
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
            '',
            'All of a sudden a door swings open and you fall through',
            'Behind you, you can hear the rumble of a mechanism',
            'There must be a way back!',
            'Use [E] to pull an object.'
        ],
        'intro_audio': None,
        'outro_text': [
        ],
        'outro_audio': None
    },

    3: {
        'intro_text': [
            'With echoing steps you enter a vast space',
            'Soon you realize, you\'re not alone here',
            'Heavy steps in the darkness send shivers down your spine',
            'Water drops through some cracks in the walls',
            'These could be your way out!'
            'Use [LCTRL] to sneak'

        ],
        'intro_audio': None,
        'outro_text': [],
        'outro_audio': None
    },
    4: {
        'intro_text': [
            'You\'ve evaded the dreadful beast',
            'Now you find yourself in some kind of prison',
            'And there, from behind the bars',
            'You can hear the familiar sounds of your dog',
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
LINE_DURATION = 1500  # 1500  # Debug 5 # 1500

OBJECT_PULLING_RADIUS = 50

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
SOUNDBEAM_MAX_LOUDNESS = 30
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
