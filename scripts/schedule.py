from apscheduler.schedulers.background import BackgroundScheduler
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import WeatherGenerator
from src.database import WeatherRepository
import time

scheduler = BackgroundScheduler()
generator = WeatherGenerator()
repo = WeatherRepository()

def generate_weather():
    weather = generator.generate_random()
    repo.save(weather)

# Schedule every 30 seconds
scheduler.add_job(generate_weather, 'interval', seconds=30)
scheduler.start()

# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
