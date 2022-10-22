# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
INPUT = 'ps4'
CONTROLLER_DEADZONE = 0.2
SOUNDBEAM_RADIUS = 1
SOUNDBEAM_NUMBERS = 16
SOUNDBEAM_ATTENUATION = 10

COLLISION_TYPES = {
    "soundbeam": 1,
    "obstacle": 2,
}

OBJECT_CATEGORIES = {
    "soundbeam":   0b01,
    "obstacle":    0b10,
}

CATEGORY_MASKS = {
    "soundbeam":   0b11,
    "obstacle":    0b11,
}
