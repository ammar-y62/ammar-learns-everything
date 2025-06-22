"""
Foreca Weather API Integration
A comprehensive wrapper for the Foreca Weather API to fetch and process weather data.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ForecaWeatherAPI:
    """
    A comprehensive wrapper for the Foreca Weather API.
    Handles authentication, data fetching, and error handling.
    """

    def __init__(self, username: str, password: str,
                 base_url: str = "https://pfa.foreca.com",
                 map_url: str = "https://map-eu.foreca.com"):
        """
        Initialize the Foreca Weather API client.

        Args:
            username (str): Foreca API username.
            password (str): Foreca API password.
            base_url (str): Base URL for the main weather API.
            map_url (str): Base URL for the weather map API.
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.map_url = map_url
        self.access_token = None
        self.token_expires_at = None
        self.session = requests.Session()

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

        # Cache for location data
        self.location_cache = {}

        logger.info("ForecaWeatherAPI initialized.")

    def _rate_limit(self):
        """Implement rate limiting to respect API limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def _authenticate(self) -> None:
        """Authenticate and retrieve an access token."""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return

        auth_url = f"{self.base_url}/authorize/token"
        auth_data = {
            "user": self.username,
            "password": self.password,
            "expire_hours": 2  # Token valid for 2 hours
        }

        try:
            self._rate_limit()
            response = self.session.post(auth_url, json=auth_data)
            response.raise_for_status()

            auth_response = response.json()
            self.access_token = auth_response["access_token"]
            self.token_expires_at = datetime.now() + timedelta(seconds=auth_response["expires_in"])

            logger.info("Authentication successful. Token is valid for 2 hours.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            raise Exception(f"Failed to authenticate with Foreca API: {e}")

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers with a valid token."""
        self._authenticate()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an authenticated GET request to the Foreca API.

        Args:
            url (str): The full URL for the API endpoint.
            params (dict, optional): URL parameters for the request.

        Returns:
            Dict: The JSON response from the API.
        """
        try:
            headers = self._get_auth_headers()
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for URL {url}: {e}")
            return {}

    def search_location(self, query: str, lang: str = "en", country: Optional[str] = None) -> List[Dict]:
        """
        Search for locations by name or coordinates.

        Args:
            query (str): Search query (e.g., "London", "51.5,-0.12").
            lang (str): Language code (default: "en").
            country (str, optional): Country code to limit search (e.g., "GB").

        Returns:
            List[Dict]: A list of matching locations.
        """
        url = f"{self.base_url}/api/v1/location/search/{query}"
        params = {"lang": lang}
        if country:
            params["country"] = country

        locations_data = self._make_request(url, params)
        locations = locations_data.get("locations", [])
        logger.info(f"Found {len(locations)} locations for query: '{query}'.")
        return locations

    def get_daily_forecast(self, location_id: int, periods: int = 7) -> pd.DataFrame:
        """
        Get the daily weather forecast for a specific location ID.

        Args:
            location_id (int): The ID of the location.
            periods (int): Number of days for the forecast (max 14).

        Returns:
            pd.DataFrame: A DataFrame containing the daily forecast data.
        """
        url = f"{self.base_url}/api/v1/forecast/daily/{location_id}"
        params = {"periods": min(periods, 14)}

        forecast_data = self._make_request(url, params)
        forecasts = forecast_data.get("forecast", [])

        if not forecasts:
            logger.warning(f"No daily forecast data returned for location ID {location_id}.")
            return pd.DataFrame()

        df = pd.DataFrame(forecasts)
        df["date"] = pd.to_datetime(df["date"])
        logger.info(f"Retrieved daily forecast for location ID {location_id}.")
        return df

    def get_hourly_forecast(self, location_id: int, periods: int = 24, tz: str = "UTC") -> pd.DataFrame:
        """
        Get the hourly weather forecast for a location.

        Args:
            location_id (int): The ID of the location.
            periods (int): Number of time periods (max 168).
            tz (str): Timezone for the response (e.g., "UTC", "Europe/London").

        Returns:
            pd.DataFrame: A DataFrame containing the hourly forecast data.
        """
        url = f"{self.base_url}/api/v1/forecast/hourly/{location_id}"
        params = {
            "periods": min(periods, 168),
            "tz": tz
        }

        forecast_data = self._make_request(url, params)
        forecasts = forecast_data.get("forecast", [])

        if not forecasts:
            logger.warning(f"No hourly forecast data returned for location ID {location_id}.")
            return pd.DataFrame()

        df = pd.DataFrame(forecasts)
        df["time"] = pd.to_datetime(df["time"])
        logger.info(f"Retrieved hourly forecast for location ID {location_id}.")
        return df

    def get_location_by_coordinates(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get location information by coordinates.

        Args:
            lat (float): Latitude
            lon (float): Longitude

        Returns:
            Dict: Location information or None if not found
        """
        query = f"{lat},{lon}"
        locations = self.search_location(query)
        return locations[0] if locations else None

    def get_air_quality(self, location: Union[str, Tuple[float, float]]) -> pd.DataFrame:
        """
        Get air quality data for a location.

        Args:
            location: Location identifier or (lat, lon) tuple

        Returns:
            pd.DataFrame: Air quality data
        """
        try:
            self._rate_limit()

            if isinstance(location, tuple):
                location_str = f"{location[0]},{location[1]}"
            else:
                location_str = str(location)

            url = f"{self.base_url}/api/v1/airquality/{location_str}"
            headers = self._get_auth_headers()
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            df = pd.DataFrame(data["airquality"])

            # Convert time column to datetime
            df["time"] = pd.to_datetime(df["time"])

            logger.info(f"Retrieved air quality data for {location_str}")
            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"Air quality data failed: {e}")
            return pd.DataFrame()

    def get_weather_maps(self, layer: str, lat: float, lon: float,
                        zoom: int = 8, width: int = 800, height: int = 600) -> bytes:
        """
        Get weather map images.

        Args:
            layer (str): Map layer type
            lat (float): Latitude
            lon (float): Longitude
            zoom (int): Zoom level
            width (int): Image width
            height (int): Image height

        Returns:
            bytes: Image data
        """
        try:
            self._rate_limit()

            url = f"{self.map_url}/api/v1/map/{layer}/{lat}/{lon}/{zoom}/{width}/{height}"
            headers = self._get_auth_headers()
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            logger.info(f"Retrieved weather map for layer: {layer}")
            return response.content

        except requests.exceptions.RequestException as e:
            logger.error(f"Weather map failed: {e}")
            return b""

    def get_weather_history(self, location: Union[str, Tuple[float, float]],
                          start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical weather data.

        Args:
            location: Location identifier or (lat, lon) tuple
            start_date (str): Start date (YYYY-MM-DD)
            end_date (str): End date (YYYY-MM-DD)

        Returns:
            pd.DataFrame: Historical weather data
        """
        try:
            self._rate_limit()

            if isinstance(location, tuple):
                location_str = f"{location[0]},{location[1]}"
            else:
                location_str = str(location)

            url = f"{self.base_url}/api/v1/observation/history/{location_str}"
            params = {
                "start": start_date,
                "end": end_date
            }

            headers = self._get_auth_headers()
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            df = pd.DataFrame(data["observations"])

            # Convert time column to datetime
            df["time"] = pd.to_datetime(df["time"])

            logger.info(f"Retrieved weather history for {location_str}")
            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"Weather history failed: {e}")
            return pd.DataFrame()

    def get_usage_stats(self, month: str = None, day: str = None) -> Dict:
        """
        Get API usage statistics.

        Args:
            month (str): Month in YYYY-MM format
            day (str): Day in YYYY-MM-DD format

        Returns:
            Dict: Usage statistics
        """
        try:
            self._rate_limit()

            if day:
                url = f"{self.base_url}/usage/day/{day}"
            elif month:
                url = f"{self.base_url}/usage/month/{month}"
            else:
                raise ValueError("Either month or day must be specified")

            auth_data = {
                "user": self.username,
                "password": self.password
            }

            response = self.session.post(url, json=auth_data)
            response.raise_for_status()

            usage_data = response.json()
            logger.info(f"Retrieved usage stats: {usage_data['hits']} total hits")
            return usage_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Usage stats failed: {e}")
            return {}

    def save_forecast_to_csv(self, location: Union[str, Tuple[float, float]],
                           filename: str, forecast_type: str = "hourly") -> bool:
        """
        Save forecast data to CSV file.

        Args:
            location: Location identifier or (lat, lon) tuple
            filename (str): Output filename
            forecast_type (str): "hourly" or "daily"

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if forecast_type == "hourly":
                df = self.get_hourly_forecast(location)
            elif forecast_type == "daily":
                df = self.get_daily_forecast(location)
            else:
                raise ValueError("forecast_type must be 'hourly' or 'daily'")

            if not df.empty:
                df.to_csv(filename, index=False)
                logger.info(f"Saved {forecast_type} forecast to {filename}")
                return True
            else:
                logger.warning(f"No data to save for {forecast_type} forecast")
                return False

        except Exception as e:
            logger.error(f"Failed to save forecast: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Example usage (replace with your actual credentials)
    # api = ForecaWeatherAPI("your_username", "your_password")

    # # Search for a location
    # locations = api.search_location("London")
    # print(f"Found {len(locations)} locations")

    # # Get forecast for London
    # if locations:
    #     london_id = locations[0]["id"]
    #     hourly_forecast = api.get_hourly_forecast(london_id)
    #     print(hourly_forecast.head())

    print("ForecaWeatherAPI module loaded successfully!")
    print("To use this module, create an instance with your API credentials:")
    print("api = ForecaWeatherAPI('your_username', 'your_password')")