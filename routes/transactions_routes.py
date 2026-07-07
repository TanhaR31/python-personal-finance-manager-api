from flask import Blueprint, request, jsonify
from managers.transaction_manager import TransactionManager
from models.transaction import Transaction
from datetime import datetime

bp = Blueprint("transactions", __name__, url_prefix="/transactions")
mgr = TransactionManager()

def parse_date(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()

@bp.route("", methods=["POST"])
def post_transaction():
    data = request.get_json(force=True)
    required = ["id", "account_id", "date", "amount", "type", "category"]
    for k in required:
        if k not in data:
            return jsonify({"error": f"Missing {k}"}), 400
    try:
        d = parse_date(data["date"])
        tx = Transaction(id=data["id"], account_id=data["account_id"], date=d, amount=float(data["amount"]), type=data["type"], category=data["category"], note=data.get("note", ""))
        mgr.create_transaction(tx)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(tx.to_dict()), 201

@bp.route("", methods=["GET"])
def get_transactions():
    from_s = request.args.get("from")
    to_s = request.args.get("to")
    try:
        fr = parse_date(from_s) if from_s else None
        to = parse_date(to_s) if to_s else None
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    rows = mgr.list_transactions(date_from=fr, date_to=to)
    return jsonify([r.to_dict() for r in rows])

@bp.route("/<transaction_id>", methods=["GET"])
def get_single_transaction(transaction_id):
    tx = mgr.get_transaction(transaction_id)
    if not tx:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(tx.to_dict())

@bp.route("/<transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
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
        
        if 'type' in data and data['type'] not in ['income', 'expense']:
            return jsonify({"error": "Type must be 'income' or 'expense'"}), 400
        
        updated_tx = mgr.update_transaction(transaction_id, **data)
        return jsonify(updated_tx.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    try:
        mgr.delete_transaction(transaction_id)
        return jsonify({"message": "Transaction deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
