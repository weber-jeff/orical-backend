# constants.py

from enum import Enum, auto

class Planet(Enum):
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
    # Future additions:
    # CHIRON = 10
    # TRUE_NODE = 11

class Aspect(Enum):
    CONJUNCTION = auto()
    OPPOSITION = auto()
    TRINE = auto()
    SQUARE = auto()
    SEXTILE = auto()

# Mapping planet names to their Swiss Ephemeris numeric codes for API compatibility
PLANET = {
    "Sun": Planet.SUN.value,
    "Moon": Planet.MOON.value,
    "Mercury": Planet.MERCURY.value,
    "Venus": Planet.VENUS.value,
    "Mars": Planet.MARS.value,
    "Jupiter": Planet.JUPITER.value,
    "Saturn": Planet.SATURN.value,
    "Uranus": Planet.URANUS.value,
    "Neptune": Planet.NEPTUNE.value,
    "Pluto": Planet.PLUTO.value,
}

# Aspect definitions: aspect name -> (ideal angle in degrees, default orb in degrees)
ASPECT_ANGLES = {
    "Conjunction": (0, 8),
    "Opposition": (180, 8),
    "Trine": (120, 6),
    "Square": (90, 6),
    "Sextile": (60, 4),
}

# Default orb allowances per planet for aspect calculations (degrees)
DEFAULT_ASPECT_ORB = {
    "Sun": 6,
    "Moon": 8,
    "Mercury": 5,
    "Venus": 5,
    "Mars": 5,
    "Jupiter": 6,
    "Saturn": 6,
    "Uranus": 6,
    "Neptune": 6,
    "Pluto": 6,
    "Default": 6,  # fallback orb if planet not listed
    # Future celestial points could be added here:
    # "Chiron": 10,
    # "True Node": 8,
}

# Precision rounding constants for astrological calculations
ROUNDING_PRECISION = {
    "longitude": 6,
    "latitude": 6,
    "distance_au": 8,
    "speed_longitude": 6,
    "orb": 2,
}

# Ephemeris path (set default or leave None to set dynamically)
EPHEMERIS_PATH = None  # e.g., "/usr/share/ephe" or "ephemeris/"

ZODIAC_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

ZODIAC_MODALITIES = {
    "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
    "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
    "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable",
}

