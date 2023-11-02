import logging
import time
from enum import Enum

from playwright.sync_api import sync_playwright

from webql.common.utils import ensure_url_scheme
from webql.web.driver_constants import USER_AGENT
from webql.web.web_driver import WebDriver

log = logging.getLogger(__name__)


class BrowserLoadState(Enum):
    DOMCONTENTLOADED = "domcontentloaded"
    """wait for the `DOMContentLoaded` event to be fired."""
    LOAD = "load"
    """wait for the `load` event to be fired."""
    NETWORKIDLE = "networkidle"
    """**DISCOURAGED** wait until there are no network connections for at least `500` ms."""


class PlaywrightWebDriver(WebDriver):
    def __init__(self, headless=True) -> None:
        self._playwright = None

        self._browser = None
        """The current browser. Only use this to close the browser session in the end."""

        self._context = None
        """The current browser context. Use this to open a new page"""

        self._current_page = None
        """The current page that is being interacted with."""

        self._headless = headless
        """Whether to run browser in headless mode or not."""

    def start_browser(self, user_session_extras: dict = None):
        self._start_browser(headless=self._headless, user_session_extras=user_session_extras)

    def stop_browser(self):
        """Closes the current browser session."""
        if self._browser:
            self._browser.close()
            self._browser = None
        self._playwright.stop()
        self._playwright = None

    def open_url(self, url: str):
        if not self._browser:
            raise ValueError(
                'No open browser if detected. Make sure you call "start_browser()" first.'
            )
        self._open_url(url)

    def get_accessiblity_tree(self) -> dict:
        """Gets the accessibility tree for the current page.

        Returns:
        dict: AT of the page

        """
        if not self._current_page:
            raise ValueError('No page is open. Make sure you call "open_url()" first.')

        self._page_scroll()
        self._modify_dom()

        full_tree = None
        try:
            # Retrieve the accessibility tree
            full_tree = self._current_page.accessibility.snapshot(interesting_only=False)
        except Exception as e:
            log.error(e)
            raise e

        return full_tree

    def click(self, element_id: str):
        try:
            element_to_click = self._current_page.locator(f"#{element_id}")
            element_to_click.click()
        except Exception as e:
            log.error(e)
            raise e

    def input(self, element_id: str, text: str):
        try:
            element_to_input = self._current_page.locator(f"#{element_id}")
            element_to_input.fill(text)
        except Exception as e:
            log.error(e)
            raise e

    def _open_url(self, url: str, load_state: BrowserLoadState = None):
        """Opens a new page and navigates to the given URL. Initialize the storgage state if provided. Waits for the given load state before returning.

        Parameters:

        url (str): The URL to navigate to.
        storgate_state_content (optional): The storage state with which user would like to initialize the browser.

        """

        self._current_page = None
        url = ensure_url_scheme(url)

        try:
            page = self._context.new_page()
            page.goto(url)
            try:
                page.wait_for_load_state(load_state.value if load_state else None)
            except TimeoutError as e:
                log.error("Timeout waiting for page to load")
                raise e
            self._current_page = page
        except Exception as e:
            log.error(e)
            raise e

    def _modify_dom(self):
        """Modifies the dom by assigning a unique ID to every node in the document,
        and setting the `aria-roledescription` attribute to the ID.
        """
        js_code = """
        () => {
            document.querySelectorAll('*').forEach((node, index) => {
                if (!node.id) {
                    node.setAttribute('id', 'tf_' + index);
                }
                
                node.setAttribute('aria-roledescription', node.id);
            
                node.setAttribute('aria-keyshortcuts', node.nodeName.toLowerCase());
            });
        }
        """
        self._current_page.evaluate(js_code)

    def _page_scroll(self, pages=3):
        """Scrolls the page down first and then up.

        Parameters:

        pages (int): The number of pages to scroll down.
        """
        delta_y = 10000
        for _ in range(pages):
            self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
            time.sleep(0.1)

        delta_y = -10000
        time.sleep(1)
        for _ in range(pages):
            self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
            time.sleep(0.1)

    def _start_browser(self, user_session_extras: dict = None, headless=True, load_media=False):
        """Starts a new browser session and set storage state (if there is any).

        Parameters:

        user_session_extras (optional): the JSON object that holds user session information
        headless (bool): Whether to start the browser in headless mode.
        load_media (bool): Whether to load media (images, fonts, etc.) or not.
        """
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=headless)
        self._context = self._browser.new_context(
            user_agent=USER_AGENT, storage_state=user_session_extras
        )
        if not load_media:
            self._context.route(
                "**/*",
                lambda route, request: route.abort()
                if request.resource_type in ["image", "media", "font"]
                else route.continue_(),
            )
