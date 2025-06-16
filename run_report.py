from backend.services.numerology_service import NumerologyService
from data.loader import _loader  # Import the singleton instance directly


class NumerologyReportBuilder:
    @staticmethod
    def generate_report(full_name: str, birthdate: str) -> dict:
        enriched_profile = NumerologyService.generate_numerology_profile(full_name, birthdate)

        report = {}
        for key, value in enriched_profile.items():
            if isinstance(value, dict) and "number" in value:
                report[key] = {
                    "number": value["number"],
                    "meaning": _loader.get_meaning(value["number"], key)
                }
            elif isinstance(value, int):
                report[key] = {
                    "number": value,
                    "meaning": _loader.get_meaning(value, key)
                }
            else:
                report[key] = value

        return report


# Example direct run test
if __name__ == "__main__":
    report = NumerologyReportBuilder.generate_report("Jeffrey Allen Louis Weber", "1987-05-08")
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))
