"""
This class acts as the front end to the user. I seperated it from the main class to prevent the user
from seeing internal methods that may be confusing
"""

# external imports
from collections.abc import Callable
from discord import Message as message
from inspect import signature
from asyncio import run

# local import
from .api_handler import DiscordAPIHandler

class DiscordBot:
    def __init__(self) -> None:
        self.api_handler = DiscordAPIHandler()
        self.logger = self.api_handler.LOGGER

    def start(self) -> None:
        """
        Starts the bot client and loads dependencies.
        """
        run(self.api_handler.main())
    
    def call_on_message(self, function: Callable[[message], str]) -> None:
        """
        The bot will call the parameter passed into this method whenever it receives a message
        """

        # check if the object passed is a function
        if not callable(function):
            self.api_handler.LOGGER.error(f"Failed to load function '{function}'")
            return

        # check if the function only has 1 parameter
        parameters = signature(function).parameters
        if len(parameters) != 1:
            self.api_handler.LOGGER.error(f"Invalid number of parameters in {function}, please only specify one.")
            return

        self.api_handler.client.callables["on_message"] = function