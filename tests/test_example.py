"""
Example usage and testing script.

"""

from datetime import datetime
from generator import WeatherGenerator
from database import WeatherRepository
from data_model import WeatherData


def test_models():
    """
    Test WeatherData dataclass.

    """
    print("=" * 50)
    print("Testing WeatherData (dataclass)")
    print("=" * 50)

    # Create weather data manually
    weather = WeatherData(
        timestamp=datetime.now(),
        location="London",
        temperature=15.5,
        humidity=70.0,
        condition="Rainy",
        wind_speed=20.5
    )

    # Print representation
    print(f"Weather object: {weather}")

    # Convert to dict
    print(f"As dict: {weather.to_dict()}")

    # Test equality
    weather2 = WeatherData(
        timestamp=weather.timestamp,
        location="London",
        temperature=15.5,
        humidity=70.0,
        condition="Rainy",
        wind_speed=20.5
    )
    print(f"weather == weather2: {weather == weather2}")
    print()


def test_generator():
    """
    Test WeatherGenerator class.
    """
    print("=" * 50)
    print("Testing WeatherGenerator ")
    print("=" * 50)

    # Generate single weather reading
    weather = WeatherGenerator.generate("Paris")
    print(f"Generated weather: {weather}")

    # Generate batch
    batch = WeatherGenerator.generate_batch("Tokyo", 5)
    print(f"\nGenerated {len(batch)} readings:")
    for w in batch:
        print(f"  - {w.condition}: {w.temperature}°C")
    
    # Generate random weather (no location needed)
    random_weather = WeatherGenerator.generate_random()
    print(f"\nRandom weather: {random_weather}")
    
    # Generate random batch
    random_batch = WeatherGenerator.generate_random_batch(3)
    print(f"\nRandom batch ({len(random_batch)} readings):")
    for w in random_batch:
        print(f"  - {w.location}: {w.condition}, {w.temperature}°C")
    print()


def test_repository():
    """
    Test WeatherRepository class.
    """
    print("=" * 50)
    print("Testing WeatherRepository (data access)")
    print("=" * 50)

    # Create repository with test database
    repo = WeatherRepository("test_weather.db")

    # Generate and save some data
    print("Saving weather data...")
    for _ in range(5):
        weather = WeatherGenerator.generate("Berlin")
        repo.save(weather)

    # Get latest weather
    latest = repo.get_latest("Berlin")
    print(f"Latest weather: {latest}")

    # Get historical data
    historical = repo.get_historical("Berlin", limit=3)
    print(f"\nHistorical data ({len(historical)} records):")
    for w in historical:
        print(f"  - {w.timestamp}: {w.condition}, {w.temperature}°C")

    # Get all locations
    locations = repo.get_all_locations()
    print(f"\nAll locations: {locations}")
    print()


def test_integration():
    """
    Test all components working together.

    """
    print("=" * 50)
    print("Testing Integration (all components)")
    print("=" * 50)

    # Initialize components
    repo = WeatherRepository("integration_test.db")

    # Simulate API flow: generate live weather
    print("Simulating: GET /weather/live/Madrid")
    weather = WeatherGenerator.generate("Madrid")
    repo.save(weather)
    print(f"Response: {weather.to_dict()}")

    # Simulate API flow: get current weather
    print("\nSimulating: GET /weather/current/Madrid")
    current = repo.get_latest("Madrid")
    print(f"Response: {current.to_dict()}")

    # Simulate API flow: seed data
    # This is what happens when user calls POST /weather/seed/<location>/<count>
    print("\nSimulating: POST /weather/seed/Madrid/10")
    batch = WeatherGenerator.generate_batch("Madrid", 10)
    for w in batch:
        repo.save(w)
    print(f"Response: Generated 10 readings")

    # Simulate API flow: get historical
    # This is what happens when user calls /weather/historical/<location>
    print("\nSimulating: GET /weather/historical/Madrid?limit=5")
    historical = repo.get_historical("Madrid", limit=5)
    print(f"Response: {len(historical)} records")
    for w in historical:
        print(f"  - {w.timestamp}: {w.condition}, {w.temperature}°C")
    print()


if __name__ == "__main__":
    """Run all tests.

    
    """
    print("\n" + "=" * 50)
    print("WEATHER API - COMPONENT TESTING")
    print("=" * 50 + "\n")

    # Test each component
    test_models()
    test_generator()
    test_repository()
    test_integration()

    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)