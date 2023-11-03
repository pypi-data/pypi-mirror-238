# external imports
from discord import Intents
from discord.ext import commands
from inspect import currentframe
from json import load
from sys import exit
import os

# local imports
from phonkd_bot.logger import logger

class DiscordAPIHandler():
    def __init__(self) -> None:
        # aliases
        self.LOGGER = logger()
        self.CALLER_FILE = self.get_caller_file()
        self.CALLER_DIRECTORY = self.get_caller_directory(self.CALLER_FILE)

        # attributes
        self.config = self.load_config_file(self.CALLER_DIRECTORY)
        self.client = self.load_client()

    """ Initializer methods """
    def get_caller_file(self) -> str:
        fname = currentframe()
        while fname.f_back:
            fname = fname.f_back
        caller_file = fname.f_globals['__file__']
        return caller_file

    def get_caller_directory(self, caller_file: str):
        caller_directory = os.path.dirname(os.path.abspath(caller_file))
        return caller_directory

    def load_config_file(self, directory: str) -> dict:
        config_path = directory + "/config.json"
        if not os.path.isfile(config_path):
            self.LOGGER.error(f"Failed to locate config.json, please create the file and try again")
            exit()
        else:
            try:
                with open(config_path) as file:
                    config_data = load(file)
            except Exception as e:
                self.LOGGER.error(f"{type(e).__name__}: {e}")
                exit()
        
        if "token" not in config_data:
            self.LOGGER.error(f"config file missing 'token' value")
            exit()

        return config_data

    def load_client(self) -> commands.Bot:
        prefix = "/" if "prefix" not in self.config else self.config["prefix"]
        client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=Intents.all())
        client.logger = self.LOGGER
        client.callables = {}
        return client

    async def load(self) -> None:
        # get the path of hte current file
        path = os.path.realpath(f"{os.path.dirname(__file__)}/cogs")

        # loop through every python file in the cogs directory
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                extension = filename[:-3]
                try:
                    # load the cog and log the information
                    await self.client.load_extension(f"phonkd_bot.cogs.{extension}")
                    self.LOGGER.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    # print the exception if there is one
                    exception = f"{type(e).__name__}: {e}"
                    self.LOGGER.warning(f"Failed to load extension {extension}\n{exception}")

    async def main(self) -> None:
        async with self.client:
            await self.load()

            try:
                await self.client.start(self.config["token"])
            except Exception as e:
                self.LOGGER.error(f"{type(e).__name__}: {e}")
                exit()