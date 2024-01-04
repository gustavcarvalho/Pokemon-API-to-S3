from aiohttp import ClientSession
from asyncio import gather, run

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
            
    return list(dict.fromkeys(names))
    
#['flying', 'poison', 'bug', 'fire', 'ice']
async def pokemon_weakness(session: ClientSession, pokemon_types, base_url):
    weakness = list()
        
    for pokemon_type in pokemon_types:
        async with session.get(f'{base_url}type/{pokemon_type}') as response:
            response = await response.json()
            weakness = [x['name'] for x in response['damage_relations']['double_damage_from']]
            # weakness.append(response['damage_relations']['double_damage_from'])
            return weakness
    
async def pokemon_id_number(session: ClientSession, base_url):
    async with session.get(f'{base_url}pokemon/') as response:
        number_of_ids = await response.json()
        return number_of_ids['count']

async def fetch_pokemon_data(session: ClientSession, base_url, ids):
    pokemon_data = dict()

    async with session.get(f'{base_url}pokemon/{ids}') as response:
        response = await response.json()
        pokemon_id = response['id']
        pokemon_name = response['name']
        pokemon_types = [t['type']['name'] for t in response['types']]
        pokemon_ability = response['abilities'][0]['ability']['name']

    # Weakness function applied to "pokemon_types"
    pokemon_types_weakness = await pokemon_weakness(session, pokemon_types, base_url)

    # Cathing "pokemon-species" and "" endpoint informations
    async with session.get(f'{base_url}pokemon-species/{ids}') as response:
        pokemon_info_species = await response.json()
        pokemon_generation = pokemon_info_species['generation']['name']
        pokemon_pokedex_number = pokemon_info_species['pokedex_numbers'][0]['entry_number']


    async with session.get(pokemon_info_species['evolution_chain']['url']) as response:
        pokemon_info_evolution = await response.json()
        pokemon_evolution_chain = extract_species_names(pokemon_info_evolution['chain'])
    
    pokemon_data[pokemon_id] = {'Pokedex Number': pokemon_pokedex_number, 'Name': pokemon_name, 'Type': pokemon_types, 'Weakness': pokemon_types_weakness, 'Ability': pokemon_ability, 'Generation': pokemon_generation,'Evolution Chain': pokemon_evolution_chain}

    return pokemon_data


async def main() -> None:
    pokemon_data = dict()
    base_url = 'https://pokeapi.co/api/v2/'

    async with ClientSession() as session:
        pokemon_ids = await pokemon_id_number(session=session, base_url=base_url)

        
        tasks = [fetch_pokemon_data(session, base_url, ids) for ids in range(1, pokemon_ids - 277)]
        responses = await gather(*tasks)
        print(responses)
        


        print(pokemon_data)

if __name__ == "__main__":
    run(main())



#