import os
import json
from functools import lru_cache
from typing import Optional, Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class MeaningLoader:
    def __init__(
        self,
        base_dir: Optional[str] = None,
        meaning_files: Optional[List[str]] = None,
        alias_map: Optional[Dict[str, str]] = None,
    ):
        # Resolve base_dir relative to this file if not provided
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meanings")
        self.base_dir = base_dir

        # Default alias_map, can be extended externally if needed
        self.alias_map = alias_map or {}

        if not os.path.isdir(self.base_dir):
            raise FileNotFoundError(f"Meaning directory not found: {self.base_dir}")

        # Default meaning files list, can be overridden via constructor arg
        self.meaning_files = meaning_files or [
            "element_meanings",
            "house_meanings",
            "aspect_meanings",
            "modality_meanings",
            "rising_sign_meanings",
            "p_aspect_p",
            "sign_meanings",
            "moon_sign_meanings",
            "planet_sign_meanings",
            "planet_in_house",
            "planet_in_sign",
        ]

    def _build_path(self, filename: str) -> str:
        if not filename.endswith(".json"):
            filename += ".json"
        return os.path.join(self.base_dir, filename)

    @lru_cache(maxsize=64)
    def _load_file(self, filename: str) -> Optional[Dict[str, Any]]:
        # Support aliasing for flexible filename mapping
        filename_to_load = self.alias_map.get(filename, filename)
        path = self._build_path(filename_to_load)

        if not os.path.isfile(path):
            logger.warning(f"Meaning file '{filename}' (resolved to '{filename_to_load}') not found at '{path}'.")
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded '{filename_to_load}' successfully from '{path}'.")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in file '{path}': {e}")
        except Exception as e:
            logger.error(f"Error loading meaning file '{path}': {e}")

        return None

    def get_meaning(self, file: str, key1: str, key2: Optional[str] = None, default: Any = None) -> Any:
        """
        Retrieve meaning data from a JSON file.
        If key2 is provided, returns nested dictionary value.
        Returns `default` if not found.
        """
        data = self._load_file(file)
        if not data:
            logger.debug(f"File '{file}' not loaded or empty.")
            return default

        if key2 is not None:
            return data.get(key1, {}).get(key2, default)
        return data.get(key1, default)

    def get_full_meaning(self, file: str) -> Dict[str, Any]:
        """Return entire dictionary content from the meaning file, or empty dict if missing."""
        data = self._load_file(file)
        if data is None:
            logger.debug(f"File '{file}' missing or empty, returning empty dict.")
            return {}
        return data

    def list_available_files(self) -> List[str]:
        """List all JSON meaning files available in the base directory."""
        try:
            return [f for f in os.listdir(self.base_dir) if f.endswith(".json")]
        except Exception as e:
            logger.error(f"Failed to list meaning files: {e}")
            return []

    def preload_all_meanings(self) -> Dict[str, Dict[str, Any]]:
        """Load all default meaning files at once into a dictionary."""
        all_meanings = {}
        for filename in self.meaning_files:
            data = self._load_file(filename)
            if data:
                all_meanings[filename] = data
            else:
                logger.warning(f"Meaning file '{filename}' could not be loaded or is empty.")
        return all_meanings


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loader = MeaningLoader()

    # Smart usage examples with clear distinction between planet core profiles and planet-in-sign meanings

    # 1. Retrieve a specific planet-in-sign meaning (e.g., Sun in Aries)
    sun_in_aries = loader.get_meaning("planet_in_sign", "Sun", "Aries", default="Meaning not found.")
    print(f"Sun in Aries meaning:\n{sun_in_aries}\n")

    # 2. Retrieve the full 'planet_in_house' dictionary and show keys
    full_planet_in_house = loader.get_full_meaning("planet_in_house")
    print(f"Full 'planet_in_house' meanings loaded. Keys: {list(full_planet_in_house.keys())}\n")

    # 3. Generate a dynamic report combining planet core meanings and their sign-specific meanings
    planet_positions = {
        "Sun": {"sign": "Aries"},
        "Moon": {"sign": "Cancer"},
        "Mercury": {"sign": "Taurus"},
    }

    # Load full core planet profiles once
    planet_core_profiles = loader.get_full_meaning("planet_sign_meanings")
    # Load full planet-in-sign meanings once
    planet_in_sign_meanings = loader.get_full_meaning("planet_in_sign")

    report = {"planets": {}}

    for planet, info in planet_positions.items():
        sign = info.get("sign")

        # Core profile for the planet (e.g., generic Sun traits)
        core_profile = planet_core_profiles.get(planet, {})

        # Sign-specific meaning of the planet (e.g., Sun in Aries)
        sign_meaning = planet_in_sign_meanings.get(planet, {}).get(sign, "Meaning not found.")

        report["planets"][planet] = {
            "core_profile": core_profile,
            "sign_meaning": sign_meaning,
        }

    print("Generated combined planet report snippet:\n", json.dumps(report, indent=4))
