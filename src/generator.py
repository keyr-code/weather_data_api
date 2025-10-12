"""
Weather Generator - Creating random weather data.
"""

from random import uniform, choice
from datetime import datetime
from .data_model import WeatherData


class WeatherGenerator:
    """
    Generates realistic weather data.
    """

    CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Foggy"]
    
    LOCATIONS = [
        "New York", "London", "Tokyo", "Sydney", "Paris", "Berlin",
        "Toronto", "Mumbai", "Cairo", "Moscow", "Rio de Janeiro", "Bangkok"
    ]

    # Temperature ranges by condition (Celsius)
    TEMP_RANGES = {
        "Sunny": (15, 35),
        "Cloudy": (10, 25),
        "Rainy": (5, 20),
        "Stormy": (0, 15),
        "Snowy": (-15, 5),
        "Foggy": (5, 15)
    }

    @staticmethod
    def generate(location: str) -> WeatherData:
        """Generate a single weather reading.

        Args:
            location: City or region name

        Returns:
            WeatherData object with generated values
        """
        # Pick random condition first
        condition = choice(WeatherGenerator.CONDITIONS)

        # Get temperature range for this condition
        temp_min, temp_max = WeatherGenerator.TEMP_RANGES[condition]
        temperature = uniform(temp_min, temp_max)

        # Generate other weather parameters
        humidity = uniform(20, 100)  # 20-100% humidity
        wind_speed = uniform(0, 50)  # 0-50 km/h wind

        # Create and return WeatherData object
        return WeatherData(
            timestamp=datetime.now(),
            location=location,
            temperature=round(temperature, 1),  # Round to 1 decimal
            humidity=round(humidity, 1),
            condition=condition,
            wind_speed=round(wind_speed, 1)
        )

    @staticmethod
    def generate_random() -> WeatherData:
        """Generate weather data with random location.
        
        Returns:
            WeatherData object with random location and values
        """
        location = choice(WeatherGenerator.LOCATIONS)
        return WeatherGenerator.generate(location)
    
    @staticmethod
    def generate_batch(location: str, count: int) -> list[WeatherData]:
        """Generate multiple weather readings.

        Args:
            location: City or region name
            count: Number of readings to generate

        Returns:
            List of WeatherData objects
        """
        return [WeatherGenerator.generate(location) for _ in range(count)]
    
    @staticmethod
    def generate_random_batch(count: int) -> list[WeatherData]:
        """Generate multiple weather readings with random locations.
        
        Args:
            count: Number of readings to generate
            
        Returns:
            List of WeatherData objects with random locations
        """
        return [WeatherGenerator.generate_random() for _ in range(count)]