import os
import logging
import swisseph as swe
import urllib.request
import zipfile

logger = logging.getLogger(__name__)

DEFAULT_EPHEMERIS_PATH = os.getenv(
    "EPHEMERIS_PATH", "/media/jeff/numy/numerology_ai/astrology/mp"
)

EPHEMERIS_ZIP_URL = "https://www.astro.com/swisseph/swepha.zip"

_ephe_path_set = False
_current_path = None

def ephemeris_files_exist(path: str) -> bool:
    expected_files = [
        "sepl_18.se1",
        "seas_18.se1",
        "semo_18.se1",
    ]
    results = []
    for f in expected_files:
        file_path = os.path.join(path, f)
        exists = os.path.isfile(file_path)
        results.append(exists)
        logger.debug(f"Checking ephemeris file {file_path}: {'Found' if exists else 'Missing'}")
    return all(results)

def download_and_extract_ephemeris(dest_path: str):
    os.makedirs(dest_path, exist_ok=True)
    zip_path = os.path.join(dest_path, "swepha.zip")
    logger.info(f"Downloading Swiss Ephemeris files from {EPHEMERIS_ZIP_URL}...")
    urllib.request.urlretrieve(EPHEMERIS_ZIP_URL, zip_path)
    logger.info("Extracting ephemeris files...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    os.remove(zip_path)
    logger.info("Ephemeris files downloaded and extracted.")

def set_ephemeris_path(ephe_path: str = None, auto_download: bool = False, force_reset: bool = False) -> str:
    global _ephe_path_set, _current_path

    if _ephe_path_set and not force_reset:
        logger.debug(f"Ephemeris path already set to {_current_path}, skipping reset.")
        return _current_path

    path = ephe_path or DEFAULT_EPHEMERIS_PATH

    if os.path.isdir(path):
        if not ephemeris_files_exist(path):
            logger.warning(f"Ephemeris files missing in {path}.")
            if auto_download:
                logger.info("Attempting to auto-download missing ephemeris files...")
                download_and_extract_ephemeris(path)
            else:
                raise FileNotFoundError(f"Ephemeris files missing in {path} and auto_download=False.")
        if not ephemeris_files_exist(path):
            raise FileNotFoundError(f"Ephemeris files still missing after download attempt at {path}.")

        swe.set_ephe_path(path)
        _ephe_path_set = True
        _current_path = path
        logger.info(f"Ephemeris path set to {path}")
    else:
        logger.error(f"[Ephemeris Manager] Invalid path: {path}. Ensure ephemeris files are extracted here.")
        raise FileNotFoundError(f"Ephemeris path not found: {path}")

    return path

def get_ephemeris_path() -> str:
    return _current_path or ""
