import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from datetime import datetime

from loguru import logger


class Sportsbet:
    def __init__(self):
        adapter = HTTPAdapter(max_retries=3)
        self.session = requests.Session()
        self.session.mount("https://www.sportsbet.com.au", adapter=adapter)

    def __enter__(self):
        return self

    def _get_request(self, url: str, params: dict = None, timeout: int = 5):
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(f"HTTP error getting {url}: {http_err}")
        except ConnectionError as con_err:
            logger.error(f"Connection error getting {url}: {con_err}")
        except Exception as err:
            logger.error(f"Error getting {url}: {err}")
        return response.json()

    def get_classes(self) -> list[dict]:
        """Gets the different sports and their classId from sportsbet"""
        return self._get_request(
            url="https://www.sportsbet.com.au/apigw/sportsbook-results/Sportsbook/Results/Classes"
        )

    def get_competitions(
        self,
        class_id: int,
        for_date: datetime = datetime.now(),
    ) -> list[dict]:
        """Gets the active competitions from sportsbet for a given sport and date"""
        return self._get_request(
            url=f"https://www.sportsbet.com.au/apigw/sportsbook-results/Sportsbook/Results/Sports/Classes/{class_id}/Competitions",
            params={"date": for_date.strftime("%Y-%m-%d")},
        )

    def get_results(self, event_id: int) -> dict:
        """Get results of an individual competition or match."""
        return self._get_request(
            url=f"https://www.sportsbet.com.au/apigw/sportsbook-sports/Sportsbook/Sports/Events/{event_id}/Results"
        )

    def get_resulted_events(
        self,
        competition_id: int,
        class_id: int,
        for_date: datetime = datetime.now(),
    ) -> list[dict]:
        """Gets a list of events that have results for a specific sport, competition and date"""
        return self._get_request(
            url=f"https://www.sportsbet.com.au/apigw/sportsbook-sports/Sportsbook/Sports/Competitions/{competition_id}/ResultedEvents?classId={class_id}",
            params={"date": for_date.strftime("%Y-%m-%d")},
        )

    def get_events(
        self,
        from_date: datetime,
        to_date: datetime,
        class_id: int,
        num_events: int = 50,
        primary_markets_only: bool = True,
        include_live_events: bool = False,
    ) -> list[dict]:
        if from_date > to_date:
            logger.error("from_date must be before to_date")
            raise ValueError
        if to_date < datetime.utcnow():
            logger.error("to_date must be in the future")
            raise ValueError
        return self._get_request(
            url="https://www.sportsbet.com.au/apigw/sportsbook-sports/Sportsbook/Sports/Events",
            params={
                "fromDate": from_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "toDate": to_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "sportsId": class_id,
                "numEventsPerClass": num_events,
                "primaryMarketOnly": primary_markets_only,
                "detailsLevel": "O",
            },
        )

    def __exit__(self, *args):
        self.session.close()
