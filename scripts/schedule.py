from apscheduler.schedulers.background import BackgroundScheduler
import sys
import os

from src.generator import WeatherGenerator
from src.database import WeatherRepository
import time

# Use same database path as API
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(root_dir, "weather.db")

scheduler = BackgroundScheduler()
generator = WeatherGenerator()
repo = WeatherRepository(db_path)

def generate_weather():
    weather = generator.generate_random()
    repo.save(weather)

# Schedule every 30 seconds
scheduler.add_job(generate_weather, 'interval', seconds=10)
scheduler.start()

# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
