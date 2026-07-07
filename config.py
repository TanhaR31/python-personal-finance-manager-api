import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, "finance.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FILE}"
