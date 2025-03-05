import json
import os
import random
from typing import List

from models.move import Move
from models.pokemon import DreamWorld, Home, OficialArtWork, Other, Pokemon, Showdown, Sprites


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.pokemon_data: List[Pokemon] = []
        self.move_data: List[Move] = []

        # Carregar Pokémon do JSON
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'pokemons.json'), 'r', encoding='utf-8') as f:
            raw_pokemon_data = json.load(f)
            self.pokemon_data = [Pokemon(**p) for p in raw_pokemon_data]

        # Carregar Moves do JSON
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'moves.json'), 'r', encoding='utf-8') as f:
            raw_move_data = json.load(f)
            self.move_data = [Move(**m) for m in raw_move_data]

        # Configurar sprites para cada Pokémon
        for p in self.pokemon_data:
            p.sprites = self.get_sprites(p.id)

    @classmethod
    def get_sprites(self, id: int) -> Sprites:
        official_artwork = OficialArtWork(
            default=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png'
        )

        dream_world = DreamWorld(frontDefault=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/{id}.svg')

        home = Home(
            frontDefault=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{id}.png',
            frontShiny=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/{id}.png',
        )

        showdown = Showdown(
            backDefault=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/{id}.gif',
            backShiny=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/shiny/{id}.gif',
            frontDefault=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{id}.gif',
            frontShiny=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{id}.gif',
        )

        # Instância de 'other' com os modelos internos
        other = Other(oficial_artWork=official_artwork, dream_world=dream_world, home=home, showdown=showdown)

        # Retorna a instância do modelo 'Sprites'
        return Sprites(
            backDefault=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{id}.png',
            backShiny=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/{id}.png',
            frontDefault=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png',
            frontShiny=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{id}.png',
            other=other,
        )

    def get_all(self) -> List[Pokemon]:
        return self.pokemon_data

    def get_by_id(self, id: int) -> Pokemon | None:
        return next((p for p in self.pokemon_data if p.id == id), None)

    def get_by_name(self, name: str) -> Pokemon:
        pokemon = next((p for p in self.pokemon_data if p.name.english.lower() == name.lower()), None)

        if pokemon is None:
            raise ValueError(f"Pokémon com o nome '{name}' não encontrado.")
        return pokemon

    def get_random(self) -> Pokemon:
        return random.choice(self.pokemon_data)

    def get_random_distinct_pokemon(self, count: int) -> List[Pokemon]:
        return random.sample(self.pokemon_data, count)

    def get_moves_by_type(self, type_name: str, limit: int = 0) -> List[Move]:
        filtered = [m for m in self.move_data if m.type.name.lower() == type_name.lower()]
        return filtered[:limit] if limit else filtered

    def get_moves_to_battle(self, types: List[str], limit: int = 0) -> List[Move]:
        filtered = [
            m for m in self.move_data if m.type.name.lower() in [t.lower() for t in types] and m.move_meta and m.damage_class.name != 'status'
        ]
        return filtered[:limit] if limit else filtered
