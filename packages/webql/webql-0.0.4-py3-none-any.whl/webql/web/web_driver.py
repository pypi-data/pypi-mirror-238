from abc import ABC, abstractmethod


class WebDriver(ABC):
    """WebDriver is a interface that defines actually web driver, such as playwright. New web driver should implement this interface."""

    @abstractmethod
    def start_browser(self, user_session_extras: dict = None):
        """Start the browser.

        Parameters:

        user_session_extras (optional): the JSON object that holds user session information
        """

    @abstractmethod
    def stop_browser(self):
        """Stops/closes the browser."""

    @abstractmethod
    def open_url(self, url: str):
        """Open URL in the browser."""

    @abstractmethod
    def get_accessiblity_tree(self) -> dict:
        """Opens url with web driver, assigns ID to every DOM element, and generates AT".

        Parameters:

        url (str): The URL to navigate to.
        user_session_extras (optional): the JSON object that holds user session information

        Returns:

        dict: The AT of the web page.
        """

    @abstractmethod
    def click(self, element_id: str):
        """Clicks on the specified web element.

        Parameters:

        element_id (str): The dom id of the web element to click on.
        """

    @abstractmethod
    def input(self, element_id: str, text: str):
        """Inputs text into the specified web element.

        Parameters:

        elemment_id (str): The dom id of the web element to input text into.
        text (str): The text to input.
        """
