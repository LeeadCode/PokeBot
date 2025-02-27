import json
import os

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.pokemon_data = []
        self.move_data = []

        # Carregar Pokémon e Moves dos arquivos JSON
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'pokemons.json'), 'r', encoding='utf-8') as f:
            self.pokemon_data = json.load(f)

        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'moves.json'), 'r', encoding='utf-8') as f:
            self.move_data = json.load(f)

        # Configurar sprites para cada Pokémon
        for p in self.pokemon_data:
            p['sprites'] = self.get_sprites(p['id'])

    def get_sprites(self, id):
        return {
            'backDefault': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{id}.png",
            'backShiny': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/{id}.png",
            'frontDefault': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png",
            'frontShiny': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{id}.png",
            'other': {
                'oficialArtWork': {
                    'default': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png",
                },
                'dreamWorld': {
                    'frontDefault': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/{id}.svg",
                },
                'home': {
                    'frontDefault': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{id}.png",
                    'frontShiny': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/{id}.png",
                },
                'showdown': {
                    'backDefault': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/{id}.gif",
                    'backShiny': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/shiny/{id}.gif",
                    'frontDefault': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{id}.gif",
                    'frontShiny': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{id}.gif",
                },
            }
        }

    def get_all(self):
        return self.pokemon_data
        
    def get_by_id(self, id):
        return next((p for p in self.pokemon_data if p['id'] == id), None)

    def get_by_name(self, name):
        pokemon = next((p for p in self.pokemon_data if p['name']['english'].lower() == name.lower()), None)
        if pokemon is None:
            raise ValueError(f"Pokemon with name '{name}' not found.")
        return pokemon

    def get_random(self):
        import random
        return random.choice(self.pokemon_data)

    def get_random_distinct_pokemons(self, count):
        import random
        return random.sample(self.pokemon_data, count)

    def get_moves_by_type(self, type, limit=0):
        filtered = [m for m in self.move_data if m['type']['name'] == type]
        return filtered[:limit] if limit else filtered

    def get_moves_to_battle(self, types, limit=0):
        filtered = [m for m in self.move_data if m['type']['name'].lower() in [t.lower() for t in types] and len(m.get('moveMeta', [])) > 0 and m['damageClass']['name'] != 'status']
        return filtered[:limit] if limit else filtered
