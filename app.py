"""
Multi-User Notes Service Backend
A REST API backend for managing users and their personal notes
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and config
from database import db, init_db
from config import config

# Import routes
from routes.auth_routes import auth_bp
from routes.notes_routes import notes_bp
from routes.share_routes import share_bp
from routes.system_routes import system_bp


def create_app():
    """Application factory function"""

    app = Flask(__name__)

    # Get environment name
    config_name = os.getenv('FLASK_ENV', 'development')

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)

    # Enable CORS
    CORS(app)

    # Create database tables
    with app.app_context():
        init_db()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(share_bp)
    app.register_blueprint(system_bp)

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'message': 'Internal server error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad request'}), 400

    return app


# Create app instance for Gunicorn
app = create_app()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False') == 'True'
    )