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
            'footstep_volume': 12
        },
        'run': {
            'speed': 2,
            'footstep_distance': 40,
            'footstep_volume': 24

        },
        'sneak': {
            'speed': 0.5,
            'footstep_distance': 20,
            'footstep_volume': 8
        }
    }
}


enemy_data = {
    'waypoint_radius': 20,
    'attack_radius': 5,
    'idle_duration_range': [500, 2000],
    'inspect_duration': 2000,
    'roar_duration': 1000,
    'curious_noise_threshold': 8,
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
            'footstep_volume': 5
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
            'With careful steps you search the light switch',
            '',
            'Press [ENTER] to continue.'
        ],
        'intro_audio': None,
        'outro_text': [
            'You groped your way for the light switch',
            'And hear, how the lamps light up',
            'But still, only darkness sorrounds you',
            'Frantically, you press the switch',
            'Again, and again...',
            'But no light meets your eyes'
        ],
        'outro_audio': None
    },
    1: {
        'intro_text': [
            'Suddenly, you hear voices from the hall',
            'Among the mutter, you locate a familiar sound',
            'Yes, clearly, your dog\'s squeaking toy',
            'You tear open the door and set foot into the hall',
            'Only, to find it twisted and mazed.',
        ],
        'intro_audio': None,
        'outro_text': [
            'You are past the strange hallway',
            'There, you find your dog\'s empty bed',
            'Your hands still feel the warmth of it',
            'But you only find the squeaking toy in it.'
        ],
        'outro_audio': None
    },
    2: {
        'intro_text': [
            'Your hands a searching for stability',
            'Running them down the cold metal walls',
            'All of a sudden a door swings open',
            'You fall through it...'
            '',
            'And find your self in another room'
        ],
        'intro_audio': None,
        'outro_text': [
            'You found strange ancient artifacts with glowing symbols',
            'Strangely, they open passages in this metal labyrinth',
            'It doesn\'t seem to fit together'
        ],
        'outro_audio': None

    },

    3: {
        'intro_text': [
            'With echoing steps you enter a vast space',
            'It is metal-clad just like the passage before',
            'Your let your fingers run along the cold walls',
            'Providing you little sense of orientation',
            '',
            'Soon you realize, you\'re not alone here',
            'Heavy steps in the darkness',
            'Each one of them sends shivers down your spine',
            '',
            'Across the large room, you seem to hear your dog'
        ],
        'intro_audio': None,
        'outro_text': [],
        'outro_audio': None


    },
}

# FOOTSTEP_DISTANCE = 20  # 40  # 120 for enemy?  # 40 for player
# FOOTSTEP_VOLUME = 15
FOOTSTEP_FADEOUT = 20
LINE_DURATION = 5  # Debug # 1500

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
