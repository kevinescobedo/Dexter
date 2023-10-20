import discord
import secret #File containing bot token
import pokemon_database

class Dexter(discord.Client):
    async def on_ready(self):
        self.pokedex = pokemon_database.PokemonDatabase("pokedex.db")
        self.answer = None
        self.hints = None
        self.hints_count = 0
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
            entry = entry.replace(info["name"], "<BLANK>")
            entry = entry.replace(info["name"].lower(), "<BLANK>")
            entry = entry.replace(info["name"].upper(), "<BLANK>")
            entry = entry.replace("POKéMON", "Pokémon")
            self.inGame = True
            self.hints_count = 0
            type1 = info["type-1"]
            type2 = info["type-2"]

            if type2:
                pokemonType = f"{type1} and {type2} type"

            else:
                pokemonType = f"{type1} type"
            self.hints = [info["genus"], pokemonType, info["sprite-url"]]
            await message.channel.send(f"{entry}")

        if self.inGame and message.content.startswith("!guess"):
            guess = message.content.split("!guess")[1].strip()
            if guess.lower() == self.answer:
                self.inGame = False
                await message.channel.send(f"<@{message.author.id}> Correct!")

            else:
                await message.channel.send(f"<@{message.author.id}> I'm sorry, that's incorrect...")

        if self.inGame and message.content == "!hint":
            if self.hints_count >= 3:
                self.inGame = False
                await message.channel.send(f"<@{message.author.id}> The answer was {self.answer.title()}")

            else:
                hint = self.hints[self.hints_count]
                if self.hints_count == 0:
                    hint = f"This species is known as the {hint}"
                    await message.channel.send(f"<@{message.author.id}> {hint}")

                if self.hints_count == 1:
                    hint = f"This Pokémon's type is {hint}"
                    await message.channel.send(f"<@{message.author.id}> {hint}")

                if self.hints_count == 2:
                    await message.channel.send(f"<@{message.author.id}> This is what the Pokémon looks like:")
                    await message.channel.send(f"{hint}")

                self.hints_count += 1


        if message.content == "!hello":
            await message.channel.send(f"<@{message.author.id}> Hello!")

if __name__ == "__main__":
    client = Dexter(command_prefix='!', intents=discord.Intents().all())
    client.run(secret.TOKEN)
