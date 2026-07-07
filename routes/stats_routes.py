from flask import Blueprint, request, jsonify
from managers.transaction_manager import TransactionManager
from managers.income_manager import IncomeManager
from services.statistics_service import summarize_transactions
from services.forecast_service import forecast_income
from datetime import datetime

bp = Blueprint("stats", __name__, url_prefix="/stats")
tx_mgr = TransactionManager()
inc_mgr = IncomeManager()

def parse_date(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()

@bp.route("/summary", methods=["GET"])
def summary():
    from_s = request.args.get("from")
    to_s = request.args.get("to")
    try:
        date_from = parse_date(from_s)
        date_to = parse_date(to_s)
        rows = tx_mgr.list_transactions(date_from=date_from, date_to=date_to)
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    result = summarize_transactions(rows)
    return jsonify(result)

@bp.route("/income_forecast", methods=["GET"])
def income_forecast():
    try:
        n_months = int(request.args.get("n_months", 3))
        if n_months < 1 or n_months > 24:
            return jsonify({"error": "n_months must be between 1 and 24"}), 400
    except ValueError:
        return jsonify({"error": "n_months must be an integer"}), 400
    
    try:
        incomes = inc_mgr.list_income()
        result = forecast_income(incomes, n_months=n_months)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500