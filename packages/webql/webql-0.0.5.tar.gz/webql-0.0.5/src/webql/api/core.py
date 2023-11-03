"""
This module is an entrypoint to WebQL service
"""
import logging

from webql.web import PlaywrightWebDriver, WebDriver

from .session import Session

log = logging.getLogger(__name__)


def start_session(url: str, web_driver: WebDriver = PlaywrightWebDriver()) -> Session:
    """Start a new TF session.

    Parameters:

    url (str): The URL to start the session with.

    Returns:

    TFSession: The new session.
    """
    log.debug(f"Starting session with {url}")

    web_driver.start_browser()
    web_driver.open_url(url)
    session = Session(web_driver)
    return session
