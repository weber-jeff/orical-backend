# encoder.py

from .constants import PLANET_IDS, SIGN_IDS, HOUSE_IDS, ASPECT_IDS

def encode_planet_in_sign(planet: str, sign: str) -> tuple[int, int]:
    """
    Return a tuple of (planet_id, sign_id)
    """
    return (
        PLANET_IDS.get(planet, -1),
        SIGN_IDS.get(sign, -1)
    )

def encode_planet_in_house(planet: str, house: str) -> tuple[int, int]:
    """
    Return a tuple of (planet_id, house_id)
    """
    return (
        PLANET_IDS.get(planet, -1),
        HOUSE_IDS.get(house, -1)
    )

def encode_aspect_between_planets(planet1: str, planet2: str, aspect: str) -> tuple[int, int, int]:
    """
    Return a tuple of (planet1_id, planet2_id, aspect_id)
    """
    return (
        PLANET_IDS.get(planet1, -1),
        PLANET_IDS.get(planet2, -1),
        ASPECT_IDS.get(aspect, -1)
    )

def encode_chart_vector(planet_sign_map: dict, planet_house_map: dict, aspects: list[tuple[str, str, str]]) -> list[int]:
    """
    Build a flat list of all encoded values from the natal chart.
    Useful for numerology-AI fusion scoring.

    Args:
        planet_sign_map: e.g., {"Sun": "Aries", ...}
        planet_house_map: e.g., {"Sun": "1st", ...}
        aspects: list of (planet1, planet2, aspect_name)

    Returns:
        List of unique encoded integers.
    """
    encoded = set()

    for planet, sign in planet_sign_map.items():
        pid, sid = encode_planet_in_sign(planet, sign)
        if pid > 0: encoded.add(pid)
        if sid > 0: encoded.add(sid)

    for planet, house in planet_house_map.items():
        pid, hid = encode_planet_in_house(planet, house)
        if hid > 0: encoded.add(hid)

    for p1, p2, asp in aspects:
        pid1, pid2, aid = encode_aspect_between_planets(p1, p2, asp)
        if aid > 0: encoded.add(aid)

    return sorted(encoded)
