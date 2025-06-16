from datetime import datetime
from typing import Optional, Union
import logging

# Use the standard library zoneinfo module (available in Python 3.9+)
from zoneinfo import ZoneInfo
import json
import os


# Define file path
BASE_DIR = os.path.dirname(__file__)
ASPECTS_PATH = os.path.join(BASE_DIR, "../astro_data/meanings/aspect_meanings.json")

# Load the JSON file first
with open(ASPECTS_PATH, "r") as f:
    ASPECTS = json.load(f)

# Then define the function
def get_aspect_details(aspect_name: str) -> dict:
    return ASPECTS.get(aspect_name, {})

# Example call – optional for testing, remove if not needed globally
if __name__ == "__main__":
    aspect = get_aspect_details("Conjunction")
    print(aspect["meaning"])

logger = logging.getLogger(__name__)

# Constants
_ZODIAC_SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)

def normalize_angle(angle: float) -> float:
    """
    Normalize an angle to the range [0, 360).

    Args:
        angle (float): The angle in degrees.

    Returns:
        float: Normalized angle in degrees.
    """
    normalized = angle % 360
    logger.debug(f"normalize_angle: input={angle}, normalized={normalized}")
    return normalized

def degree_to_sign(degree: float) -> str:
    """
    Convert an ecliptic longitude degree to its corresponding zodiac sign.

    Args:
        degree (float): Ecliptic longitude in degrees (0-360).

    Returns:
        str: Zodiac sign name.
    
    Raises:
        ValueError: If degree is not within 0-360 (after normalization).
    """
    if not isinstance(degree, (int, float)):
        raise TypeError("degree must be a number")
    
    degree = normalize_angle(degree)
    index = int(degree // 30)
    sign = _ZODIAC_SIGNS[index]
    logger.debug(f"degree_to_sign: degree={degree}, sign={sign}")
    return sign

def local_to_utc(
    year: int, month: int, day: int, hour: int, minute: int, timezone_str: str
) -> datetime:
    """
    Convert local datetime to UTC datetime.

    Args:
        year (int): Year of the local time.
        month (int): Month of the local time.
        day (int): Day of the local time.
        hour (int): Hour of the local time (0-23).
        minute (int): Minute of the local time (0-59).
        timezone_str (str): Timezone string (e.g., "America/New_York").

    Returns:
        datetime: UTC datetime object.

    Raises:
        Exception: If timezone string is invalid or conversion fails.
    """
    try:
        tz = ZoneInfo(timezone_str)
    except Exception as e:
        logger.error(f"Invalid timezone string: {timezone_str} - {e}")
        raise ValueError(f"Invalid timezone string: {timezone_str}") from e

    local_dt = datetime(year, month, day, hour, minute, 0, tzinfo=tz)
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    logger.debug(f"local_to_utc: local={local_dt}, utc={utc_dt}")
    return utc_dt

def calculate_julian_day(dt_utc: Union[datetime, None] = None,
                         year: Optional[int] = None,
                         month: Optional[int] = None,
                         day: Optional[int] = None,
                         hour: Optional[int] = 0,
                         minute: Optional[int] = 0,
                         second: Optional[int] = 0) -> float:
    """
    Calculate the Julian Day for a given UTC datetime or date components.

    Args:
        dt_utc (datetime, optional): UTC datetime object.
        year (int, optional): Year if dt_utc not provided.
        month (int, optional): Month if dt_utc not provided.
        day (int, optional): Day if dt_utc not provided.
        hour (int, optional): Hour (default 0).
        minute (int, optional): Minute (default 0).
        second (int, optional): Second (default 0).

    Returns:
        float: Julian Day number.

    Raises:
        ValueError: If insufficient or invalid date/time info provided.
    """
    import swisseph as swe

    if dt_utc is not None:
        year = dt_utc.year
        month = dt_utc.month
        day = dt_utc.day
        hour = dt_utc.hour
        minute = dt_utc.minute
        second = dt_utc.second
    else:
        if None in (year, month, day):
            raise ValueError("Must provide either dt_utc or year, month, and day")

    decimal_hour = hour + (minute / 60.0) + (second / 3600.0)
    jd = swe.julday(year, month, day, decimal_hour)
    logger.debug(f"calculate_julian_day: year={year}, month={month}, day={day}, hour={decimal_hour}, jd={jd}")
    return jd
