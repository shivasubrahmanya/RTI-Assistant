# src/controllers/letter_controller.py

# ... existing imports ...
from flask import Blueprint, request, jsonify
from src.services.letter_service import generate_letter_body

letter_bp = Blueprint("letter", __name__)

# ... existing code ...
@letter_bp.route("/letters", methods=["POST"])
def create_letter():
    try:
        input_data = request.get_json(force=True) or {}
        body = generate_letter_body(input_data)
        return jsonify({"body": body}), 200
    except Exception as e:
        # ... existing error handling ...
        return jsonify({"error": str(e)}), 500
# ... existing code ...