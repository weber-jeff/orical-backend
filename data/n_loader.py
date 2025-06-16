import json
from pathlib import Path
from typing import Dict, Any


class UniversalMeaningLoader:
    """
    Loads the single, master numerology meanings file and can retrieve
    a combined meaning for any number in any context.
    """

    def __init__(self):
        # Correctly join the relative path to the JSON file
        path = Path(__file__).parent /"numerology_meanings.json"
        path = path.resolve()  # Normalize the path to absolute
        self._meanings_data = self._load_json(path)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Loads the JSON file with error handling."""
        try:
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Error loading JSON file at {path}: {e}")
            return {}

    def get_meaning(self, number: int, context: str) -> Dict[str, Any]:
        """
        Gets the complete meaning for a number by merging the 'core' meaning
        with the meaning for a specific 'context' (e.g., 'lifePath').
        """
        key = str(number)
        number_data = self._meanings_data.get(key)

        if not number_data:
            return {"error": f"No data found for number {key}."}

        core_data = number_data.get("core", {})
        context_specific_data = number_data.get("contextual", {}).get(context, {})

        # Merge both dictionaries (context overrides core on conflicts)
        return {**core_data, **context_specific_data}


# ✅ Singleton-style shared instance
_loader = UniversalMeaningLoader()

# Optional helper function for consistent use elsewhere
def get_meaning(context: str, number: int | str) -> Dict[str, Any]:
    try:
        return _loader.get_meaning(int(number), context.strip())
    except (ValueError, AttributeError):
        return {"error": "Invalid number or context input"}


# For quick CLI test
if __name__ == "__main__":
    test_number = 1
    test_context = "balance" 
    meaning = get_meaning(test_context, test_number)
    print(json.dumps(meaning, indent=2, ensure_ascii=False))
