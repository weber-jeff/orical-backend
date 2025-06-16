element_meanings = {
    "Fire": {
        "name": "Fire",
        "meaning": (
            "Fire is the element of energy, inspiration, and transformation. It fuels action, courage, and creativity, "
            "bringing enthusiasm and the spark of life to everything it touches."
        ),
        "keywords": ["passion", "energy", "enthusiasm", "courage", "drive", "creativity"],
        "strengths": [
            "Leadership", "Optimism", "Inspiration", "Boldness", "Initiative"
        ],
        "challenges": [
            "Impatience", "Impulsiveness", "Aggression", "Burnout"
        ],
        "spiritual_lesson": (
            "Learn to channel your fiery passion without burning out or overwhelming others."
        ),
        "relationship_effect": (
            "Fire signs bring warmth and excitement but can sometimes create friction if unchecked."
        ),
        "career_effect": (
            "Ideal for dynamic, creative, or leadership roles that require initiative and courage."
        ),
        "psychological_shadow": (
            "Restlessness, arrogance, and reckless behavior."
        ),
        "archetype": "The Warrior — bold, pioneering, and fiercely independent.",
        "associated_signs": ["Aries", "Leo", "Sagittarius"],
        "color": "Red, Orange",
        "body_part": "Heart, Circulatory System",
        "season": "Summer",
    },
    "Earth": {
        "name": "Earth",
        "meaning": (
            "Earth represents stability, practicality, and groundedness. It focuses on tangible results, structure, and "
            "material well-being."
        ),
        "keywords": ["stability", "practicality", "reliability", "patience", "materialism", "sensuality"],
        "strengths": [
            "Dependability", "Hard work", "Persistence", "Common sense"
        ],
        "challenges": [
            "Stubbornness", "Materialism", "Rigidity", "Resistance to change"
        ],
        "spiritual_lesson": (
            "Balance material concerns with openness to growth and change."
        ),
        "relationship_effect": (
            "Earth signs build lasting, loyal relationships grounded in trust."
        ),
        "career_effect": (
            "Excellent in careers involving finance, construction, agriculture, or anything requiring detail and persistence."
        ),
        "psychological_shadow": (
            "Fear of change, rigidity, and over-cautiousness."
        ),
        "archetype": "The Builder — steady, reliable, and grounded.",
        "associated_signs": ["Taurus", "Virgo", "Capricorn"],
        "color": "Brown, Green",
        "body_part": "Bones, Muscles, Stomach",
        "season": "Autumn",
    },
    "Air": {
        "name": "Air",
        "meaning": (
            "Air symbolizes intellect, communication, and social connection. It governs thoughts, ideas, and the exchange "
            "of information."
        ),
        "keywords": ["intellect", "communication", "social", "curiosity", "objectivity", "adaptability"],
        "strengths": [
            "Analytical thinking", "Open-mindedness", "Sociability", "Creativity"
        ],
        "challenges": [
            "Indecisiveness", "Detachment", "Superficiality", "Restlessness"
        ],
        "spiritual_lesson": (
            "Develop clarity of thought and balance your need for mental stimulation with emotional depth."
        ),
        "relationship_effect": (
            "Air signs foster intellectual bonds and lively conversation."
        ),
        "career_effect": (
            "Ideal for careers in writing, teaching, technology, and any field that values ideas and communication."
        ),
        "psychological_shadow": (
            "Overthinking, emotional detachment, and inconsistency."
        ),
        "archetype": "The Thinker — curious, communicative, and inventive.",
        "associated_signs": ["Gemini", "Libra", "Aquarius"],
        "color": "Yellow, Light Blue",
        "body_part": "Lungs, Nervous System",
        "season": "Spring",
    },
    "Water": {
        "name": "Water",
        "meaning": (
            "Water governs emotions, intuition, and the unconscious. It flows through feelings, empathy, and spiritual "
            "depth."
        ),
        "keywords": ["emotion", "intuition", "sensitivity", "empathy", "nurturing", "imagination"],
        "strengths": [
            "Emotional intelligence", "Compassion", "Creativity", "Healing"
        ],
        "challenges": [
            "Moodiness", "Over-sensitivity", "Escapism", "Dependency"
        ],
        "spiritual_lesson": (
            "Learn to flow with emotions without being overwhelmed or lost in them."
        ),
        "relationship_effect": (
            "Water signs create deeply emotional and nurturing bonds."
        ),
        "career_effect": (
            "Strong in counseling, healing arts, creative fields, and any role requiring emotional insight."
        ),
        "psychological_shadow": (
            "Emotional vulnerability, withdrawal, and clinginess."
        ),
        "archetype": "The Healer — empathetic, intuitive, and deeply connected.",
        "associated_signs": ["Cancer", "Scorpio", "Pisces"],
        "color": "Blue, Silver",
        "body_part": "Stomach, Kidneys, Fluids",
        "season": "Winter",
    },
}

def get_element_report(element_name: str) -> str:
    """Generate a detailed report string for the specified element."""
    data = element_meanings.get(element_name)
    if not data:
        return f"Error: Element '{element_name}' not found."

    report = "=" * 60 + "\n"
    report += f"🔥 Element: {data['name']} 🔥\n"
    report += "=" * 60 + "\n"
    report += f"📖 Meaning: {data['meaning']}\n"
    report += f"🔑 Keywords: {', '.join(data['keywords'])}\n"
    report += f"💪 Strengths: {', '.join(data['strengths'])}\n"
    report += f"⚠️ Challenges: {', '.join(data['challenges'])}\n"
    report += f"🧘 Spiritual Lesson: {data['spiritual_lesson']}\n"
    report += f"❤️ Relationship Effect: {data['relationship_effect']}\n"
    report += f"💼 Career Effect: {data['career_effect']}\n"
    report += f"👤 Psychological Shadow: {data['psychological_shadow']}\n"
    report += f"🎭 Archetype: {data['archetype']}\n"
    report += f"🌟 Associated Signs: {', '.join(data['associated_signs'])}\n"
    report += f"🎨 Color: {data['color']}\n"
    report += f"🧍 Body Part: {data['body_part']}\n"
    report += f"🍂 Season: {data['season']}\n"
    report += "=" * 60 + "\n"
    return report
print(get_element_report("Fire"))
print(get_element_report("Earth"))
print(get_element_report("Air"))
print(get_element_report("Water"))
