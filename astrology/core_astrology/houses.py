# houses.py

from typing import Dict, List, Union
import logging

from astrology.core_astrology.utils import normalize_angle

logger = logging.getLogger(__name__)

def assign_planets_to_houses(
    planet_positions: Dict[str, Dict[str, float]],
    house_cusps: List[float],
    house_system: str = "WholeSign",
) -> Dict[str, Union[int, str]]:
    """
    Assigns planets to houses based on their longitudes and house cusps.
    Supports multiple house systems: 'WholeSign' and 'Placidus' currently.

    Args:
        planet_positions: dict of planet -> dict with 'longitude' key.
        house_cusps: list of 12 house cusp longitudes in degrees.
        house_system: 'WholeSign' or 'Placidus' (default: WholeSign).

    Returns:
        Dict mapping planet name to assigned house number (1-12) or 'Unknown'.
    """

    if len(house_cusps) != 12:
        logger.error("House cusps list must contain exactly 12 values.")
        return {planet: "Unknown" for planet in planet_positions}

    if house_system not in {"WholeSign", "Placidus"}:
        logger.error(f"Unsupported house system: {house_system}")
        return {planet: "Unknown" for planet in planet_positions}

    # Normalize cusps to 0-360 degrees
    cusps_norm = [normalize_angle(cusp) for cusp in house_cusps]

    assignments: Dict[str, Union[int, str]] = {}

    if house_system == "WholeSign":
        # Whole sign houses start from the first cusp, each house = 30°
        start_cusp = cusps_norm[0]

        for planet, data in planet_positions.items():
            lon = data.get("longitude")
            if lon is None:
                logger.warning(f"Longitude missing for planet {planet}. Assigned 'Unknown'.")
                assignments[planet] = "Unknown"
                continue

            offset = (normalize_angle(lon) - start_cusp) % 360
            house = int(offset // 30) + 1
            assignments[planet] = house

    else:  # Placidus or other quadrant-based systems
        # Sort cusps to ensure order (should be in ascending order for houses 1-12)
        cusps_sorted = sorted(cusps_norm)

        for planet, data in planet_positions.items():
            lon = data.get("longitude")
            if lon is None:
                logger.warning(f"Longitude missing for planet {planet}. Assigned 'Unknown'.")
                assignments[planet] = "Unknown"
                continue

            lon_norm = normalize_angle(lon)
            house_assigned = None

            for i in range(12):
                start = cusps_sorted[i]
                end = cusps_sorted[(i + 1) % 12]

                # Handle cusp wrap-around (e.g., 350° to 10°)
                if start > end:
                    if lon_norm >= start or lon_norm < end:
                        house_assigned = i + 1
                        break
                else:
                    if start <= lon_norm < end:
                        house_assigned = i + 1
                        break

            if house_assigned is None:
                logger.warning(f"Could not assign house for planet {planet} with longitude {lon_norm}")
                house_assigned = "Unknown"

            assignments[planet] = house_assigned

    return assignments
