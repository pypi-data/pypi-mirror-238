from webql.web import WebDriver

from .response_proxy import WQLResponseProxy


class Session:
    """A session with a TF service.

    Attributes:
        url (str): The URL of the TF service.
        session (requests.Session): The session object.
    """

    def __init__(self, web_driver: WebDriver):
        """Initialize the session.

        Parameters:

        url (str): The URL of the TF service.
        """
        self._web_driver = web_driver

    def query(self, query: str) -> WQLResponseProxy:
        """Query the web page tree for elements that match the WebQL query.

        Parameters:

        query (str): The query string.

        Returns:

        dict: WebQL Response (Elements that match the query)
        """
        print(f"querying {query}")

        _accessibility_tree = self._web_driver.get_accessiblity_tree()
        # TODO: implement actual web request
        response = None
        return response

    def stop(self):
        """Close the session."""
        print("closing session")
        self._web_driver.stop_browser()
