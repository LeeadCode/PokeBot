from typing import List, Literal, Optional

from .custom_model_base import ModelBase


class Type(ModelBase):
    name: str


class Target(ModelBase):
    name: str


class DamageClass(ModelBase):
    name: str


class MetaAilment(ModelBase):
    name: Literal[
        'unknown',
        'none',
        'paralysis',
        'sleep',
        'freeze',
        'burn',
        'poison',
        'confusion',
        'infatuation',
        'trap',
        'nightmare',
        'torment',
        'disable',
        'yawn',
        'heal-block',
        'no-type-immunity',
        'leech-seed',
        'embargo',
        'perish-song',
        'ingrain',
        'tar-shot',
        'silence',
    ]


class MetaCategory(ModelBase):
    name: Literal[
        'damage',
        'ailment',
        'net-good-stats',
        'heal',
        'damage+ailment',
        'swagger',
        'damage+lower',
        'damage+raise',
        'damage+heal',
        'ohko',
        'whole-field-effect',
        'field-effect',
        'force-switch',
        'unique',
    ]


class MetaStatChange(ModelBase):
    stat: Type
    change: int


class MoveMeta(ModelBase):
    ailment_chance: int
    max_turns: Optional[int] = None
    min_hits: Optional[int] = None
    min_turns: Optional[int] = None
    max_hits: Optional[int] = None
    healing: int
    drain: int
    crit_rate: int
    stat_chance: int
    meta_category: MetaCategory
    meta_ailment: MetaAilment
    flinch_chance: int


class Move(ModelBase):
    name: str
    accuracy: Optional[int]
    power: Optional[int]
    pp: Optional[int]
    move_effect_chance: Optional[int] = None
    type: Type
    move_meta: Optional[List[MoveMeta]] = None
    meta_stat_changes: List[MetaStatChange]
    target: Target
    damage_class: DamageClass
    damage_class: DamageClass
