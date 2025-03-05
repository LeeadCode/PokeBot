from .custom_model_base import ModelBase
from typing import List, Optional
from .move import Move


class Name(ModelBase):
    english: str
    japanese: str
    chinese: str
    french: str


def camel_to_snake(string: str) -> str:
    return ''.join([string[0].lower()] + [char if char.islower() else f'_{char.lower()}' for char in string[1:]])


class BaseStats(ModelBase):
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    evasion: Optional[int] = 0
    accuracy: Optional[int] = 0


class Profile(ModelBase):
    height: str
    weight: str
    egg: List[str]
    ability: List[List[str]]
    gender: str


class OficialArtWork(ModelBase):
    default: str


class DreamWorld(ModelBase):
    frontDefault: str


class Home(ModelBase):
    front_default: str
    front_shiny: str


class Showdown(ModelBase):
    back_default: str
    back_shiny: str
    front_default: str
    front_shiny: str


class Other(ModelBase):
    oficial_artWork: OficialArtWork
    dream_world: DreamWorld
    home: Home
    showdown: Showdown


class Sprites(ModelBase):
    back_default: str
    back_shiny: str
    front_default: str
    front_shiny: str
    other: Other


class Pokemon(ModelBase):
    id: int
    name: Name
    type: List[str]
    base: BaseStats
    species: str
    description: str
    profile: Profile
    sprites: Optional[Sprites] = None
    moves: Optional[List[Move]] = None
