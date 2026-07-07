from flask import Blueprint, request, jsonify
from managers.account_manager import AccountManager
from models.account import Account

bp = Blueprint("accounts", __name__, url_prefix="/accounts")
mgr = AccountManager()

@bp.route("", methods=["POST"])
def create_account():
    data = request.get_json(force=True)
    required = ["id", "name", "currency"]
    for k in required:
        if k not in data:
            return jsonify({"error": f"Missing {k}"}), 400
    acc = Account(id=data["id"], name=data["name"], currency=data["currency"])
    try:
        mgr.create_account(acc)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(acc.to_dict()), 201

@bp.route("", methods=["GET"])
def list_accounts():
    accs = mgr.list_accounts()
    return jsonify([a.to_dict() for a in accs])

@bp.route("/<account_id>", methods=["GET"])
def get_account(account_id):
    acc = mgr.get_account(account_id)
    if not acc:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(acc.to_dict())

@bp.route("/<account_id>", methods=["PUT"])
def update_account(account_id):
    data = request.get_json(force=True)
    
    if not data or (not data.get("name") and not data.get("currency")):
        return jsonify({"error": "No fields to update. Provide 'name' or 'currency'"}), 400
    
    try:
        updated_acc = mgr.update_account(account_id, **data)
        return jsonify(updated_acc.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<account_id>", methods=["DELETE"])
def delete_account(account_id):
    try:
        mgr.delete_account(account_id)
        return jsonify({"message": "Account deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
