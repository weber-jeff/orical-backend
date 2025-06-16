import sys
import swisseph as swe
import json
from pathlib import Path
from typing import Optional, Dict
import logging
from aspects import calculate_aspects
from houses import assign_planets_to_houses
from ephemeris_manager import set_ephemeris_path

# --- Setup logger ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Safe loader for JSON meaning files ---
def safe_load_meaning(filepath: Path) -> dict:
    if not filepath.is_file():
        logger.warning(f"Meaning file not found: {filepath}")
        return {}

    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as jde:
        logger.warning(f"JSON decode error in {filepath}: {jde}")
    except Exception as e:
        logger.warning(f"Failed to load meaning file {filepath}: {e}")
    return {}

# --- Load all astrology meaning files at once ---
def load_all_meanings(base_path: Optional[Path] = None) -> Dict[str, dict]:
    if base_path is None:
        base_path = (Path(__file__).parent.parent / "astro_data" / "meanings").resolve()

    if not base_path.exists() or not base_path.is_dir():
        logger.error(f"Meaning base path not found or not a directory: {base_path}")
        raise FileNotFoundError(f"Meaning base path not found or not a directory: {base_path}")

    meaning_files = {
        "aspect_meanings": "aspect_meanings.json",
        "planet_meanings": "planet_meanings.json",
        "house_meanings": "house_meanings.json",
        "rising_sign_meanings": "rising_sign_meanings.json",
        "moon_sign_meanings": "moon_sign_meanings.json",
        "sign_meanings": "sign_meanings.json",
        "element_meanings": "element_meanings.json",
        "modality_meanings": "modality_meanings.json",
        "p_aspects": "p_aspects.json",
        "planet_in_house_meanings": "planet_in_house_meanings.json",
        "planet_in_sign": "planet_in_sign.json",
    }

    meanings = {}
    for key, filename in meaning_files.items():
        full_path = base_path / filename
        meanings[key] = safe_load_meaning(full_path)
        if not meanings[key]:
            logger.warning(f"Meaning file '{filename}' loaded empty or failed.")
    return meanings

# --- Attempt to import core astrology modules, fallback to stubs ---
try:
    from astrology.astro_data.load_meanings import MeaningLoader, get_aspect_report, get_house_report_string
    from astrology.astro_data.glyphs import aspect_glyphs
    from astrology.core_astrology.birth_chart import (
        generate_birth_chart,
        get_planet_positions,
        get_sun_sign,
        get_moon_sign,
        get_sign_details,
        degree_to_sign,
        element,
        modality,
        calculate_aspects_within_chart,
        PLANET_NAMES,
        ASPECT_ANGLES,
        ASPECT_TYPES,
    )
except ImportError as e:
    logger.warning(f"Some astrology imports failed: {e}")
    MeaningLoader = None
    aspect_glyphs = {}
    get_aspect_report = lambda x: f"Aspect report unavailable for {x}"
    get_house_report_string = lambda x: f"House {x} report unavailable"
    def generate_birth_chart(*args, **kwargs):
        return {"error": "Birth chart generation unavailable"}
    def get_planet_positions(*args, **kwargs):
        return {}
    get_sun_sign = lambda m, d: "Unknown"
    get_moon_sign = lambda y, m, d, h, mi, lat, lon, alt=0: "Unknown"
    get_sign_details = lambda sign: {}
    degree_to_sign = lambda lon: "Unknown"
    element = lambda x: "Unknown"
    modality = lambda x: "Unknown"
    calculate_aspects_within_chart = lambda chart, aspects: []
    PLANET_NAMES, ASPECT_ANGLES, ASPECT_TYPES = {}, {}, {}

meanings = load_all_meanings()

# --- Utility function for formatting planetary longitude ---
def format_longitude(lon: Optional[float]) -> str:
    if lon is None:
        return "Unknown"
    sign_name = degree_to_sign(lon)
    deg_in_sign = lon % 30
    degrees = int(deg_in_sign)
    minutes_full = (deg_in_sign - degrees) * 60
    minutes = int(minutes_full)
    seconds = int((minutes_full - minutes) * 60)
    return f"{degrees:02d}° {sign_name} {minutes:02d}'{seconds:02d}\""

# --- Constants for planet codes used in Swiss Ephemeris ---
PLANET_LIST_FOR_REPORT = {
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
    "Chiron": swe.CHIRON,
    "TrueNode": swe.TRUE_NODE,
}

# --- Main astrology report generator ---
def generate_astrology_report(year: int, month: int, day: int,
                              hour: int, minute: int,
                              lon: float, lat: float,
                              ut_offset: float = 0.0,
                              alt: float = 0) -> str:
    chart_data = generate_birth_chart(
        year, month, day, hour, minute,
        timezone_str="UTC",
        lat=lat, lon=lon, alt=alt
    )

    if "error" in chart_data:
        logger.error(f"Error generating birth chart: {chart_data['error']}")
        return f"Error generating birth chart: {chart_data['error']}"

    planet_positions = chart_data.get("planet_positions", {})
    sun_long = planet_positions.get("Sun", {}).get("longitude")
    sun_sign = degree_to_sign(sun_long) if isinstance(sun_long, float) else "Unknown"
    sun_in_sign_meaning = meanings.get("planet_in_sign_meanings", {}).get("Sun", {}).get(sun_sign, "No specific meaning available for Sun in this sign.")

    moon_sign = chart_data.get("moon_sign", "Unknown")
    ascendant = chart_data.get("ascendant_longitude")
    asc_deg_str = format_longitude(ascendant)
    mc_longitude = chart_data.get("mc_longitude")
    vertex_longitude = chart_data.get("vertex_longitude")

    # Aspects
    aspects = chart_data.get("aspects", {})
    aspect_lines = []
    for planet, aspect_list in aspects.items():
        for aspect in aspect_list:
            aspect_type = aspect.get("aspect_type")
            aspecting = aspect.get("aspecting_planet")
            orb = aspect.get("orb")
            glyph = aspect_glyphs.get(aspect_type, aspect_type)
            aspect_lines.append(f"{planet} {glyph} {aspecting} (orb: {orb:.2f})")

    report_lines = [
        f"--- Astrology Report ---",
        f"Birth Date/Time (UTC): {chart_data.get('birth_datetime_utc', 'N/A')}",
        f"Location: Lat {chart_data.get('geo_location', {}).get('latitude')}, Lon {chart_data.get('geo_location', {}).get('longitude')}",
        "",
        f"🌞 Sun in {sun_sign} — {sun_in_sign_meaning}",
        f"🌙 Moon in {moon_sign}",
        f"⬆️ Ascendant at {asc_deg_str}",
        f"⬇️ Midheaven at {format_longitude(mc_longitude)}",
        f"✅ Vertex at {format_longitude(vertex_longitude)}",
        "",
        "⚡ Aspects:",
        *aspect_lines,
        "",
        "🏠 House Positions (todo)",
        "🪐 Planetary Archetypes (todo)"
    ]
    return "\n".join(report_lines)
