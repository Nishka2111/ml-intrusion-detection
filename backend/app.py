import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from backend.database.database import db
from backend.routes.health import health_bp
from backend.routes.prediction import prediction_bp
from backend.routes.alerts import alerts_bp
from backend.routes.statistics import statistics_bp
from backend.routes.logs import logs_bp
from backend.routes.traffic import traffic_bp
from backend.routes.analyze import analyze_bp
from backend.routes.performance import performance_bp

load_dotenv()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///intrusion_detection.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Allow Streamlit frontend (default port 8501) to call this API
    CORS(app)

    db.init_app(app)

    # Register API blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(traffic_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(performance_bp)

    with app.app_context():
        from backend.database import models  # noqa: F401
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
