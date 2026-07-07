from flask import Blueprint, request, jsonify
from managers.income_manager import IncomeManager
from models.income import Income
from datetime import datetime

bp = Blueprint("income", __name__, url_prefix="/income")
mgr = IncomeManager()

def parse_date(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()

@bp.route("", methods=["POST"])
def post_income():
    data = request.get_json(force=True)
    required = ["id", "account_id", "date", "amount", "source"]
    for k in required:
        if k not in data:
            return jsonify({"error": f"Missing {k}"}), 400
    try:
        d = parse_date(data["date"])
        inc = Income(id=data["id"], account_id=data["account_id"], date=d, amount=float(data["amount"]), source=data.get("source", ""))
        mgr.create_income(inc)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(inc.to_dict()), 201

@bp.route("", methods=["GET"])
def get_income():
    from_s = request.args.get("from")
    to_s = request.args.get("to")
    try:
        fr = parse_date(from_s) if from_s else None
        to = parse_date(to_s) if to_s else None
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    rows = mgr.list_income(date_from=fr, date_to=to)
    return jsonify([r.to_dict() for r in rows])

@bp.route("/<income_id>", methods=["GET"])
def get_single_income(income_id):
    inc = mgr.get_income(income_id)
    if not inc:
        return jsonify({"error": "Income not found"}), 404
    return jsonify(inc.to_dict())

@bp.route("/<income_id>", methods=["PUT"])
def update_income(income_id):
    data = request.get_json(force=True)
    
    if not data:
        return jsonify({"error": "No fields to update"}), 400
    
    try:
        if 'date' in data:
            data['date'] = parse_date(data['date'])
        
        if 'amount' in data:
            data['amount'] = float(data['amount'])
            if data['amount'] <= 0:
                return jsonify({"error": "Amount must be positive"}), 400
        
        updated_inc = mgr.update_income(income_id, **data)
        return jsonify(updated_inc.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<income_id>", methods=["DELETE"])
def delete_income(income_id):
    try:
        mgr.delete_income(income_id)
        return jsonify({"message": "Income deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
