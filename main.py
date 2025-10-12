"""
Main entry point for the Weather API application.
"""

from src.api import app

if __name__ == '__main__':
    # Run Flask development server
    # WARNING: Don't use in production (use gunicorn instead)
    # Production: gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
    app.run(debug=True, host='0.0.0.0', port=5000)