import sqlite3

class PokemonDatabase:
    def __init__(self, name: str="pokedex.db"):
        self.db = sqlite3.connect(name, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)
        self.cursor = self.db.cursor()

    def create_table(self) -> None:
        """
        Creates a new table with the following schema:
        DEXNUM: INT PRIMARY KEY
        NAME: TEXT NOT NULL
        GENUS: TEXT NOT NULL
        ENTRY: TEXT NOT NULL
        """
        command = """CREATE TABLE IF NOT EXISTS POKEDEX(NUM INT PRIMARY KEY, NAME TEXT NOT NULL, GENUS TEXT NOT NULL, ENTRY TEXT NOT NULL)"""
        self.db.execute(command)
        self.flush()

    def insert_entry(self, num: int, name: str, genus: str, entry: str) -> None:
        """
        Inserts entry into pokedex table
        """
        try:
            command = """INSERT INTO POKEDEX(NUM, NAME, GENUS, ENTRY) VALUES(?, ?, ?, ?) """
            self.db.execute(command, (num, name, genus, entry))
        
        except sqlite3.IntegrityError:
            print(f"Cannot insert entry: {num} {name} {genus} {entry}")

    def get_data(self, num: int) -> dict:
        """
        Returns a dict with the following information:
        num, name, genus, entry
        """
        command = f"""SELECT * FROM POKEDEX WHERE NUM = {num}"""
        self.cursor.execute(command)
        rows = self.cursor.fetchone()

        data = dict()
        data["num"] = rows[0]
        data["name"] = rows[1]
        data["genus"] = rows[2]
        data["entry"] = rows[3]

        return data

    def flush(self) -> None:
        """
        Flushes any outstanding commits to the database
        """
        self.db.commit()

    def close(self) -> None:
        """
        Closes connection to the database
        """
        self.flush()
        self.db.close()



if __name__ == "__main__":
    pokedex = PokemonDatabase()
    pokedex.create_table()
    pokedex.close()
