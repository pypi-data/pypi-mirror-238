import json

from webql.common.aria_constants import CLICKABLE_ROLES, INPUT_ROLES
from webql.web import WebDriver


class WADLNode:
    def __init__(self, data: dict, web_driver: WebDriver):
        self._data = data
        self._web_driver = web_driver

    def __getattr__(self, name):
        if name not in self._data:
            raise AttributeError(f"{name} not found in WADL")

        if self._is_clickable(self._data[name]):
            return ClickableNode(self._data[name], self._web_driver)
        if self._is_text_input(self._data[name]):
            return TextInputNode(self._data[name], self._web_driver)
        if isinstance(self._data[name], dict):
            return WADLNode(self._data[name], self._web_driver)

        return self._data[name]

    def __str__(self):
        return json.dumps(self._data, indent=2)

    def _is_clickable(self, node: dict) -> bool:
        return node.get("role") in CLICKABLE_ROLES

    def _is_text_input(self, node: dict) -> bool:
        return node.get("role") in INPUT_ROLES


class ClickableNode:
    def __init__(self, node: dict, web_driver: WebDriver):
        self._node = node
        self._web_driver = web_driver

    def click(self):
        """Perform a click on the element"""
        self._web_driver.click(self._node["id"])

    def __str__(self):
        return json.dumps(self._node, indent=2)


class TextInputNode:
    def __init__(self, node: dict, web_driver: WebDriver):
        self._node = node
        self._web_driver = web_driver

    def input(self, text: str):
        """Input text into the element"""
        self._web_driver.input(self._node["id"], text)

    def __str__(self):
        return json.dumps(self._node, indent=2)
