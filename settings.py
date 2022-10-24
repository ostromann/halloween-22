# game setup
WIDTH = 300
HEIGHT = 300
FPS = 60
INPUT = 'ps4'
CONTROLLER_DEADZONE = 0.3


TILESIZE = 20
WALL_WIDTH = 20

FOOTSTEP_DISTANCE = 20
FOOTSTEP_VOLUME = 15

OBJECT_PULLING_RADIUS = 50

FADEOUT_DECAY_TIME = 0.005

# SOUNDBEAM SETTINGS
SOUNDBEAM_FORCE = 8
SOUNDBEAM_SIZE = 2
SOUNDBEAM_SIZE_GAIN = 1
SOUNDBEAM_NUMBERS = 512
SOUNDBEAM_SPEED = 4
SOUNDBEAM_ATTENUATION = 20
SOUNDBEAM_MAX_LOUDNESS = 25
SOUNDBEAM_DIFFRACTION_FACTOR = 0.5

# ENEMY SETTINGS
ENEMY_FOOTSTEP_DISTANCE = 30
ENEMY_FOOTSTEP_VOLUME = 3
ENEMY_MOVEMENT_SPEED = 0.3
ENEMY_VOLUME_THRESHOLD = 100
ENEMY_VOLUME_DECAY = 5
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
