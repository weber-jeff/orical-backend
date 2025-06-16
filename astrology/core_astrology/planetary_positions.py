import os
import sys
import logging
from datetime import datetime
from typing import Dict, Optional, Union, List, Tuple

import pytz
import swisseph as swe

from astrology.core_astrology.utils import (
    normalize_angle,
    degree_to_sign,
    local_to_utc,
    calculate_julian_day,
)

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# --- Swiss Ephemeris Planet IDs ---
SWISSEPH_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    # Optional: add nodes, Chiron, etc.
}

# --- Ephemeris Path ---
EPHEMERIS_PATH = os.getenv("SWISS_EPHE_PATH", "/media/jeff/numy/numerology_ai/astrology/mp")

# --- Aspect Definitions ---
ASPECT_ANGLES = {
    "Conjunction": (0.0, 8.0),
    "Opposition": (180.0, 8.0),
    "Trine": (120.0, 6.0),
    "Square": (90.0, 6.0),
    "Sextile": (60.0, 4.0),
}

# --- Default Orb Per Planet ---
DEFAULT_PLANET_ORBS = {
    "Sun": 8.0,
    "Moon": 8.0,
    "Mercury": 6.0,
    "Venus": 6.0,
    "Mars": 6.0,
    "Jupiter": 7.0,
    "Saturn": 7.0,
    "Uranus": 5.0,
    "Neptune": 5.0,
    "Pluto": 5.0,
    "Default": 5.0,
}

# --- Rounding Constants ---
ROUND_LONGITUDE = 6
ROUND_LATITUDE = 6
ROUND_DISTANCE_AU = 8
ROUND_SPEED_LONGITUDE = 6
ROUND_ORB = 2

# --- Main Planet Position Calculator ---
def calculate_planet_positions(julian_day: float) -> Dict[str, Dict[str, Union[float, str]]]:
    positions = {}
    try:
        swe.set_ephe_path(EPHEMERIS_PATH)

        for name, pid in SWISSEPH_PLANETS.items():
            flags = swe.FLG_SWIEPH | swe.FLG_SPEED
            planet_data = swe.calc_ut(julian_day, pid, flags)
            lon = round(planet_data[0][0], ROUND_LONGITUDE)
            lat = round(planet_data[0][1], ROUND_LATITUDE)
            dist = round(planet_data[0][2], ROUND_DISTANCE_AU)
            speed = round(planet_data[0][3], ROUND_SPEED_LONGITUDE)

            sign = degree_to_sign(lon)

            positions[name] = {
                "longitude": lon,
                "latitude": lat,
                "distance_au": dist,
                "speed_longitude": speed,
                "sign": sign,
            }

        return positions

    except Exception as e:
        logger.error("Exception in calculate_planet_positions:", exc_info=True)
        raise e

# Aspect definitions: aspect_name: (exact_angle, default_orb_for_aspect_type)
ASPECT_ANGLES = {
    "Conjunction": (0.0, 8.0),
    "Opposition": (180.0, 8.0),
    "Trine": (120.0, 6.0),
    "Square": (90.0, 6.0),
    "Sextile": (60.0, 4.0),
    # Add others like Quintile, Septile, SemiSquare, Sesquiquadrate if desired
}



def get_moon_sign(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    lat: float,
    lon: float,
    altitude: float = 0.0,
    timezone_str: Optional[str] = None,
    ephe_path: Optional[str] = None,
) -> Union[str, Dict[str, str]]:
    """
    Calculate the Moon's zodiac sign for the given date, time, and location.

    Args:
        Same as calculate_planet_positions for date/time/location.

    Returns:
        Moon sign as string (e.g., "Cancer") or dict with 'error' key on failure.
    """
    try:
        if ephe_path:
            set_ephemeris_path(ephe_path)

        if timezone_str:
            dt_utc = local_to_utc(year, month, day, hour, minute, timezone_str)
            jd_ut = calculate_julian_day(dt_utc)
        else:
            jd_ut = swe.julday(year, month, day, hour + minute / 60.0)

        swe.set_topo(lon, lat, altitude)

        moon_data, ret_flag = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SWIEPH)

        if ret_flag < 0 or not moon_data or len(moon_data) < 1:
            logger.error(f"Failed to calculate Moon position, ret_flag={ret_flag}")
            return {"error": "Failed to calculate Moon position"}

        moon_longitude = normalize_angle(moon_data[0])
        moon_sign = degree_to_sign(moon_longitude)

        return moon_sign

    except Exception as e:
        logger.exception("Exception in get_moon_sign:")
        return {"error": str(e)}

# --- Utility Functions ---

def set_ephemeris_path(custom_ephe_path: Optional[str] = None) -> str:
    """
    Set Swiss Ephemeris data path.

    Prioritizes custom_ephe_path, then EPHEMERIS_PATH constant.
    Raises FileNotFoundError if no valid path is found.
    A TODO for auto-downloading ephemeris files remains a good idea for user-friendliness.

    Args:
        custom_ephe_path: Optional custom path to ephemeris files.

    Returns:
        The effective ephemeris path used.

    Raises:
        FileNotFoundError: If a valid ephemeris directory cannot be found or set.
    """
    paths_to_try = []
    if custom_ephe_path:
        paths_to_try.append(custom_ephe_path)
    paths_to_try.append(EPHEMERIS_PATH) # Default defined in constants

    for path_attempt in paths_to_try:
        if path_attempt and os.path.isdir(path_attempt):
            try:
                swe.set_ephe_path(path_attempt)
                logger.info(f"Swiss Ephemeris path set to: {path_attempt}")
                return path_attempt
            except Exception as e: # pylint: disable=broad-except
                logger.warning(f"Could not set ephemeris path to {path_attempt} using swe.set_ephe_path: {e}")
        else:
            if path_attempt == custom_ephe_path: # only log warning if it was a custom attempt
                 logger.warning(f"Provided custom ephemeris path is not a valid directory: {path_attempt}")


    # If all attempts fail
    error_msg = (
        f"No valid Swiss Ephemeris directory found. "
        f"Tried custom path: '{custom_ephe_path}', and default: '{EPHEMERIS_PATH}'. "
        f"Please ensure ephemeris files are available and the path is correct."
        # TODO: Consider implementing ephemeris auto-download here.
    )
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)


def normalize_angle(angle: float) -> float:
    """Normalize an angle to the range [0, 360)."""
    return angle % 360.0


def degree_to_sign(degree: float) -> str:
    """Convert a celestial longitude (0-360) to its zodiac sign name."""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ]
    normalized_degree = normalize_angle(degree)
    index = int(normalized_degree // 30)
    return signs[index % 12]


def local_to_utc(
    year: int, month: int, day: int, hour: int, minute: int, timezone_str: str
) -> datetime:
    """
    Convert local date/time with a timezone string to a UTC datetime object.
    """
    try:
        tz = pytz.timezone(timezone_str)
    except pytz.exceptions.UnknownTimeZoneError as e:
        logger.error(f"Invalid timezone string '{timezone_str}': {e}")
        raise ValueError(f"Invalid timezone string: {timezone_str}") from e
    
    local_dt = datetime(year, month, day, hour, minute)
    try:
        localized_dt = tz.localize(local_dt, is_dst=None) # is_dst=None raises AmbiguousTimeError/NonExistentTimeError
    except (pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError) as e:
        logger.error(f"Could not unambiguously localize {local_dt} to timezone '{timezone_str}': {e}. Consider providing UTC or a non-ambiguous time.")
        # Fallback: try to force it, or let it raise. Forcing might be bad.
        # For now, re-raise a more informative error.
        raise ValueError(f"Timezone localization failed for {local_dt} in {timezone_str}: {e}") from e
        
    return localized_dt.astimezone(pytz.utc)


def calculate_julian_day_utc(dt_utc: datetime) -> float:
    """
    Calculate Julian Day (UT) from a UTC datetime object.
    """
    if dt_utc.tzinfo is None or dt_utc.tzinfo.utcoffset(dt_utc) != pytz.utc.utcoffset(None):
        raise ValueError("Input datetime must be UTC.")
    
    jd_ut = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
    )
    return jd_ut

# --- Core Astrological Calculation Functions ---

def calculate_planet_positions(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    latitude_deg: float,
    longitude_deg: float,
    altitude_m: float = 0.0,
    timezone_str: Optional[str] = None,
    ephe_path_override: Optional[str] = None,
    flags: int = swe.FLG_SWIEPH | swe.FLG_SPEED,
) -> Dict[str, Dict[str, Union[float, str]]]:
    """
    Calculate positions of planets for a given datetime and location.

    Args:
        year, month, day, hour, minute: Date and time.
            If timezone_str is provided, this is treated as local time.
            If timezone_str is None, this is treated as UTC.
        latitude_deg, longitude_deg: Geographic coordinates in degrees.
        altitude_m: Altitude in meters above sea level.
        timezone_str: Timezone name (e.g., 'America/New_York'). If None, UTC is assumed.
        ephe_path_override: Optional path to ephemeris files, overriding the default.
        flags: Swiss Ephemeris calculation flags.

    Returns:
        A dictionary where keys are planet names and values are dictionaries
        containing 'longitude', 'latitude', 'distance_au', 'speed_longitude', 'sign'.
        Returns a dictionary with an 'error' key on failure.
    """
    try:
        # Ensure ephemeris path is set. This will raise FileNotFoundError if unsuccessful.
        effective_ephe_path = set_ephemeris_path(ephe_path_override)

        if timezone_str:
            dt_utc = local_to_utc(year, month, day, hour, minute, timezone_str)
            jd_ut = calculate_julian_day_utc(dt_utc)
        else:
            # Assume UTC if no timezone_str is provided
            # Note: swe.julday can take a Gregorian date directly
            jd_ut = swe.julday(year, month, day, hour + minute / 60.0)

        # Set observer's location for topocentric calculations
        swe.set_topo(longitude_deg, latitude_deg, altitude_m)

        positions: Dict[str, Dict[str, Union[float, str]]] = {}
        for name, planet_id in SWISSEPH_PLANETS.items():

            pos_data, return_flag = swe.calc_ut(jd_ut, planet_id, flags)

            if return_flag < 0 or not pos_data or len(pos_data) < 6: # Speed flag adds more elements
                error_msg = (
                    f"Failed to calculate position for {name}. "
                    f"Swiss Ephemeris error flag: {return_flag}. "
                    f"Ensure ephemeris files at '{effective_ephe_path}' are complete and accessible for the given date."
                )
                logger.error(error_msg)
                # Decide: continue to next planet or return error for all?
                # For now, we'll try to get as many as possible and log errors.
                # If critical, one might return {"error": error_msg} here.
                positions[name] = {"error": f"Calculation failed, flag: {return_flag}"}
                continue

            longitude = normalize_angle(pos_data[0])
            positions[name] = {
                "longitude": round(longitude, ROUND_LONGITUDE),
                "latitude": round(pos_data[1], ROUND_LATITUDE),
                "distance_au": round(pos_data[2], ROUND_DISTANCE_AU),
                "speed_longitude": round(pos_data[3], ROUND_SPEED_LONGITUDE),
                # "speed_latitude": round(pos_data[4], ROUND_SPEED_LONGITUDE), # if needed
                # "speed_distance": round(pos_data[5], ROUND_SPEED_LONGITUDE), # if needed
                "sign": degree_to_sign(longitude),
            }

        if not positions:
            return {"error": "No planetary positions could be calculated. Check logs for details."}
        
        # Check if all planets have data or if some had errors
        if any("error" in data for data in positions.values()):
             logger.warning("Some planet positions could not be calculated. See previous errors.")


        return positions

    except FileNotFoundError as e: # From set_ephemeris_path
        logger.critical(f"Ephemeris path setup failed: {e}")
        return {"error": f"Ephemeris path setup failed: {e}"}
    except ValueError as e: # From local_to_utc or calculate_julian_day_utc
        logger.error(f"Date/Time/Timezone conversion error: {e}")
        return {"error": f"Date/Time/Timezone conversion error: {e}"}
    except Exception as e: # Catch-all for other unexpected swisseph errors or issues
        logger.exception("Unexpected exception in calculate_planet_positions:")
        return {"error": f"An unexpected error occurred: {e}"}


def calculate_aspects(
    planet_positions: Dict[str, Dict[str, Union[float, str]]], # Expects output from calculate_planet_positions
    aspect_definitions: Optional[Dict[str, Tuple[float, float]]] = None,
    planet_orbs: Optional[Dict[str, float]] = None,
) -> Dict[str, List[Dict[str, Union[str, float]]]]:
    """
    Calculate aspects between planets based on their longitudes.

    Args:
        planet_positions: Dictionary of planet positions (must contain 'longitude').
        aspect_definitions: Custom aspect angles and their type-specific orbs.
                            Defaults to ASPECT_ANGLES.
        planet_orbs: Custom orbs for individual planets. Defaults to DEFAULT_PLANET_ORBS.

    Returns:
        A dictionary where keys are planet names, and values are lists of aspects
        that planet makes, each aspect being a dictionary with
        'aspecting_planet', 'aspect_type', and 'orb'.
    """
    if aspect_definitions is None:
        aspect_definitions = ASPECT_ANGLES
    if planet_orbs is None:
        planet_orbs = DEFAULT_PLANET_ORBS

    aspects_found: Dict[str, List[Dict[str, Union[str, float]]]] = {
        planet: [] for planet in planet_positions if "longitude" in planet_positions[planet]
    }
    
    # Filter out planets for which positions could not be calculated
    valid_planets = [
        p_name for p_name, p_data in planet_positions.items() 
        if isinstance(p_data.get("longitude"), (int, float))
    ]


    for i in range(len(valid_planets)):
        for j in range(i + 1, len(valid_planets)):
            p1_name = valid_planets[i]
            p2_name = valid_planets[j]

            # We've already filtered for valid longitude above
            p1_lon = planet_positions[p1_name]["longitude"]
            p2_lon = planet_positions[p2_name]["longitude"]

            # Ensure they are floats for calculation
            if not (isinstance(p1_lon, (float, int)) and isinstance(p2_lon, (float, int))):
                logger.warning(f"Skipping aspect between {p1_name} and {p2_name} due to missing/invalid longitude.")
                continue

            angular_separation = abs(p1_lon - p2_lon)
            angular_separation = min(angular_separation, 360.0 - angular_separation)  # Shortest arc

            # Determine orb based on planets involved and aspect type
            orb_p1 = planet_orbs.get(p1_name, planet_orbs.get("Default", 5.0))
            orb_p2 = planet_orbs.get(p2_name, planet_orbs.get("Default", 5.0))

            for aspect_name, (target_angle, aspect_type_orb) in aspect_definitions.items():
                # Weighted orb: use the smaller of the aspect's own orb and the average of the two planets' orbs
                # This is a common astrological practice.
                effective_orb = min(aspect_type_orb, (orb_p1 + orb_p2) / 2.0)

                if abs(angular_separation - target_angle) <= effective_orb:
                    exact_orb_value = round(abs(angular_separation - target_angle), ROUND_ORB)
                    
                    aspect_info_p1 = {
                        "aspecting_planet": p2_name,
                        "aspect_type": aspect_name,
                        "orb": exact_orb_value,
                    }
                    aspect_info_p2 = {
                        "aspecting_planet": p1_name,
                        "aspect_type": aspect_name,
                        "orb": exact_orb_value,
                    }
                    # Check if aspects_found has the key, which it should if valid_planets was built correctly
                    if p1_name in aspects_found:
                         aspects_found[p1_name].append(aspect_info_p1)
                    if p2_name in aspects_found:
                         aspects_found[p2_name].append(aspect_info_p2)
    return aspects_found


def assign_planets_to_houses(
    planet_positions: Dict[str, Dict[str, Union[float, str]]], # Expects output from calculate_planet_positions
    house_cusps_deg: List[float], # List of 12 house cusp longitudes in degrees
    house_system_name: str = "WholeSign", # Currently supports "WholeSign" and generic cusp-based
) -> Dict[str, Union[int, str]]:
    """
    Assign planets to astrological houses based on their longitudes and house cusps.

    Args:
        planet_positions: Dictionary of planet positions (must contain 'longitude').
        house_cusps_deg: A list of 12 floats representing house cusp longitudes in degrees,
                         starting with the 1st house cusp (Ascendant).
        house_system_name: Name of the house system used (e.g., "WholeSign", "Placidus").
                           Currently, logic is specific for "WholeSign" or generic cusp systems.

    Returns:
        A dictionary mapping planet names to their house number (1-12) or "Unknown".
        Returns a dictionary with 'error' key on critical failure.
    """
    if len(house_cusps_deg) != 12:
        msg = f"Invalid number of house cusps: {len(house_cusps_deg)}. Expected 12."
        logger.error(msg)
        return {"error": msg}

    # Normalize cusps to ensure they are in [0, 360) range
    # For most systems, cusps are already sorted, but normalization is safe.
    normalized_cusps = [normalize_angle(cusp) for cusp in house_cusps_deg]

    planet_house_assignments: Dict[str, Union[int, str]] = {}

    for planet_name, p_data in planet_positions.items():
        planet_lon = p_data.get("longitude")

        if not isinstance(planet_lon, (float, int)):
            logger.warning(
                f"Longitude missing or invalid for planet {planet_name}. Cannot assign house."
            )
            planet_house_assignments[planet_name] = "Unknown (No Longitude)"
            continue
        
        planet_lon = normalize_angle(planet_lon) # Ensure planet longitude is also normalized
        assigned_house: Union[int, str] = "Unknown (Logic Error)"


        if house_system_name.lower() == "wholesign":
            # The 1st house cusp (Ascendant) determines the start of the 1st house.
            # Each house occupies one full sign (30 degrees).
            asc_lon = normalized_cusps[0]
            # Calculate how many 30-degree segments the planet is from the start of the Ascendant's sign
            relative_longitude = normalize_angle(planet_lon - asc_lon)
            house_number = int(relative_longitude // 30) + 1
            assigned_house = house_number
        else:
            # Generic logic for cusp-based systems (Placidus, Koch, Regiomontanus, Campanus etc.)
            # Assumes normalized_cusps[i] is the cusp of house i+1.
            # House i+1 starts at normalized_cusps[i] and ends at normalized_cusps[(i+1)%12].
            for i in range(12):
                cusp_start = normalized_cusps[i]
                cusp_end = normalized_cusps[(i + 1) % 12] # Next cusp, wraps around for the 12th house

                # Check if planet falls within the house boundaries
                # This handles the case where the house boundary crosses 0° Aries (e.g. cusp_start=350, cusp_end=20)
                if cusp_start <= cusp_end: # Normal case, e.g. house from 10° to 40°
                    if cusp_start <= planet_lon < cusp_end:
                        assigned_house = i + 1
                        break
                else: # Wrap-around case, e.g. house from 350° to 20° (crossing 0° Aries)
                    if planet_lon >= cusp_start or planet_lon < cusp_end:
                        assigned_house = i + 1
                        break
            # If no house assigned after loop (should not happen with valid cusps & planet_lon)
            if assigned_house == "Unknown (Logic Error)" and i == 11 :
                 logger.error(f"Planet {planet_name} at {planet_lon}° could not be assigned to a house with cusps: {normalized_cusps} using {house_system_name} system.")


        planet_house_assignments[planet_name] = assigned_house
    return planet_house_assignments


# --- Example Main Usage ---
if __name__ == "__main__":
    try:
        logger.info("--- Starting Astrological Calculations Example ---")
        
        # Note: set_ephemeris_path() is now called within calculate_planet_positions.
        # You can pass ephe_path_override to it if needed.
        # For this example, we rely on the default EPHEMERIS_PATH or SWISS_EPHE_PATH env var.
        # If EPHEMERIS_PATH is not correctly set, calculate_planet_positions will return an error.
        
        # Example: Calculate for a specific date, time, and location
        target_year = 2025
        target_month = 7
        target_day = 1
        target_hour = 12
        target_minute = 0
        # New York City coordinates
        observer_lat = 40.7128
        observer_lon = -74.0060
        observer_alt = 10.0 # Altitude in meters
        tz_string = "America/New_York"

        logger.info(
            f"Calculating positions for: {target_year}-{target_month:02d}-{target_day:02d} "
            f"{target_hour:02d}:{target_minute:02d} {tz_string} "
            f"at Lat {observer_lat}, Lon {observer_lon}"
        )

        planet_positions_result = calculate_planet_positions(
            target_year, target_month, target_day, target_hour, target_minute,
            observer_lat, observer_lon, observer_alt,
            timezone_str=tz_string,
            # ephe_path_override="/path/to/my/ephe" # Optionally override here
        )

        if "error" in planet_positions_result:
            logger.error(f"Failed to calculate planet positions: {planet_positions_result['error']}")
        else:
            print("\n--- Planet Positions ---")
            for planet_name, data_dict in planet_positions_result.items():
                if "error" in data_dict:
                     print(f"  {planet_name:<10}: {data_dict['error']}")
                elif isinstance(data_dict, dict): # Check if data_dict is indeed a dictionary
                    lon = data_dict.get('longitude', 'N/A')
                    lat = data_dict.get('latitude', 'N/A')
                    sign = data_dict.get('sign', 'N/A')
                    speed = data_dict.get('speed_longitude', 'N/A')
                    retro = "R" if isinstance(speed, (float,int)) and speed < 0 else ""
                    print(f"  {planet_name:<10}: Lon={lon:>8}° {str(sign):<11} Lat={lat:>8}° Speed={speed:>8}°/day {retro}")
                else:
                    print(f"  {planet_name:<10}: Invalid data format.")


            # --- House Calculation (Example with Whole Sign) ---
            # In a real app, you'd calculate house cusps using swe.houses()
            # For Whole Sign, the Ascendant's longitude defines the first cusp.
            # Let's assume an Ascendant at 15° Leo for this example for Whole Sign.
            # (This would normally come from a call to swe.houses)
            ascendant_longitude = 15.0 + 30.0 * 4 # 15° Leo
            
            # For Whole Sign, all cusps start at the same degree as the Ascendant in their respective signs
            # house_cusps_ws = [normalize_angle(ascendant_longitude + 30.0 * i) for i in range(12)]
            # No, for Whole Sign, the first cusp defines the *sign* of the first house. All houses start at 0° of their sign.
            # If ASC is 15 Leo, 1st house is Leo, 2nd is Virgo etc. Cusp list for Whole Sign is effectively 0 Aries, 0 Taurus ...
            # if we want planets placed based on the sign of the ASC.
            # A more direct way for Whole Sign:
            #   1. Find sign of ASC. That's House 1.
            #   2. Each planet's sign relative to ASC sign determines house.
            # However, the function `assign_planets_to_houses` with "WholeSign" system and
            # the first cusp `normalized_cusps[0]` (which is `asc_lon`) does this calculation correctly.
            # So, providing the actual ascendant longitude as the first cusp is correct for that implementation.
            
            logger.info(f"\nAssuming Ascendant at {degree_to_sign(ascendant_longitude)} {ascendant_longitude % 30:.2f}° for Whole Sign house example.")
            # For WholeSign with an Ascendant at 15 Leo, the cusps are effectively:
            # 1st: 15 Leo, 2nd: 15 Virgo, ..., 12th: 15 Cancer
            # No, this is incorrect for traditional Whole Sign. Traditional Whole Sign houses are the signs themselves.
            # If Ascendant is in Leo, Leo is the 1st house.
            # The provided `assign_planets_to_houses` for "WholeSign" expects the ASC longitude as the first cusp
            # and then calculates offsets. `offset = (lon - start_cusp) % 360; house_num = int(offset // 30) + 1`
            # This means if ASC is 15 Leo (135 deg), and a planet is 160 deg (Virgo), offset = (160-135)%360 = 25. house_num = int(25//30)+1 = 1. Correct.
            # If planet is 130 deg (Leo), offset = (130-135)%360 = -5%360 = 355. house_num = int(355//30)+1 = 11+1 = 12. No, this is not right for standard Whole Sign.

            # Re-evaluating Whole Sign cusps for the function:
            # The function `assign_planets_to_houses` for "WholeSign" calculates `offset = (lon - start_cusp) % 360`, then `house_num = int(offset // 30) + 1`.
            # If `start_cusp` is the degree of the Ascendant (e.g., 135° for 15° Leo):
            # - Planet at 136° (1° into Leo from ASC): offset = 1, house_num = 1. Correct.
            # - Planet at 164° (29° into Leo from ASC): offset = 29, house_num = 1. Correct.
            # - Planet at 166° (1° into Virgo from ASC): offset = 31, house_num = 2. Correct.
            # So, the `house_cusps_deg` for `assign_planets_to_houses` with "WholeSign"
            # should simply be `[ascendant_longitude, (ascendant_longitude+30)%360, ...]`
            # Or, more simply, the first element is the most important for this mode.
            # The example `house_cusps = [0.0 + 30 * i for i in range(12)]` in the original code
            # implies an Aries rising chart for Whole Sign using that logic.

            # For a clear Whole Sign example based on an Ascendant:
            # Let's use a Placidus calculation to get an Ascendant for our example time/place
            # This requires `swe.houses_ex` or `swe.houses`
            jd_for_houses = swe.julday(target_year, target_month, target_day, target_hour + target_minute / 60.0)
            if tz_string: # if local time was given, convert jd to match what swe.houses expects (usually UT)
                dt_utc_for_houses = local_to_utc(target_year, target_month, target_day, target_hour, target_minute, tz_string)
                jd_for_houses = calculate_julian_day_utc(dt_utc_for_houses)

            # Calculate Placidus houses to get an Ascendant
            # swe.houses_ex returns (cusps[1..12], ascmc[0..9], serr)
            # ascmc[0] = Ascendant, ascmc[1] = MC
            # Default house system for swe.houses is 'P' (Placidus)
            _cusps, ascmc, _serr_h = swe.houses_ex(jd_for_houses, observer_lat, observer_lon, flags=swe.FLG_SWIEPH) # Use flags for ephemeris type
            actual_asc_lon = normalize_angle(ascmc[0])
            actual_mc_lon = normalize_angle(ascmc[1])
            logger.info(f"\nCalculated Ascendant (Placidus): {actual_asc_lon:.2f}° ({degree_to_sign(actual_asc_lon)})")
            logger.info(f"Calculated Midheaven (Placidus): {actual_mc_lon:.2f}° ({degree_to_sign(actual_mc_lon)})")

            # Create house cusps for Whole Sign based on the actual Ascendant's sign
            # The first house (Whole Sign) starts at 0 degrees of the Ascendant's sign.
            asc_sign_start_lon = (actual_asc_lon // 30) * 30
            house_cusps_for_whole_sign = [normalize_angle(asc_sign_start_lon + 30.0 * i) for i in range(12)]

            # For the assign_planets_to_houses function with "WholeSign", the crucial element is the first cusp.
            # It should be the degree of the Ascendant if you want houses to start from the Ascendant degree.
            # Or 0 degrees of the Ascendant's sign if you want traditional Whole Sign Houses.
            # The current implementation: `offset = (lon - start_cusp) % 360; house_num = int(offset // 30) + 1`
            # This means `start_cusp` should be the degree of the Ascendant for the 1st house to *begin* at the Ascendant.
            # For traditional Whole Sign (1st house = sign of Asc), `start_cusp` should be 0° of the Ascendant's sign.

            # Let's demonstrate with traditional Whole Sign Houses:
            traditional_ws_start_cusp = (actual_asc_lon // 30) * 30.0 # 0 degrees of the Ascendant's sign
            # The list of cusps for assign_planets_to_houses for this interpretation of WholeSign should be:
            # [0_deg_of_ASC_sign, 0_deg_of_next_sign, ...]
            # The current function's "WholeSign" mode effectively uses the *first cusp provided* as the "0 point"
            # and segments 30 deg from there. So, to get traditional whole sign, the first cusp needs to be 0° of the ASC's sign.
            
            traditional_whole_sign_cusps_input = [normalize_angle(traditional_ws_start_cusp + 30.0 * i) for i in range(12)]

            print(f"\n--- Planet House Assignments (Traditional Whole Sign, 1st house = {degree_to_sign(traditional_ws_start_cusp)}) ---")
            house_assignments = assign_planets_to_houses(
                planet_positions_result,
                traditional_whole_sign_cusps_input, # Provide the list starting with 0° of Ascendant's sign
                house_system_name="WholeSign" 
            )
            if "error" in house_assignments:
                logger.error(f"House assignment failed: {house_assignments['error']}")
            else:
                for planet_name, house_num in house_assignments.items():
                    print(f"  {planet_name:<10}: House {house_num}")

            # --- Aspect Calculation ---
            print("\n--- Aspects ---")
            aspect_results = calculate_aspects(planet_positions_result)
            for planet_name, aspect_list in aspect_results.items():
                if aspect_list: # Only print if there are aspects
                    print(f"  {planet_name}:")
                    for aspect_detail in aspect_list:
                        print(
                            f"    - {aspect_detail['aspect_type']} with "
                            f"{aspect_detail['aspecting_planet']} "
                            f"(orb: {aspect_detail['orb']:.2f}°)"
                        )
                # else:
                #     print(f"  {planet_name}: No aspects found.")
        
        logger.info("\n--- Astrological Calculations Example Finished ---")

    except FileNotFoundError as e:
        # This can be raised by set_ephemeris_path if called at the top level,
        # or if calculate_planet_positions re-raises it.
        logger.critical(f"CRITICAL: Ephemeris files not found. Please check configuration. Error: {e}")
        print(f"Error: Ephemeris files not found. Please ensure SWISS_EPHE_PATH is set correctly or ephemeris files are at {EPHEMERIS_PATH}.", file=sys.stderr)
    except Exception as e: # General catch-all for the main script execution
        logger.error(f"A fatal error occurred in the main execution: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}", file=sys.stderr)