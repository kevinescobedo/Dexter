import discord
import secret #File containing bot token
import game

class Dexter(discord.Client):
    async def on_ready(self):
        self.games = dict()
        await client.change_presence(activity=discord.Game(name="Pokémon"))

    async def on_message(self, message):
        """
        Handles message input
        """
        if message.content == "!stop":
            for discordID in self.games:
                self.games[discordID].pokedex.close()
            await client.close()

        if message.content == "!pokemon":
            self.games[message.author.id] = game.Game(message.author.id)
            entry = self.games[message.author.id].start_game()

            await message.channel.send(f"{entry}")

        try:
            if self.games[message.author.id].in_game() and message.content.startswith("!guess"):
                guess = message.content.split("!guess")[1].strip()
                result = self.games[message.author.id].make_guess(guess)
                await message.channel.send(f"{result}")

        except KeyError:
            pass

        try:
            if self.games[message.author.id].in_game() and message.content == "!hint":
                hint = self.games[message.author.id].give_hint()
                await message.channel.send(f"{hint}")

        except KeyError:
            pass

        if message.content == "!hello":
            await message.channel.send(f"<@{message.author.id}> Hello!")

if __name__ == "__main__":
    client = Dexter(command_prefix='!', intents=discord.Intents().all())
    client.run(secret.TOKEN)
