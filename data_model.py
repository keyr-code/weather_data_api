"""
Data models for the weather data
"""
#TODO Add rain, snow, and foggy details

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class WeatherData:
    """Represents a single weather reading.
    """
    timestamp: datetime  # When reading was taken
    location: str  # City or region name
    temperature: float  # Celsius
    humidity: float  # Percentage (0-100)
    condition: str  # Weather condition (Sunny, Rainy, etc.)
    wind_speed: float  # km/h

    def to_dict(self) -> dict:
        """
        Convert to dictionary for JSON serialization.
        """
        data = asdict(self)
        # Convert datetime to ISO string for JSON compatibility
        data['timestamp'] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'WeatherData':
        """
        Create WeatherData from dictionary.
        """
        # Convert ISO string back to datetime object.
        # Database stores as string, we need datetime object
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
