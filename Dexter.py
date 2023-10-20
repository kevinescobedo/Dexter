import discord
import secret #File containing bot token
import pokemon_database

class Dexter(discord.Client):
    async def on_ready(self):
        self.pokedex = pokemon_database.PokemonDatabase("pokedex.db")
        self.answer = None
        self.inGame = False
        await client.change_presence(activity=discord.Game(name="Pokémon"))

    async def on_message(self, message):
        """
        Handles message input
        """
        if message.content == "!stop":
            await client.close()

        if message.content == "!pokemon":
            info = self.pokedex.get_random_data()
            entry = info["entry"]
            self.answer = info["name"].lower()
            entry = entry.replace(info["name"], "This Pokemon")
            entry = entry.replace(info["name"].lower(), "This Pokemon")
            entry = entry.replace(info["name"].upper(), "This Pokemon")
            self.inGame = True
            await message.channel.send(f"{entry}")

        if self.inGame and message.content.startswith("!guess"):
            guess = message.content.split("!guess")[1].strip()
            if guess.lower() == self.answer:
                self.inGame = False
                await message.channel.send(f"<@{message.author.id}> Correct!")

            else:
                await message.channel.send(f"<@{message.author.id}> I'm sorry, that's incorrect...")


        if message.content == "!hello":
            await message.channel.send(f"<@{message.author.id}> Hello!")

if __name__ == "__main__":
    client = Dexter(command_prefix='!', intents=discord.Intents().all())
    client.run(secret.TOKEN)
