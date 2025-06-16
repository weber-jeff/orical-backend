import os
import logging
from typing import Dict, List, Union
import swisseph as swe
from collections import Counter

from astrology.core_astrology.utils import local_to_utc
from astrology.astro_data.load_meanings import MeaningLoader
from astrology.core_astrology.planetary_positions import (
    calculate_planet_positions,
    get_moon_sign,
    degree_to_sign,
)
from astrology.core_astrology.aspects import calculate_aspects
from astrology.core_astrology.houses import assign_planets_to_houses
from astrology.core_astrology.constants import ZODIAC_ELEMENTS, ZODIAC_MODALITIES

MAJOR_PLANETS = {
    "Sun", "Moon", "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
}

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger(__name__)

def get_dominant_trait(planet_positions: Dict[str, dict], trait_map: dict) -> str:
    traits = [trait_map.get(data.get("sign")) for planet, data in planet_positions.items()
              if planet in MAJOR_PLANETS and data.get("sign") in trait_map]
    return Counter(traits).most_common(1)[0][0] if traits else "Unknown"

def _validate_inputs(year: int, month: int, day: int, hour: int, minute: int, lat: float, lon: float, timezone_str: str) -> None:
    if not (1 <= month <= 12): raise ValueError("Month must be between 1 and 12")
    if not (1 <= day <= 31): raise ValueError("Day must be between 1 and 31")
    if not (0 <= hour < 24): raise ValueError("Hour must be between 0 and 23")
    if not (0 <= minute < 60): raise ValueError("Minute must be between 0 and 59")
    if not (-90 <= lat <= 90): raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= lon <= 180): raise ValueError("Longitude must be between -180 and 180")
    if not timezone_str: raise ValueError("Timezone string must be provided")

def _check_for_error(result: dict, context: str) -> bool:
    if "error" in result:
        logger.error(f"{context} error: {result['error']}")
        return True
    return False

def generate_birth_chart(
    year: int,
    month: int,
    day: int,
    hour: int = 12,
    minute: int = 0,
    timezone_str: str = "UTC",
    lat: float = 0.0,
    lon: float = 0.0,
    alt: float = 0.0,
    house_system: str = "P",
) -> Dict[str, Union[str, float, dict, list]]:
    try:
        _validate_inputs(year, month, day, hour, minute, lat, lon, timezone_str)
        ut_dt = local_to_utc(year, month, day, hour, minute, timezone_str)
        frac_hour = ut_dt.hour + ut_dt.minute / 60.0 + ut_dt.second / 3600.0 + ut_dt.microsecond / 3_600_000_000.0
        jd_ut = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day, frac_hour)
        swe.set_topo(lon, lat, alt)

        planet_positions = calculate_planet_positions(ut_dt.year, ut_dt.month, ut_dt.day, ut_dt.hour, ut_dt.minute, lat, lon, alt)
        if _check_for_error(planet_positions, "Planet positions"):
            return {"error": planet_positions["error"]}

        sun_sign = degree_to_sign(planet_positions.get("Sun", {}).get("longitude"))
        moon_sign = get_moon_sign(ut_dt.year, ut_dt.month, ut_dt.day, ut_dt.hour, ut_dt.minute, lat, lon, alt)
        if moon_sign.startswith("Error"):
            return {"error": moon_sign}

        loader = MeaningLoader()
        sun_data = {
            "planet_only": loader.get_meaning("planet_sign_meanings.json", "Sun", default={}),
            "planet_sign_meanings": loader.get_meaning("planet_sign_meanings.json", "Sun", sun_sign, default={}),
        }
        moon_data = {
            "planet_only": loader.get_meaning("planet_in_sign.json", "Moon", default={}),
            "planet_in_sign": loader.get_meaning("planet_in_sign.json", "Moon", moon_sign, default={}),
        }

        aspects = calculate_aspects(planet_positions)
        if _check_for_error(aspects, "Aspects"):
            return {"error": aspects["error"]}

        house_cusps, ascmc = swe.houses(jd_ut, lat, lon, house_system.encode())
        planet_houses = assign_planets_to_houses(planet_positions, list(house_cusps))
        if _check_for_error(planet_houses, "House assignment"):
            return {"error": planet_houses["error"]}

        asc_sign = degree_to_sign(ascmc[0])
        mc_sign = degree_to_sign(ascmc[1])
        vertex_sign = degree_to_sign(ascmc[3])

        all_meanings = loader.get_full_meaning("planet_in_house.json")
        planet_house_meanings = {planet: all_meanings.get(planet, {}).get(str(house), "No meaning found.") for planet, house in planet_houses.items()}

        dominant_element = get_dominant_trait(planet_positions, ZODIAC_ELEMENTS)
        dominant_modality = get_dominant_trait(planet_positions, ZODIAC_MODALITIES)

        return {
            "birth_datetime_utc": ut_dt.strftime("%Y-%m-%d %H:%M:%S UT"),
            "julian_day_ut": jd_ut,
            "geo_location": {"latitude": lat, "longitude": lon, "altitude": alt},
            "planet_positions": planet_positions,
            "sun_sign": sun_sign,
            "sun_meaning": sun_data,
            "moon_sign": moon_sign,
            "moon_meaning": moon_data,
            "aspects": aspects,
            "house_cusps_placidus": list(house_cusps),
            "ascendant_sign": asc_sign,
            "mc_sign": mc_sign,
            "vertex_sign": vertex_sign,
            "planet_houses": planet_houses,
            "planet_house_meanings": planet_house_meanings,
            "house_system": house_system,
            "chart_meta": {
                "dominant_element": dominant_element,
                "dominant_modality": dominant_modality,
                "chart_type": f"{dominant_element} {dominant_modality}"
            },
        }

    except Exception as e:
        logger.error("Unexpected error in generate_birth_chart", exc_info=True)
        return {"error": f"Unexpected error: {str(e)}"}
