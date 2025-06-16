from backend.services.numerology_core.expression import ExpressionCalculator
from backend.services.numerology_core.life_path import LifePathCalculator
from backend.services.numerology_core.balance import BalanceCalculator
from backend.services.numerology_core.pinnacle_combo import CompoundCalculator
from backend.services.numerology_core.birthday import BirthdayCalculator
from backend.services.numerology_core.personal import PersonalCalculator
from backend.services.numerology_core.challenge import ChallengeCalculator
from backend.services.numerology_core.soul_urge import SoulUrgeCalculator
from backend.services.numerology_core.karmic import KarmicLessonCalculator
from backend.services.numerology_core.hidden_passion import HiddenPassionCalculator
from backend.services.numerology_core.personality import PersonalityCalculator
from backend.services.numerology_core.maturity import MaturityCalculator
from backend.services.numerology_core.utils_num import parse_birthdate

from datetime import datetime
from pprint import pprint


class NumerologyService:
    """
    Service class for generating comprehensive numerology profiles.
    """

    @staticmethod
    def generate_numerology_profile(full_name: str, birthdate: str) -> dict:
        """
        Generate a detailed numerology profile given full name and birthdate (YYYY-MM-DD).
        Returns a dictionary with all core, karmic, and time-based numerology calculations.
        Gracefully handles errors in individual calculations, continuing profile generation.
        """
        try:
            parsed_date = parse_birthdate(birthdate)
        except Exception as e:
            raise ValueError(f"Invalid birthdate format or parsing error: {birthdate}") from e

        birth_year = parsed_date.year
        birth_month = parsed_date.month
        birth_day = parsed_date.day
        target_date = datetime.today()

        personal_calculator = PersonalCalculator()  # instantiate once

        profile = {}

        # Core Numbers
        try:
            profile["lifePath"] = LifePathCalculator.calculate(birthdate)
        except Exception as e:
            profile["lifePath"] = None
            print(f"[WARN] LifePathCalculator failed: {e}")

        try:
            profile["expression"] = ExpressionCalculator.calculate(full_name)
        except Exception as e:
            profile["expression"] = None
            print(f"[WARN] ExpressionCalculator failed: {e}")

        try:
            profile["soulUrge"] = SoulUrgeCalculator.calculate(full_name)
        except Exception as e:
            profile["soulUrge"] = None
            print(f"[WARN] SoulUrgeCalculator failed: {e}")

        try:
            profile["personality"] = PersonalityCalculator.calculate(full_name)
        except Exception as e:
            profile["personality"] = None
            print(f"[WARN] PersonalityCalculator failed: {e}")

        try:
            profile["maturity"] = MaturityCalculator.calculate(full_name, birthdate)
        except Exception as e:
            profile["maturity"] = None
            print(f"[WARN] MaturityCalculator failed: {e}")

        try:
            profile["birthday"] = BirthdayCalculator.calculate(birthdate)
        except Exception as e:
            profile["birthday"] = None
            print(f"[WARN] BirthdayCalculator failed: {e}")

        try:
            profile["balance"] = BalanceCalculator.calculate(birthdate)
        except Exception as e:
            profile["balance"] = None
            print(f"[WARN] BalanceCalculator failed: {e}")

        # Karmic Numbers
        try:
            profile["karmicLessons"] = KarmicLessonCalculator.calculate(full_name)
        except Exception as e:
            profile["karmicLessons"] = None
            print(f"[WARN] KarmicLessonCalculator failed: {e}")

        try:
            profile["hiddenPassion"] = HiddenPassionCalculator.calculate(full_name)
        except Exception as e:
            profile["hiddenPassion"] = None
            print(f"[WARN] HiddenPassionCalculator failed: {e}")

        # Time-Based Numbers
        try:
            profile["personalCycles"] = personal_calculator.calculate_personal_cycle(
                birth_month, birth_day, target_date
            )
        except Exception as e:
            profile["personalCycles"] = None
            print(f"[WARN] PersonalCalculator failed: {e}")

        try:
            profile["challenges"] = ChallengeCalculator.calculate(birthdate)
        except Exception as e:
            profile["challenges"] = None
            print(f"[WARN] ChallengeCalculator failed: {e}")

        # Compound Number (Expression + Life Path)
        try:
            expression_num = profile["expression"]
            life_path_num = profile["lifePath"]

            if isinstance(expression_num, dict):
                expression_num = expression_num.get("number", 0)
            if isinstance(life_path_num, dict):
                life_path_num = life_path_num.get("number", 0)

            profile["pinnacleCombo"] = CompoundCalculator.generate(expression_num, life_path_num)
        except Exception as e:
            profile["pinnacleCombo"] = {"error": str(e)}
            print(f"[WARN] CompoundCalculator failed: {e}")

        return profile


if __name__ == "__main__":
    print("🔮 Generating sample numerology profile...\n")
    profile = NumerologyService.generate_numerology_profile("Jeffrey Allen Louis Weber", "1987-05-08")
    pprint(profile)
