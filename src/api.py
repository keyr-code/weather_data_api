"""
Weather API - REST endpoints for weather data access.

"""

from flask import Flask, jsonify, request
from datetime import datetime
from .generator import WeatherGenerator
from .database import WeatherRepository

# Initialize Flask application

app = Flask(__name__)

# Initialize dependencies

generator = WeatherGenerator()
repository = WeatherRepository()


@app.route('/weather/live/<location>', methods=['GET'])
def get_live_weather(location: str):
    """Generate and return live weather data.

    Flow:
    1. Generate new weather data
    2. Save to database (for historical queries later)
    3. Return to user

    Example: GET /weather/live/London
    """
    try:
        # Generate new weather reading
        weather = generator.generate(location)

        # Save to database for historical record

        repository.save(weather)

        # Return as JSON

        return jsonify({
            'status': 'success',
            'data': weather.to_dict()
        }), 200

    except Exception as e:
        # Handle any errors gracefully
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/weather/current/<location>', methods=['GET'])
def get_current_weather(location: str):
    """
    Get most recent weather data from database.

    Example: GET /weather/current/London
    """
    try:
        # Get latest weather from database

        weather = repository.get_latest(location)

        # Handle case where no data exists

        if weather is None:
            return jsonify({
                'status': 'error',
                'message': f'No weather data found for {location}'
            }), 404

        return jsonify({
            'status': 'success',
            'data': weather.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/weather/historical/<location>', methods=['GET'])
def get_historical_weather(location: str):
    """
    Get historical weather data for a location.

    Query Parameters:
    - start: Start date (ISO format, optional)
    - end: End date (ISO format, optional)
    - limit: Max records to return (default: 100)

    Example: GET /weather/historical/London?start=2024-01-01&limit=50
    """
    try:
        # Parse query parameters

        start_str = request.args.get('start')
        end_str = request.args.get('end')
        limit = request.args.get('limit', 100, type=int)

        # Convert date strings to datetime objects

        start = datetime.fromisoformat(start_str) if start_str else None
        end = datetime.fromisoformat(end_str) if end_str else None

        # Query database for historical data

        weather_list = repository.get_historical(location, start, end, limit)

        # Handle empty results
        # Inform user if no data matches their query
        if not weather_list:
            return jsonify({
                'status': 'success',
                'message': f'No historical data found for {location}',
                'data': []
            }), 200

        # Convert all WeatherData objects to dicts
        return jsonify({
            'status': 'success',
            'count': len(weather_list),
            'data': [w.to_dict() for w in weather_list]
        }), 200

    except ValueError as e:
        # Handle invalid date format

        return jsonify({
            'status': 'error',
            'message': f'Invalid date format: {str(e)}'
        }), 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/weather/locations', methods=['GET'])
def get_locations():
    """
    Get list of all available locations.

    Example: GET /weather/locations
    """
    try:
        # Get all unique locations from database

        locations = repository.get_all_locations()

        return jsonify({
            'status': 'success',
            'count': len(locations),
            'data': locations
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/weather/random', methods=['GET'])
def get_random_weather():
    """Generate random weather data for any location.
    
    Example: GET /weather/random
    """
    try:
        weather = generator.generate_random()
        repository.save(weather)
        
        return jsonify({
            'status': 'success',
            'data': weather.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/weather/seed/<location>/<int:count>', methods=['POST'])
def seed_data(location: str, count: int):
    """Generate and save multiple weather readings.
    Populate database with test/historical data quickly.

    Example: POST /weather/seed/London/100
    """
    try:
        # Validate count

        if count > 1000:
            return jsonify({
                'status': 'error',
                'message': 'Count cannot exceed 1000'
            }), 400

        # Generate batch of weather data

        weather_list = generator.generate_batch(location, count)

        # Save all to database
        # Persist for historical queries
        for weather in weather_list:
            repository.save(weather)

        return jsonify({
            'status': 'success',
            'message': f'Generated {count} weather readings for {location}'
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/weather/seed/random/<int:count>', methods=['POST'])
def seed_random_data(count: int):
    """Generate and save random weather readings for random locations.
    
    Example: POST /weather/seed/random/50
    """
    try:
        if count > 1000:
            return jsonify({
                'status': 'error',
                'message': 'Count cannot exceed 1000'
            }), 400
            
        weather_list = generator.generate_random_batch(count)
        
        for weather in weather_list:
            repository.save(weather)
            
        return jsonify({
            'status': 'success',
            'message': f'Generated {count} random weather readings'
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# Health check endpoint
# Monitoring systems need to verify API is running
@app.route('/health', methods=['GET'])
def health_check():
    """Check if API is running.

    Example: GET /health
    """
    return jsonify({
        'status': 'healthy',
        'service': 'weather-api'
    }), 200


if __name__ == '__main__':
    # Run Flask development server
    # Easy testing during development
    # WARNING: Don't use in production (use gunicorn/uwsgi instead)
    # Run gunicorn -w 4 -b 0.0.0.0:5000 api:app in terminal
    app.run(debug=True, host='0.0.0.0', port=5000)