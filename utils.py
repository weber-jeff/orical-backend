# /media/jeff/numy/numerology_ai/numerology/numerology_report.py
import os
import sys
import datetime # For get_numerological_insights and __main__ examples
from collections import Counter # For Hidden Passion
import json
# --- Section 1: Setup for Importing Compatibility Data (SIMPLIFIED) ---
# Now we only need to import one comprehensive dictionary from combat1.py




# --- Section 2: Core Numerology Calculation Logic ---
# (This section remains the same: PYTHAGOREAN_MAP, VOWELS, reduce_number, 
#  calculate_life_path, calculate_expression_number, etc. ...
#  get_reduced_date_components, calculate_balance_number, calculate_maturity_number,
#  calculate_challenge_numbers, calculate_pinnacle_numbers, calculate_hidden_passion_number)
# For brevity, not re-pasting all these functions here. Ensure they are present.
# --- Letter to Number Mappings (Standardized) ---
PYTHAGOREAN_MAP = {
    'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2, 'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4, 'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8, 'I': 9, 'R': 9
}
VOWELS = "AEIOU"
def reduce_number(n: int, keep_master_as_is=True) -> int:
    if keep_master_as_is and n in [11, 22, 33]: return n
    s = str(n)
    while len(s) > 1:
        current_sum = sum(int(digit) for digit in s)
        if keep_master_as_is and current_sum in [11, 22, 33] and len(str(current_sum)) == 2:
            return current_sum
        s = str(current_sum)
        if len(s) == 1: break 
    return int(s)

def load_json_file(filepath):
    """Loads a JSON file and returns the data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
    
    
def safe_get(dictionary, key, default=None):
    return dictionary.get(key, default)

def get_number_from_string(text: str, letter_map: dict) -> int:
    total = 0
    for char in text.upper():
        if char in letter_map: total += letter_map[char]
    return total
def calculate_life_path(birth_date_str: str) -> int | str:
    try:
        all_digits_sum = sum(int(digit) for digit in birth_date_str.replace('-', ''))
        return reduce_number(all_digits_sum)
    except ValueError: return "Invalid Date Format"
    except Exception as e: return f"Error calculating Life Path: {e}"
def calculate_expression_number(full_name_str: str) -> int | str:
    try:
        name_for_calc = "".join(filter(str.isalpha, full_name_str))
        if not name_for_calc: return "Name Required"
        name_sum = get_number_from_string(name_for_calc, PYTHAGOREAN_MAP)
        return reduce_number(name_sum)
    except Exception as e: return f"Error calculating Expression: {e}"
def calculate_soul_urge_number(full_name_str: str) -> int | str:
    try:
        name_for_calc = "".join(filter(str.isalpha, full_name_str))
        vowel_str = "".join(char for char in name_for_calc.upper() if char in VOWELS)
        if not vowel_str: return 0
        vowel_sum = get_number_from_string(vowel_str, PYTHAGOREAN_MAP)
        return reduce_number(vowel_sum)
    except Exception as e: return f"Error calculating Soul Urge: {e}"
def calculate_personality_number(full_name_str: str) -> int | str:
    try:
        name_for_calc = "".join(filter(str.isalpha, full_name_str))
        consonant_str = "".join(char for char in name_for_calc.upper() if char.isalpha() and char not in VOWELS and char in PYTHAGOREAN_MAP)
        if not consonant_str: return 0
        consonant_sum = get_number_from_string(consonant_str, PYTHAGOREAN_MAP)
        return reduce_number(consonant_sum)
    except Exception as e: return f"Error calculating Personality: {e}"
def calculate_birthday_number(birth_date_str: str) -> int | str:
    try:
        day_str = birth_date_str.split('-')[2]
        return reduce_number(int(day_str))
    except (ValueError, IndexError): return "Invalid Date Format for Birthday"
    except Exception as e: return f"Error calculating Birthday: {e}"
def get_reduced_date_components(birth_date_str: str) -> tuple[int|str, int|str, int|str] | str:
    try:
        parts = birth_date_str.split('-')
        if len(parts) != 3: raise ValueError("Date must be YYYY-MM-DD")
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        r_month = reduce_number(month, keep_master_as_is=True)
        r_day = reduce_number(day, keep_master_as_is=True)
        year_sum_digits = sum(int(d) for d in str(year))
        r_year = reduce_number(year_sum_digits, keep_master_as_is=True)
        return r_month, r_day, r_year
    except ValueError as ve: return f"Invalid date component: {ve}"
    except Exception as e: return f"Error reducing date components: {e}"
def calculate_balance_number(full_name_str: str) -> int | str:
    try:
        name_parts = full_name_str.upper().split()
        if not name_parts: return "Name Required"
        initials_sum = 0
        for part in name_parts:
            if part and part[0].isalpha() and part[0] in PYTHAGOREAN_MAP:
                initials_sum += PYTHAGOREAN_MAP[part[0]]
        if initials_sum == 0 and full_name_str: return "Could not derive initials"
        elif initials_sum == 0 and not full_name_str: return "Name Required"
        return reduce_number(initials_sum)
    except Exception as e: return f"Error calculating Balance Number: {e}"
def calculate_maturity_number(life_path_num: int, expression_num: int) -> int | str:
    if not (isinstance(life_path_num, int) and isinstance(expression_num, int)):
        return "Valid Life Path and Expression numbers required"
    maturity_sum = life_path_num + expression_num
    return reduce_number(maturity_sum)
def calculate_challenge_numbers(birth_date_str: str) -> list[int | str] | str:
    components = get_reduced_date_components(birth_date_str)
    if isinstance(components, str): return f"Cannot calculate Challenges: {components}"
    r_month, r_day, r_year = components
    sd_month = reduce_number(r_month, keep_master_as_is=False)
    sd_day = reduce_number(r_day, keep_master_as_is=False)
    sd_year = reduce_number(r_year, keep_master_as_is=False)
    if not all(isinstance(i, int) for i in [sd_month, sd_day, sd_year]):
         return "Invalid date components for Challenges after reduction."
    try:
        challenge1 = reduce_number(abs(sd_month - sd_day), keep_master_as_is=False)
        challenge2 = reduce_number(abs(sd_day - sd_year), keep_master_as_is=False)
        main_challenge3 = reduce_number(abs(challenge1 - challenge2), keep_master_as_is=False)
        challenge4 = reduce_number(abs(sd_month - sd_year), keep_master_as_is=False)
        return [challenge1, challenge2, main_challenge3, challenge4]
    except Exception as e: return f"Error calculating Challenges: {e}"
def calculate_pinnacle_numbers(birth_date_str: str) -> list[int | str] | str:
    components = get_reduced_date_components(birth_date_str)
    if isinstance(components, str): return f"Cannot calculate Pinnacles: {components}"
    r_month, r_day, r_year = components
    if not all(isinstance(i, int) for i in [r_month, r_day, r_year]):
         return "Invalid date components for Pinnacles."
    try:
        pinnacle1 = reduce_number(r_month + r_day)
        pinnacle2 = reduce_number(r_day + r_year)
        pinnacle3 = reduce_number(pinnacle1 + pinnacle2)
        pinnacle4 = reduce_number(r_month + r_year)
        return [pinnacle1, pinnacle2, pinnacle3, pinnacle4]
    except Exception as e: return f"Error calculating Pinnacles: {e}"
def calculate_hidden_passion_number(full_name_str: str) -> list[int] | str:
    try:
        name_for_calc = "".join(filter(str.isalpha, full_name_str))
        if not name_for_calc: return "Name Required"
        all_digits_in_name = [PYTHAGOREAN_MAP[char] for char in name_for_calc.upper() if char in PYTHAGOREAN_MAP]
        if not all_digits_in_name: return "No valid letters for Hidden Passion"
        digit_counts = Counter(all_digits_in_name)
        if not digit_counts: return "No digits counted for Hidden Passion"
        max_freq = max(digit_counts.values()) if digit_counts else 0
        hidden_passions = sorted([num for num, count in digit_counts.items() if count == max_freq])
        return hidden_passions if hidden_passions else "No dominant digit found"
    except Exception as e: return f"Error calculating Hidden Passion: {e}"


# --- Section 3: Daily Insights Functions ---
# (This section remains the same)
# For brevity, not re-pasting. Ensure it's present.
def reduce_number_simple(n):
    s = str(n)
    while len(s) > 1: s = str(sum(int(digit) for digit in s))
    return int(s)
def get_numerological_insights(birth_month, birth_day, target_date_obj):
    try:
        personal_day = reduce_number_simple(birth_month + birth_day + target_date_obj.day)
        personal_month = reduce_number_simple(birth_month + target_date_obj.month)
        personal_year = reduce_number_simple(birth_month + birth_day + target_date_obj.year)
        personal_day_meaning = f"Energy of {personal_day}. Themes: [to be defined for {personal_day}]"
        return {
            "personal_day": f"{personal_day} ({personal_day_meaning})",
            "personal_month": str(personal_month), "personal_year": str(personal_year),
        }
    except Exception as e: return {"personal_day": "Error calculating daily insights", "error_message": str(e)}


# --- Section 4: Interpretation Dictionaries ---
# (This section remains the same: life_path_meanings, get_life_path_meaning,
#  placeholders for EXPRESSION_INTERPRETATIONS, SOUL_URGE_INTERPRETATIONS, etc.)
# For brevity, not re-pasting. Ensure it's present.
life_path_meanings = { 1: {"description": "Independent...", "advice": "...", "master": False, "element": "Fire", "traits": [], "strengths": [], "weaknesses": []},
    11: {"description": "Intuitive...", "advice": "...", "master": True, "element": "Air", "traits": [], "strengths": [], "weaknesses": []},} # Populate fully
DEFAULT_LP_MEANING = { "description": "Life Path meaning not found.", "advice": "N/A", "master": False, "element": "N/A", "traits": [], "strengths": [], "weaknesses": []}
def get_life_path_meaning(number: int) -> dict: return life_path_meanings.get(number, DEFAULT_LP_MEANING)
EXPRESSION_INTERPRETATIONS = {1: "Expression 1 meaning..."} # Populate fully
SOUL_URGE_INTERPRETATIONS = {1: "Soul Urge 1 meaning..."} # Populate fully
PERSONALITY_INTERPRETATIONS = {1: "Personality 1 meaning..."} # Populate fully
BIRTHDAY_INTERPRETATIONS = {1: "Birthday 1 meaning..."} # Populate fully
BALANCE_NUMBER_INTERPRETATIONS = {1: "Balance Number 1 meaning..."} # Populate fully
MATURITY_NUMBER_INTERPRETATIONS = {1: "Maturity Number 1 meaning..."} # Populate fully
CHALLENGE_NUMBER_INTERPRETATIONS = {0: "Challenge 0 meaning..."} # Populate fully
PINNACLE_NUMBER_INTERPRETATIONS = {1: "Pinnacle 1 meaning..."} # Populate fully
HIDDEN_PASSION_INTERPRETATIONS = {1: "Hidden Passion for 1..."} # Populate fully
DEFAULT_INTERPRETATION = "Interpretation pending."
DEFAULT_BALANCE_MEANING = {"description": "Balance Number meaning not found.", "advice": "N/A"}
def get_balance_meaning(number: int) -> dict: return BALANCE_NUMBER_INTERPRETATIONS.get(number, DEFAULT_BALANCE_MEANING)


# --- Section 5: Main Report Generation Function ---
# (This function generate_full_numerology_report remains largely the same in structure,
#  it will just use the new way of getting compatibility below if it were to call it,
#  but its primary role is the blueprint, not compatibility between two people)
# For brevity, not re-pasting the full generate_full_numerology_report. Ensure it's present.
def generate_full_numerology_report(name: str, birth_date_str: str) -> str:
    # ... (previous implementation that calculates all numbers and formats them) ...
    # This function calculates and formats the single person blueprint.
    # It does NOT use the life_path_compatibility dictionary directly.
    # It uses life_path_meanings for the individual's LP.
    # (Ensure this function is complete as per previous versions)
    # Example snippet of how it uses get_life_path_meaning:
    lp_num = calculate_life_path(birth_date_str)
    if not isinstance(lp_num, int): return f"Could not calculate Life Path: {lp_num}"
    lp_details = get_life_path_meaning(lp_num)
    lp_report_section_intro = [
        "--------------------------------------------------",
        "🔑 THE LIFE PATH NUMBER (General Meaning)",
        "--------------------------------------------------",
        "The Life Path number is often considered the most significant number in your numerology chart...",
        "\n"
    ]
    lp_report_section_details = [
        f"🔑 LIFE PATH NUMBER: {lp_num} {'(Master Number)' if lp_details.get('master') else ''}",
        f"   Element: {lp_details.get('element', 'N/A')}",
        "--------------------------------------------------",
        f"Description: {lp_details.get('description', DEFAULT_INTERPRETATION)}",
        # ... more details from lp_details ...
        "\n"
    ]
    # This is just a small part of generate_full_numerology_report
    # The full function as defined before should be here.
    # For this example, let's assume it's defined elsewhere or copy-pasted fully.
    # For now, a placeholder:
    if 'generate_full_numerology_report_defined_elsewhere' not in locals():
        def generate_full_numerology_report(name, birth_date_str):
            # THIS IS A PLACEHOLDER - USE YOUR FULL FUNCTION
            lp_num = calculate_life_path(birth_date_str)
            if not isinstance(lp_num, int): return f"Error in LP calc: {lp_num}"
            lp_details = get_life_path_meaning(lp_num)
            return (f"Report for {name} ({birth_date_str}):\n"
                    f"Life Path: {lp_num} - {lp_details.get('description')}\n"
                    f"... other numbers ...")


       



    # --- Test Full Numerology Blueprint ---
    # Ensure generate_full_numerology_report is fully defined above or imported
    test_name = "Jeffery Allen Louis Weber"
    test_birth_date = "1987-05-08" 
    print(f"\n--- Generating Full Blueprint for {test_name} ({test_birth_date}) ---")
    # You need the full definition of generate_full_numerology_report here from previous steps
    # For now, assuming it's defined and just calling it:
    if 'generate_full_numerology_report_defined_elsewhere' in locals(): # Check if it's the placeholder
         print("NOTE: Using placeholder for generate_full_numerology_report. For full output, ensure it's completely defined.")
    full_report = generate_full_numerology_report(test_name, test_birth_date)
    print(full_report)

def get_data_dir():
    """Returns the absolute path to the local 'data' directory."""
    current_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(current_dir, "..", "data"))

if __name__ == "__main__":
    data_dir = get_data_dir()
    file_path = os.path.join(data_dir, "expression_meanings.json")
    meanings = load_json_file(file_path)
    expression_5 = safe_get(meanings, "5", "Meaning not found.")

    print("Expression 5 meaning:")
    print(expression_5)
