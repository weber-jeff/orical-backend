from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import logging
import os

# === Import Your Services ===
from backend.services.cosmic_fusion import CosmicFusionService
from backend.services.numerology_service import NumerologyService
# from insights.daily_insight_engine import CosmicInsightGenerator

# === App Initialization ===
app = Flask(__name__)
CORS(app)

# === Logging Configuration ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# === Blueprint Setup ===
fusion_bp = Blueprint("fusion", __name__)

# === Routes ===

# Health check
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


# --- Numerology Profile ---
@app.route("/api/numerology-profile", methods=["POST"])
def get_numerology_profile():
    try:
        data = request.get_json()
        name = data.get("name")
        birthdate = data.get("birthdate")

        if not name or not birthdate:
            return jsonify({"status": "error", "message": "Missing name or birthdate"}), 400

        profile = NumerologyService.generate_numerology_profile(name, birthdate)
        return jsonify({"status": "success", "profile": profile}), 200

    except Exception as e:
        logger.exception("Error generating numerology profile")
        return jsonify({"status": "error", "message": str(e)}), 500


# --- Cosmic Profile Generation ---
@fusion_bp.route("/cosmic-profile", methods=["POST"])
def get_cosmic_profile():
    data = request.get_json()
    required_fields = ["sunSign", "destiny", "soulUrge", "personality", "lifePath", "birthday"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({
            "status": "error",
            "message": f"Missing fields: {', '.join(missing_fields)}"
        }), 400

    try:
        profile = CosmicFusionService.generate_cosmic_profile(
            data["sunSign"],
            data["destiny"],
            data["soulUrge"],
            data["personality"],
            data["lifePath"],
            data["birthday"]
        )
        return jsonify(profile), 200

    except Exception as e:
        logger.exception("Failed to generate cosmic profile")
        return jsonify({"status": "error", "message": str(e)}), 500


# --- Daily Insight from Full Cosmic Profile ---
@fusion_bp.route("/daily-insight", methods=["POST"])
def get_fusion_daily_insight():
    data = request.get_json()
    if "cosmicProfile" not in data or "targetDate" not in data:
        return jsonify({"status": "error", "message": "Missing cosmicProfile or targetDate"}), 400

    try:
        profile = data["cosmicProfile"]
        date = data["targetDate"]
        feedback = data.get("learningInsights", {})

        insight = CosmicFusionService.generate_enhanced_daily_insight(profile, date, feedback)
        return jsonify(insight), 200

    except Exception as e:
        logger.exception("Failed to generate enhanced daily insight")
        return jsonify({"status": "error", "message": str(e)}), 500


# --- [OPTIONAL] Daily Insight (Lite version) ---
@app.route("/api/daily-insight", methods=["POST"])
def get_daily_insight():
    try:
        data = request.get_json()
        name = data.get("name")
        birthdate = data.get("birthdate")
        target_date = data.get("target_date")

        if not name or not birthdate:
            return jsonify({"status": "error", "message": "Missing name or birthdate"}), 400

        logger.info(f"Generating insight for {name} on {target_date or 'today'}")
        # insight = insight_engine.generate_daily_insight(name, birthdate, target_date)
        # return jsonify({"status": "success", "data": insight}), 200
        return jsonify({"status": "error", "message": "Insight engine not yet implemented"}), 501

    except Exception as e:
        logger.exception("Failed to generate daily insight")
        return jsonify({"status": "error", "message": str(e)}), 500


# === Register Blueprint ===
app.register_blueprint(fusion_bp, url_prefix="/api")

# === App Entrypoint ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
