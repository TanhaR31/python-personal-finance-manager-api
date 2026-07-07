from flask import Flask
from storage.db import init_db, get_session, Base, engine
from routes import accounts_routes, transactions_routes, income_routes, stats_routes
import config

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

    init_db()

    app.register_blueprint(accounts_routes.bp)
    app.register_blueprint(transactions_routes.bp)
    app.register_blueprint(income_routes.bp)
    app.register_blueprint(stats_routes.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
