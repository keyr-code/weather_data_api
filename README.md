# Weather API

A REST API for generating and managing weather data with SQLite storage.

## Features

- Generate live weather data for any location
- Store and retrieve historical weather records
- RESTful endpoints for weather data access
- SQLite database for data persistence
- Batch data generation for testing

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   python main.py
   ```

3. **Test the API:**
   ```bash
   python tests/test_api.py
   ```

## API Endpoints

- `GET /weather/live/{location}` - Generate new weather data
- `GET /weather/current/{location}` - Get latest weather data
- `GET /weather/historical/{location}` - Get historical data
- `GET /weather/locations` - List all locations
- `POST /weather/seed/{location}/{count}` - Generate test data
- `GET /health` - Health check

## Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
```

## Project Structure

```
weather_api/
├── src/           # Source code
├── tests/         # Test files
├── scripts/       # Utility scripts
├── main.py        # Application entry point
└── README.md      # This file
```