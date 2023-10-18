import discord
import secret #File containing bot token

class Dexter(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity=discord.Game(name="Pokémon"))

    async def on_message(self, message):
        """
        Handles message input
        """
        if message.content == "!stop":
            await client.close()

        if message.content == "!hello":
            await message.channel.send("Hello!")

if __name__ == "__main__":
    client = Dexter(command_prefix='!', intents=discord.Intents().all())
    client.run(secret.TOKEN)
