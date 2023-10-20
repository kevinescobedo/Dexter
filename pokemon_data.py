import urllib.request
import json

def get_pokemon_info(dexnum: int) -> dict:
    """
    Returns a dict with information from PokeAPI about specified Pokemon
    """
    assert 1 <= dexnum <= 1010
    link = f"https://pokeapi.co/api/v2/pokemon-species/{dexnum}"
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(request)
    result = json.loads(response.read())

    data = dict()
    data["num"] = dexnum
    
    name_information = result["names"]
    for name in name_information:
        if name["language"]["name"] == "en":
            data["name"] = name["name"].strip()
            break

    general_information = result["genera"]
    for information in general_information:
        if information["language"]["name"] == "en":
            data["genus"] = information["genus"].strip()
            break

    dex_information = result["flavor_text_entries"]
    for dexinfo in dex_information:
        if dexinfo["language"]["name"] == "en":
            data["entry"] = dexinfo["flavor_text"].strip().replace("\n", " ")
            break

    return data

def get_supplementary_info(dexnum: int) -> dict:
    """
    Returns a dictionary with supplementary information on the Pokémon
    """
    assert 1 <= dexnum <= 1010
    link = f"https://pokeapi.co/api/v2/pokemon/{dexnum}"
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(request)
    result = json.loads(response.read())

    data = dict()
    data["num"] = dexnum
    ability_info = result["abilities"]
    abilities = [None, None, None]

    for i, sub_info in enumerate(ability_info):
        abilityName = sub_info["ability"]["name"].title()
        abilities[sub_info["slot"] - 1] = abilityName

    data["ability1"] = abilities[0]
    data["ability2"] = abilities[1]
    data["hiddenability"] = abilities[2]

    type_info = result["types"]
    types = [None, None]

    for i, sub_info in enumerate(type_info):
        typeName = sub_info["type"]["name"].title()
        types[sub_info["slot"] - 1] = typeName

    data["type1"] = types[0]
    data["type2"] = types[1]

    data["sprite-link"] = result["sprites"]["front_default"]

    return data

if __name__ == "__main__":
    dexnum = 25
    print(get_pokemon_info(dexnum))
    print(get_supplementary_info(dexnum))
