import requests

def fetch_pokemon_data():
    base_url = 'https://pokeapi.co/api/v2/'
    data = requests.get(base_url).json()
    pokemon_data = dict()
    response = requests.get(f'{base_url}pokemon/?limit={data["count"]}')
    response.raise_for_status()
    pokemon_list = response.json()['results']

    for pokemon_info in pokemon_list:
        pokemon_url = pokemon_info['url']
        response_pokemon = requests.get(pokemon_url).json()
        pokemon_id = response_pokemon['id']
        pokemon_name = response_pokemon['name']
        pokemon_types = [t['type']['name'] for t in response_pokemon['types']]
        pokemon_ability = response_pokemon['abilities']['ability']['name']
        pokemon_data[pokemon_id] = {'Name': pokemon_name, 'Type': pokemon_types, 'Abilities': pokemon_ability}

    print(pokemon_data)

if __name__ == "__main__":
    fetch_pokemon_data()
