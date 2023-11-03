from discord.ext import commands
from traceback import format_exc

class OnMessage(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if self.client.callables["on_message"] is None:
            return
    
        if message.author == self.client.user:
            return

        try:
            response = self.client.callables["on_message"](message)
            await message.channel.send(response)
        except Exception as e:
            error_type = type(e).__name__
            traceback_info = format_exc()
            self.client.logger.error(f"{error_type}: {e}\n{traceback_info}")

# add cog extension to "client" (the bot)
# NOTE: THIS CODE RUNS FROM THE DIRECTORY THAT "main.py" IS IN
async def setup(client):
    await client.add_cog(OnMessage(client))