import pokemon_database

class Game:
    def __init__(self, discordID: int):
        self.person = discordID
        self.pokedex = pokemon_database.PokemonDatabase()
        self.answer = None
        self.playing = False
        self.hints_count = 0
        self.hints = []

    def start_game(self) -> str:
        """
        Starts the game by getting a random Pokedex entry and setting the hints
        """
        info = self.pokedex.get_random_data()
        entry = info["entry"]
        self.answer = info["name"].lower()
        entry = entry.replace(info["name"], "<BLANK>")
        entry = entry.replace(info["name"].lower(), "<BLANK>")
        entry = entry.replace(info["name"].upper(), "<BLANK>")
        entry = entry.replace("POKéMON", "Pokémon")

        self.playing = True
        self.hints_count = 0

        type1 = info["type-1"]
        type2 = info["type-2"]

        if type2:
            pokemonType = f"{type1} and {type2} type"

        else:
            pokemonType = f"{type1} type"

        self.hints = [info["genus"], pokemonType, info["sprite-url"]]

        return entry

    def give_hint(self) -> str:
        """
        Gives out hints
        """
        if self.hints_count >= 3:
            self.playing = False
            return f"<@{self.person}> The answer was {self.answer.title()}"

        else:
            hint = self.hints[self.hints_count]
            self.hints_count += 1

            if self.hints_count == 1:
                hint = f"<@{self.person}> This species is known as the {hint}"

            if self.hints_count == 2:
                hint = f"<@{self.person}> This Pokémon's type is {hint}"

            if self.hints_count == 3:
                hint = f"{hint}"

            return hint

    def make_guess(self, guess: str) -> str:
        """
        Checks the guess
        """
        if guess.lower() == self.answer:
            self.playing = False
            return f"<@{self.person}> Correct!"

        else:
            return f"<@{self.person}> I'm sorry, that's incorrect..."

    def in_game(self) -> bool:
        """
        Returns whether or not a game is being played
        """
        return self.playing
