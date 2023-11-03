import logging

import requests

from webql.web import WebDriver

from ..common.api_constants import GET_WEBQL_ENDPOINT, SERVICE_URL
from .response_proxy import WQLResponseProxy

log = logging.getLogger(__name__)


class Session:
    """A session with a TF service.

    Attributes:
        url (str): The URL of the TF service.
        session (requests.Session): The session object.
    """

    def __init__(self, web_driver: WebDriver):
        """Initialize the session.

        Parameters:

        web_driver (WebDriver): The web driver that will be used in this session.
        """
        self._web_driver = web_driver

    def query(self, query: str, timeout: int = 30) -> WQLResponseProxy:
        """Query the web page tree for elements that match the WebQL query.

        Parameters:

        query (str): The query string.
        timeout (optional): Optional timeout value for the connection with backend api service.

        Returns:

        dict: WebQL Response (Elements that match the query)
        """
        log.debug(f"querying {query}")

        try:
            accessibility_tree = self._web_driver.get_accessiblity_tree()
        except Exception as e:
            log.error(e)
            raise e
        try:
            response = self._query(query, accessibility_tree, timeout)
        except Exception as e:
            log.error(e)
            raise e
        wql_response_proxy = WQLResponseProxy(response, self._web_driver)
        return wql_response_proxy

    def stop(self):
        """Close the session."""
        log.debug("closing session")
        self._web_driver.stop_browser()

    def _query(self, query: str, accessibility_tree: dict, timeout: int) -> dict:
        """Make Request to WebQL API.

        Parameters:

        query (str): The query string.
        accessibility_tree (dict): The accessibility tree.
        timeout (int): The timeout value for the connection with backend api service

        Returns:

        dict: WebQL response in json format.
        """
        request_data = {"query": f"{query}", "accessibility_tree": accessibility_tree}
        url = SERVICE_URL + GET_WEBQL_ENDPOINT

        try:
            response = requests.post(url, json=request_data, timeout=timeout)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                log.error(e)
                raise e
            return response.json()
        except Exception as e:
            log.error(e)
            raise e
