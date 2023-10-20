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

    def create_supplementary_table(self) -> None:
        """
        Creates a new table with the following schema:
        DEXNUM: INT PRIMARY KEY
        ABILITY1 TEXT NOT NULL
        ABILITY2 TEXT
        HIDDENABILITY TEXT
        TYPE1 TEXT NOT NULL
        TYPE2 TEXT
        SPRITEURL TEXT NOT NULL
        """
        command = """CREATE TABLE IF NOT EXISTS INFORMATION(DEXNUM INT PRIMARY KEY, ABILITY1 TEXT NOT NULL, ABILITY2 TEXT, HIDDENABILITY TEXT, TYPE1 TEXT NOT NULL, TYPE2 TEXT, SPRITEURL TEXT NOT NULL);"""
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

    def insert_info_entry(self, num: int, ability1: str, ability2: str, hiddenability: str, type1: str, type2: str, sprite_url: str) -> None:
        """
        Inserts info into the database
        """
        try:
            command = """INSERT INTO INFORMATION(DEXNUM, ABILITY1, ABILITY2, HIDDENABILITY, TYPE1, TYPE2, SPRITEURL) VALUES(?, ?, ?, ?, ?, ?, ?)"""
            self.db.execute(command, (num, ability1, ability2, hiddenability, type1, type2, sprite_url))

        except sqlite3.IntegrityError:
            print(f"Cannot insert entry: {num} {ability1} {ability2} {hiddenability} {type1} {type2} {sprite_url}")

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
    
    def get_random_data(self) -> dict:
        """
        Returns a dict with the following information about a random Pokemon
        num, name, genus, entry
        """
        command = """SELECT * FROM POKEDEX JOIN INFORMATION ON POKEDEX.NUM = INFORMATION.DEXNUM ORDER BY RANDOM() LIMIT 1"""
        self.cursor.execute(command)
        rows = self.cursor.fetchone()

        data = dict()
        data["num"] = rows[0]
        data["name"] = rows[1]
        data["genus"] = rows[2]
        data["entry"] = rows[3]
        data["ability-1"] = rows[5]
        data["ability-2"] = rows[6]
        data["hidden-ability"] = rows[7]
        data["type-1"] = rows[8]
        data["type-2"] = rows[9]
        data["sprite-url"] = rows[10]

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
