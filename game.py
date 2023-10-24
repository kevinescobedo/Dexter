import pokemon_database

class Game:
    def __init__(self, discordID: int):
        self.person = discordID
        self.pokedex = pokemon_database.PokemonDatabase()

    def startGame(self) -> None:
        """
        Starts the game by getting a random Pokedex entry and setting the hints
        """
        pass
