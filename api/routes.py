from flask import Blueprint, request, jsonify
from astronumy.numerology.numer_orchestrator import AstroNumOrchestrator

bp = Blueprint('api', __name__)

@bp.route('/api/report', methods=['POST'])
def generate_report():
    data = request.json
    orchestrator = AstroNumOrchestrator(
        name=data['name'],
        birthdate=data['birthdate'],
        time=data.get('time'),
        location=data.get('location')
    )
    return jsonify(orchestrator.generate_full_report())
