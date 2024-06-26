from flask import Flask
from config import LocalDevelopmentConfig
from model.db import db

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)