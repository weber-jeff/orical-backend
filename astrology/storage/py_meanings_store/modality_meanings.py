# astrology/astro_data/modality_meanings.py

modality_meanings = {
    "Cardinal": {
        "name": "Cardinal",
        "meaning": (
            "Cardinal signs are the initiators and leaders of the zodiac. They are dynamic, proactive, and "
            "constantly seeking new beginnings and ways to start projects. Their energy sparks action and sets things in motion."
        ),
        "keywords": ["initiative", "leadership", "ambition", "drive", "innovation"],
        "strengths": ["Goal-oriented", "Visionary", "Energetic", "Decisive"],
        "challenges": ["Impatience", "Overbearing", "Restlessness", "Difficulty finishing what they start"],
        "spiritual_lesson": "Learn to balance initiating new endeavors with patience and follow-through.",
        "relationship_effect": "Cardinal individuals lead relationships with confidence but may need to be mindful of not dominating.",
        "career_effect": "Excel in leadership roles, entrepreneurship, management, and any career requiring initiative.",
        "psychological_shadow": "Can become controlling, impulsive, or easily frustrated by delays.",
        "archetype": "The Initiator – the spark that lights the fire.",
        "associated_signs": ["Aries", "Cancer", "Libra", "Capricorn"],
        "elemental_association": {
            "Aries": "Fire", "Cancer": "Water", "Libra": "Air", "Capricorn": "Earth"
        }
    },
    "Fixed": {
        "name": "Fixed",
        "meaning": (
            "Fixed signs are the stabilizers and sustainers of the zodiac. They embody determination, persistence, "
            "and resistance to change, providing consistency and reliability."
        ),
        "keywords": ["stability", "determination", "loyalty", "persistence", "endurance"],
        "strengths": ["Reliable", "Focused", "Patient", "Tenacious"],
        "challenges": ["Stubbornness", "Resistance to change", "Possessiveness", "Inflexibility"],
        "spiritual_lesson": "Learn to be adaptable while holding onto your core values.",
        "relationship_effect": "Fixed individuals provide steady, enduring love but may struggle with rigidity.",
        "career_effect": "Thrive in careers requiring perseverance, routine, craftsmanship, and management.",
        "psychological_shadow": "Can become inflexible, resistant to new ideas, or stuck in unhealthy patterns.",
        "archetype": "The Stabilizer – the rock and foundation.",
        "associated_signs": ["Taurus", "Leo", "Scorpio", "Aquarius"],
        "elemental_association": {
            "Taurus": "Earth", "Leo": "Fire", "Scorpio": "Water", "Aquarius": "Air"
        }
    },
    "Mutable": {
        "name": "Mutable",
        "meaning": (
            "Mutable signs are the adapters and communicators of the zodiac. They are flexible, versatile, and skilled "
            "at navigating change, often acting as the connectors and translators in the zodiac wheel."
        ),
        "keywords": ["adaptability", "flexibility", "communication", "versatility", "curiosity"],
        "strengths": ["Open-minded", "Resourceful", "Multitasker", "Diplomatic"],
        "challenges": ["Indecisiveness", "Inconsistency", "Restlessness", "Superficiality"],
        "spiritual_lesson": "Balance your flexibility with commitment and depth.",
        "relationship_effect": "Mutable individuals bring variety and change to relationships but may struggle with consistency.",
        "career_effect": "Excel in careers requiring adaptability, communication, teaching, and travel.",
        "psychological_shadow": "Can be scattered, unreliable, or emotionally detached.",
        "archetype": "The Adapter – the versatile communicator.",
        "associated_signs": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
        "elemental_association": {
            "Gemini": "Air", "Virgo": "Earth", "Sagittarius": "Fire", "Pisces": "Water"
        }
    }
}


def get_modality_report(modality_name: str) -> str:
    """Generate a detailed report for a modality (quality), including elemental specificity."""
    data = modality_meanings.get(modality_name)
    if not data:
        return f"❌ Error: Modality '{modality_name}' not found."

    report = f"\n{'=' * 60}\n"
    report += f"♻️ MODALITY: {data['name'].upper()}\n"
    report += f"{'=' * 60}\n"
    report += f"📖 Meaning:\n{data['meaning']}\n\n"
    report += f"🔑 Keywords: {', '.join(data['keywords'])}\n"
    report += f"💪 Strengths: {', '.join(data['strengths'])}\n"
    report += f"⚠️ Challenges: {', '.join(data['challenges'])}\n"
    report += f"🧘 Spiritual Lesson:\n{data['spiritual_lesson']}\n"
    report += f"❤️ Relationship Effect:\n{data['relationship_effect']}\n"
    report += f"💼 Career Effect:\n{data['career_effect']}\n"
    report += f"👤 Psychological Shadow:\n{data['psychological_shadow']}\n"
    report += f"🎭 Archetype: {data['archetype']}\n"
    report += f"🌐 Associated Signs and Elements:\n"
    for sign in data["associated_signs"]:
        element = data["elemental_association"].get(sign, "Unknown")
        report += f"   - {sign} ({element})\n"
    report += f"{'=' * 60}\n"
    return report


def get_modality_by_sign(sign_name: str) -> str:
    """Return the modality name for a given zodiac sign."""
    for modality, data in modality_meanings.items():
        if sign_name in data["associated_signs"]:
            return modality
    return "Unknown"


def list_modalities() -> list:
    """Return all modality names."""
    return list(modality_meanings.keys())


# Example Usage:
if __name__ == "__main__":
    print(get_modality_report("Cardinal"))
    print(get_modality_report("Fixed"))
    print(get_modality_report("Mutable"))
    print("♻️ taurus modality:", get_modality_by_sign("Virgo"))
