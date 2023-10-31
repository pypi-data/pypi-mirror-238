# -*- coding: utf-8 -*-
import pandas as pd

from functools import cached_property
from requests.adapters import HTTPAdapter, Retry
from typing import Any, Dict, Optional, List, Union, Tuple

from turon.exceptions import APIException, NotFound, Unauthorized
from turon.session import Session


__version__ = "1.0.0"

__all__ = ["Turon", "Query"]


class Turon(object):
    """
    The Turon API client. Formats and submits API calls to Turon.

    :param app_key: The application key from your Turon share.
    :param api_key: The secret key from your Turon share.
    :param base_url: API endpoint url.
    :param retry_attempts: Total number of retries to allow.
    :param retry_backoff_factor: A backoff factor to apply between attempts after the second try.
    """
    def __init__(
        self,
        app_key: str,
        api_key: str,
        base_url: str = 'https://pylon.turon.io',
        retry_attempts: int = 3,
        retry_backoff_factor: int = 0.5,
    ):
        self.app_key = app_key
        self.api_key = api_key
        self.base_url = base_url
        self.retry_attempts = retry_attempts
        self.retry_backoff_factor = retry_backoff_factor

    @cached_property
    def session(self) -> Session:
        headers = {
            'TURON-APP-KEY': self.app_key,
            'TURON-API-KEY': self.api_key,
        }

        max_retries = Retry(
            total=self.retry_attempts,
            backoff_factor=self.retry_backoff_factor,
            status_forcelist=[500, 501, 502, 504])

        session = Session(self.base_url)
        session.headers = headers
        session.mount('https://', HTTPAdapter(max_retries=max_retries))

        return session

    def get(self, endpoint_name: str, **params: Dict[str, Any]) -> 'Query':
        """
        This method builds and returns a Query object that can be executed against the Turon API.

        :param endpoint_name: Endpoint you are querying.
        :param params: Query parameters, such as lookup fields, that
            you want to include in your request. This will throw an error if required
            fields are missing.
        """
        return Query(self, endpoint_name=endpoint_name, params=params)


class Query(object):
    """
    A prepared query to be executed against the Turon API. This object is lazy loaded and
    will defer execution until certain methods (`to_*`) are called.

    :param client: Instance of the Turon client.
    :param endpoint_name: Endpoint you are querying.
    :param params: Query parameters, such as lookup fields, that
        you want to include in your request. This will throw an error if required
        fields are missing.

    """
    def __init__(self, client: Turon, endpoint_name: str, params: Optional[Dict[str, Any]] = None):
        self.client = client
        self.endpoint_name = endpoint_name
        self.params = params

    @property
    def session(self) -> Session:
        return self.client.session

    def do_request(self, params: Optional[Dict[str, Any]]):
        response = self.session.get(self.endpoint_name, params=params)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            raise Unauthorized()

        if response.status_code == 404:
            raise NotFound()

        raise APIException(response.content.decode(), code=response.status_code)

    def get_data(self, limit: str = None):
        response = self.do_request(params=self.params)

        if 'data' not in response:
            return response

        data = response['data']

        while response.get('has_next_page', False):
            if limit and len(data) >= limit:
                break

            params = self.params.copy()
            params.update({'cursor': response['end_cursor']})

            response = self.do_request(params=params)

            data = data + response.get('data', [])

        return data if not limit else data[:limit]

    def to_dict(self, limit: int = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Convert the query results to a dictionary or list of dictionaries.

        :param limit: Maximum number of objects to return. Only applied for
            endpoints configured to return multiple results.
        """
        return self.get_data(limit=limit)

    def to_tuple(self, limit: int = None) -> Union[List[Tuple[Any]], Tuple[Any]]:
        """
        Convert the query results to a tuple or list of tuples.

        :param limit: Maximum number of objects to return. Only applied for
            endpoints configured to return multiple results.
        """
        data = self.get_data(limit=limit)

        if isinstance(data, dict):
            return tuple(data.values())

        return [tuple(d.values()) for d in data]

    def to_pandas(self, limit: int = None) -> pd.DataFrame:
        """
        Convert the query results to pandas DataFrame.

        :param limit: Maximum number of objects to return. Only applied for
            endpoints configured to return multiple results.
        """
        data = self.get_data(limit=limit)

        if isinstance(data, dict):
            return pd.DataFrame([data])

        return pd.DataFrame(data)
