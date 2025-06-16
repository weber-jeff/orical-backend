from typing import Dict, List, Tuple, Union
import logging
import math

from .constants import ASPECT_ANGLES, DEFAULT_ASPECT_ORB, ROUNDING_PRECISION

ROUND_ORB = ROUNDING_PRECISION["orb"]
logger = logging.getLogger(__name__)

def normalize_angle(angle: float) -> float:
    return angle % 360

def shortest_angle_diff(a1: float, a2: float) -> float:
    diff = abs(a1 - a2)
    return min(diff, 360 - diff)

def calculate_aspects(
    planet_positions: Dict[str, Dict[str, float]],
    aspect_definitions: Dict[str, Tuple[float, float]] = None,
    planet_orbs: Dict[str, float] = None,
    single_aspect_per_pair: bool = False,
) -> Dict[str, List[Dict[str, Union[str, float]]]]:
    if aspect_definitions is None:
        aspect_definitions = ASPECT_ANGLES
    if planet_orbs is None:
        planet_orbs = DEFAULT_ASPECT_ORB

    aspects_found = {planet: [] for planet in planet_positions}
    planets = list(planet_positions.keys())

    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1, p2 = planets[i], planets[j]
            p1_lon = planet_positions[p1].get("longitude")
            p2_lon = planet_positions[p2].get("longitude")

            if p1_lon is None or p2_lon is None:
                logger.warning(f"Missing longitude for {p1} or {p2}, skipping aspect calculation")
                continue

            angle_diff = shortest_angle_diff(p1_lon, p2_lon)

            orb1 = planet_orbs.get(p1, planet_orbs.get("Default", 6))
            orb2 = planet_orbs.get(p2, planet_orbs.get("Default", 6))

            matched_aspects = []

            for aspect_name, (target_angle, default_orb) in aspect_definitions.items():
                weighted_orb = min(default_orb, (orb1 + orb2) / 2)
                orb_diff = abs(angle_diff - target_angle)

                if orb_diff <= weighted_orb:
                    orb = round(orb_diff, ROUND_ORB)
                    aspect_data = {
                        "aspecting_planet": p2,
                        "aspect_type": aspect_name,
                        "orb": orb,
                        "exact_angle_diff": round(angle_diff, ROUNDING_PRECISION["longitude"]),
                    }
                    matched_aspects.append(aspect_data)

                    if single_aspect_per_pair:
                        break

            if matched_aspects:
                if single_aspect_per_pair and len(matched_aspects) > 1:
                    matched_aspects.sort(key=lambda x: x["orb"])
                    matched_aspects = [matched_aspects[0]]

                for aspect_data in matched_aspects:
                    aspects_found[p1].append(aspect_data)
                    mirrored = aspect_data.copy()
                    mirrored["aspecting_planet"] = p1
                    aspects_found[p2].append(mirrored)

    return aspects_found

def assign_planets_to_houses(
    planet_positions: Dict[str, Dict[str, float]], house_cusps: List[float]
) -> Dict[str, int]:
    houses = {}
    for planet, position in planet_positions.items():
        lon = normalize_angle(position["longitude"])
        for i in range(12):
            start = normalize_angle(house_cusps[i])
            end = normalize_angle(house_cusps[(i + 1) % 12])
            if start < end:
                if start <= lon < end:
                    houses[planet] = i + 1
                    break
            else:
                if lon >= start or lon < end:
                    houses[planet] = i + 1
                    break
    return houses

if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stdout
    )

    aspect_definitions = {
        "Conjunction": (0, 8),
        "Opposition": (180, 8),
        # Add other aspects as needed
    }

    ROUND_ORB = 2
    angle_diff = 1.5
    orb1 = 5
    orb2 = 6
    p2 = "Mars"
    matched_aspects = []

    for aspect_name, (target_angle, default_orb) in aspect_definitions.items():
        orb_diff = abs(angle_diff - target_angle)
        weighted_orb = min(default_orb, (orb1 + orb2) / 2)
        if orb_diff <= weighted_orb:
            orb = round(orb_diff, ROUND_ORB)
            aspect_data = {
                "aspecting_planet": p2,
                "aspect_type": aspect_name,
                "orb": orb,
                "exact_angle_diff": angle_diff,
            }
            matched_aspects.append(aspect_data)

    logger.info(f"Matched aspects: {matched_aspects}")
