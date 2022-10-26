# game setup
WIDTH = 720  # 480  # 720
HEIGHT = 480  # 360  # 480
FPS = 60
# INPUT = 'ps4'
# CONTROLLER_DEADZONE = 0.3


TILESIZE = 20
WALL_WIDTH = 20

player_data = {
    'movement': {
        'idle': {
            'speed': 0,
            'footstep_distance': 0.1,
            'footstep_volume': 2
        },
        'walk': {
            'speed': 1,
            'footstep_distance': 20,
            'footstep_volume': 8
        },
        'run': {
            'speed': 2,
            'footstep_distance': 40,
            'footstep_volume': 16

        },
        'sneak': {
            'speed': 0.5,
            'footstep_distance': 20,
            'footstep_volume': 4
        }
    }

}

PLAYER_MOVEMENT_SPEED = 1
PLAYER_WALK_FOOTSTEP_DISTANCE = 20
PLAYER_WALK_FOOTSTEP_VOLUME = 8

PLAYER_SNEAK_FOOTSTEP_DISTANCE = 20
PLAYER_SNEAK_FOOTSTEP_VOLUME = 3

PLAYER_RUN_FOOTSTEP_DISTANCE = 40
PLAYER_RUN_FOOTSTEP_VOLUME = 20

PLAYER_WALKING_SPEED = 1
PLAYER_SNEAK_SPEED = 0.5
PLAYER_RUNNING_SPEED = 2

# FOOTSTEP_DISTANCE = 20  # 40  # 120 for enemy?  # 40 for player
# FOOTSTEP_VOLUME = 15
FOOTSTEP_FADEOUT = 20

OBJECT_PULLING_RADIUS = 50

FADEOUT_DECAY_TIME = 0.005

# SOUNDBEAM SETTINGS
SOUNDBEAM_FORCE = 8
SOUNDBEAM_SIZE = 5  # 3  # 2 for 300 x 300
SOUNDBEAM_SIZE_GAIN = 0
SOUNDBEAM_MAX_SIZE_GAIN = 1
SOUNDBEAM_NUMBERS = 256
SOUNDBEAM_SPEED = 2
SOUNDBEAM_ATTENUATION = 20
SOUNDBEAM_MAX_LOUDNESS = 25
SOUNDBEAM_DIFFRACTION_FACTOR = 0

# ENEMY SETTINGS
ENEMY_FOOTSTEP_DISTANCE = 40
ENEMY_FOOTSTEP_VOLUME = 5
ENEMY_MOVEMENT_SPEED = 1
ENEMY_VOLUME_THRESHOLD = 600
ENEMY_VOLUME_DECAY = 2
ENEMY_DESTINATION_RADIUS = 10

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
