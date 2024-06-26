import os

dir = os.path.abspath(os.path.dirname(__file__))

class LocalDevelopmentConfig:
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(dir, "model")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.db")
