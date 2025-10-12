"""
Weather data storing in databases
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from .data_model import WeatherData


class WeatherRepository:
    """
    Handles all database operations for weather data.
    """

    def __init__(self, db_path: str = "weather.db"):
        """
        Initialize repository with database connection.

        Args:
            db_path: Path to SQLite database file
        """
        # Store database path as instance variable
        self.db_path = db_path

        # Initialize database schema
        # Ensure table exists before any operations
        self._init_db()

    def _init_db(self) -> None:
        """
        Create weather table if it doesn't exist.

        """

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    timestamp TEXT NOT NULL,
                    location TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    condition TEXT NOT NULL,
                    wind_speed REAL NOT NULL
                )
            """)
            # Create index for faster queries by location
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_location 
                ON weather(location)
            """)
            conn.commit()

    def save(self, weather: WeatherData) -> None:
        """
        Save weather data to database.

        Args:
            weather: WeatherData object to save
        """
        with sqlite3.connect(self.db_path) as conn:
            # Use parameterized query to prevent SQL injection
            conn.execute("""
                INSERT INTO weather 
                (timestamp, location, temperature, humidity, condition, wind_speed)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                weather.timestamp.isoformat(),  # Convert datetime to string
                weather.location,
                weather.temperature,
                weather.humidity,
                weather.condition,
                weather.wind_speed
            ))
            conn.commit()

    def get_latest(self, location: str) -> Optional[WeatherData]:
        """
        Get most recent weather reading for a location.

        Args:
            location: City or region name

        Returns:
            Most recent WeatherData or None if no data exists
        """
        with sqlite3.connect(self.db_path) as conn:
            # Set row factory to return dict instead of tuple
            conn.row_factory = sqlite3.Row

            cursor = conn.execute("""
                SELECT * FROM weather 
                WHERE location = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (location,))

            row = cursor.fetchone()

            # Return None if no data found
            # Handling of missing data
            if row is None:
                return None

            # Convert database row to WeatherData object

            return WeatherData.from_dict(dict(row))

    def get_historical(
            self,
            location: str,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            limit: int = 100
    ) -> List[WeatherData]:
        """
        Get historical weather readings for a location.

        Args:
            location: City or region name
            start: Start datetime (optional)
            end: End datetime (optional)
            limit: Maximum number of records to return

        Returns:
            List of WeatherData objects, newest first
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Build query dynamically based on parameters

            query = "SELECT * FROM weather WHERE location = ?"
            params = [location]

            # Add date filters if provided

            if start:
                query += " AND timestamp >= ?"
                params.append(start.isoformat())

            if end:
                query += " AND timestamp <= ?"
                params.append(end.isoformat())

            # Order by newest first and limit results

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            # Convert all rows to WeatherData objects

            return [WeatherData.from_dict(dict(row)) for row in rows]

    def get_all_locations(self) -> List[str]:
        """
        Get list of all locations with weather data.

        Returns:
            List of unique location names
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT DISTINCT location FROM weather
                ORDER BY location
            """)
            # Extract first column from each row

            return [row[0] for row in cursor.fetchall()]
