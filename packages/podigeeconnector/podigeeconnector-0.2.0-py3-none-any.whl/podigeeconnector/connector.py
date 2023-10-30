"""
PodigeeConnector implements the Podigee Podcast API.
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
from threading import RLock

from bs4 import BeautifulSoup
import requests


class PodigeeConnector:
    """Representation of the Podigee Podcast API."""

    def __init__(self, base_url, podcast_id, podigee_session_v5):
        """
        Initializes the PodigeeConnector object.

        Args:
            base_url (str): Base URL for the API.
            podcast_id (str): Podigee Podcast ID for the API
            podigee_session_v5 (str): Podigee API session token
                                      (from podigee_session_v5 cookie)
        """

        self.base_url = base_url
        self.podcast_id = podcast_id
        self.cookies = {"_podigee_session_v5": podigee_session_v5}
        self._auth_lock = RLock()

    @classmethod
    def from_credentials(cls, base_url, podcast_id, username, password):
        """
        Initializes the PodigeeConnector object from username and password.
        """
        podigee_session_v5 = cls._login(username, password)
        return cls(base_url, podcast_id, podigee_session_v5)

    @staticmethod
    def _login(username, password):
        """
        Logs into Podigee and returns the session token.
        """
        (session_token, csrf_token) = PodigeeConnector.extract_csrf_token()

        headers = {
            "Cookie": f"_podigee_session_v5={session_token}",
        }

        data = {
            "authenticity_token": csrf_token,
            "user[locale]": "en",
            "user[email]": username,
            "user[password]": password,
        }

        response = requests.post(
            "https://app.podigee.com/sessions",
            headers=headers,
            data=data,
            timeout=60,
        )

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Check if the podigee_session_v5 cookie is set
        if "_podigee_session_v5" not in response.cookies:
            raise ValueError("_podigee_session_v5 cookie not found")

        # Return the session token
        return response.cookies["_podigee_session_v5"]

    @staticmethod
    def extract_csrf_token() -> str:
        """
        Extracts the csrf token from a Podigee login page.
        This is required to log in to Podigee.
        """
        url = "https://app.podigee.com/"
        response = requests.get(url, allow_redirects=True, timeout=60)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        token_tag = soup.find("meta", {"name": "csrf-token"})

        if token_tag is None:
            raise ValueError("csrf token not found")
        csrf_token = token_tag["content"]

        session_token = PodigeeConnector.__extract_session_token(response)

        return (session_token, csrf_token)

    @staticmethod
    def __extract_session_token(response: requests.Response) -> str:
        """
        Extract the podigee_session_v5 cookie from the response
        """
        for cookie in response.cookies:
            if cookie.name == "_podigee_session_v5":
                podigee_session_v5 = cookie.value
                break

        if podigee_session_v5 is None:
            raise ValueError("_podigee_session_v5 cookie not found")

        return podigee_session_v5

    def _build_url(self, *args) -> str:
        return f"{self.base_url}/{'/'.join(args)}"

    def _date_params(
        self, start: Optional[datetime], end: Optional[datetime]
    ) -> Dict[str, str]:
        # Set default values for start and end
        if start is None:
            # Default to 30 days ago
            start = datetime.now() - timedelta(days=30)
        if end is None:
            # Default to today
            end = datetime.now()

        return {
            "from": start.strftime("%Y-%m-%d"),
            "to": end.strftime("%Y-%m-%d"),
        }

    def _request(self, url: str, parms: Optional[dict] = None) -> dict:
        response = requests.get(
            url,
            params=parms,
            cookies=self.cookies,
            timeout=60,
        )

        if response.status_code == 200:
            return response.json()
        return response.raise_for_status()

    def podcast_analytics(self, start=None, end=None) -> dict:
        """
        Loads podcast analytics data.
        """
        url = self._build_url(
            "podcasts",
            self.podcast_id,
            "analytics",
        )
        params = self._date_params(start, end)
        return self._request(url, params)

    def episodes(
        self,
    ) -> list:
        """Loads podcast episode data.

        Returns a List of episodes.

        Args:
            -

        Returns:
            list


        Example return value:
        {
            "objects": [
                {
                "id": 1188106,
                "downloads": 0,
                "analytics_episodes_cover_image": "...",
                "title": "New Episode",
                "slug": "1-new-episode",
                "number": 1,
                "published_at": null
                },
                {
                "id": 1188110,
                "downloads": 0,
                "analytics_episodes_cover_image": "...",
                "title": "New Episode",
                "slug": "2-new-episode",
                "number": 2,
                "published_at": "2023-08-13T15:00:14Z"
                }
            ]
        }
        """

        url = self._build_url(
            "podcasts",
            self.podcast_id,
            "analytics",
            "episodes",
        )
        # Set a very high limit to get all episodes
        start = datetime.now() - timedelta(days=1000)
        end = datetime.now()
        params = {"limit": 10000, **self._date_params(start, end)}
        objects = self._request(url, params)

        # This returns a dict with one key: objects.
        # The value is a list of dicts, each dict is an episode.
        return objects["objects"]

    def episode_analytics(
        self, episode_id: str, granularity=None, start=None, end=None
    ) -> dict:
        """
        Loads analytics for a specific episode.

        Args:
            episode_id (str): Episode ID
            granularity (str): Granularity of the data.
                               Possible values are: day, week, month, year
            start (datetime): Start date for the data
            end (datetime): End date for the data

        Returns:
            dict: Episode analytics data

        Example return value:
        {
            "meta": {
                "timerange": {
                    "start_datetime": "string",
                    "end_datetime": "string"
                },
                "aggregation_granularity": "hour"
            },
            "objects": [
                {
                "downloaded_on": "2023-08-13T14:57:30.119Z",
                "downloads": {},
                "formats": {},
                "platforms": {},
                "countries": {},
                "clients": {},
                "clients_on_platforms": {},
                "sources": {}
                }
            ]
        }
        """
        url = self._build_url(
            "episodes",
            str(episode_id),
            "analytics",
        )
        params = self._date_params(start, end)
        if granularity is not None:
            params["granularity"] = granularity

        return self._request(url, params)
