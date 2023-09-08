import requests

def extract_species_names(data):
    names = list()

    if 'species' in data:
        species_data = data['species']
        if 'name' in species_data:
            names.append(species_data['name'])
        for evolution in data['evolves_to']:
            if 'species' in evolution:
                species_data = evolution['species']
                if 'name' in species_data:
                    names.append(species_data['name'])
            names.extend(extract_species_names(evolution))
            
    names = list(dict.fromkeys(names))
    return names

def pokemon_weakness(pokemon_types, base_url):
    weakness = list()
        
    for pokemon_type in pokemon_types:
        type_weakness = requests.get(f'{base_url}type/{pokemon_type}').json()
        type_weakness = type_weakness['damage_relations']['double_damage_from']
        for type_weakness_values in type_weakness:
            type_weakness_values['name']
            weakness.append(type_weakness_values)
    
    return weakness


def fetch_pokemon_data():
    pokemon_data = dict()
    base_url = 'https://pokeapi.co/api/v2/'

    number_of_ids = requests.get(f'{base_url}pokemon/').json()
    number_of_ids = number_of_ids['count']

    try:
        for ids in range(1, number_of_ids + 1):
            
            # Cathing "pokemon" endpoint informations
            pokemon_info = requests.get(f'{base_url}pokemon/{ids}').json()
            pokemon_id = pokemon_info['id']
            pokemon_name = pokemon_info['name']
            pokemon_types = [t['type']['name'] for t in pokemon_info['types']]
            pokemon_ability = pokemon_info['abilities'][0]['ability']['name']

            # Weakness function applied to "pokemon_types"
            pokemon_types_weakness = pokemon_weakness(pokemon_types, base_url)

            # Cathing "pokemon-species" and "" endpoint informations
            pokemon_info_species = requests.get(f'{base_url}pokemon-species/{ids}').json()
            pokemon_generation = pokemon_info_species['generation']['name']
            pokemon_pokedex_number = pokemon_info_species['pokedex_numbers'][0]['entry_number']


            pokemon_info_evolution = requests.get(pokemon_info_species['evolution_chain']['url']).json()
            pokemon_evolution_chain = extract_species_names(pokemon_info_evolution['chain'])


            

            pokemon_data[pokemon_id] = {'Pokedex Number': pokemon_pokedex_number, 'Name': pokemon_name, 'Type': pokemon_types, 'Weakness': pokemon_types_weakness, 'Ability': pokemon_ability, 'Generation': pokemon_generation,'Evolution Chain': pokemon_evolution_chain}

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")


    print(pokemon_data)

if __name__ == "__main__":
    fetch_pokemon_data()
