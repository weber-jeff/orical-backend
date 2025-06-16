# fusion_logic.py

def fusion_overlap_score(numerology_number: int, encoded_astro_vector: list[int]) -> int:
    """
    Score based on how many astrology codes overlap with numerology core number.
    Simple rule: match or divisible.

    Args:
        numerology_number: Core numerology number (e.g., Life Path)
        encoded_astro_vector: List of astrology-derived integers

    Returns:
        Integer score (0+)
    """
    return sum(1 for code in encoded_astro_vector if code == numerology_number or code % numerology_number == 0)

def is_favorable_alignment(numerology_number: int, astro_vector: list[int], threshold: int = 3) -> bool:
    """
    Decide if numerology + astrology match is strong enough for recommendations.

    Args:
        numerology_number: e.g., Life Path number
        astro_vector: List of encoded astrological IDs
        threshold: Minimum match count

    Returns:
        True if match is strong enough, False otherwise.
    """
    return fusion_overlap_score(numerology_number, astro_vector) >= threshold
