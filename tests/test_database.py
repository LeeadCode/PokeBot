import pytest

from src.database import Database
from src.models.move import DamageClass, Move, MoveMeta, Type

mock_move_meta = [
    MoveMeta(
        ailment_chance=0,
        max_turns=None,
        min_hits=None,
        min_turns=None,
        max_hits=None,
        healing=0,
        drain=0,
        crit_rate=0,
        stat_chance=0,
        meta_category={'name': 'damage'},
        meta_ailment={'name': 'none'},
        flinch_chance=0,
    )
]


@pytest.fixture
def db():
    db = Database()
    db.move_data = [
        Move(
            id=1,
            name='Move1',
            type=Type(name='Fire'),
            damageClass=DamageClass(name='physical'),
            accuracy=None,
            power=None,
            pp=None,
            move_meta=mock_move_meta,
            meta_stat_changes=[],
            target={
                'name': 'selected-pokemon',
            },
        ),
        Move(
            id=2,
            name='Move2',
            type=Type(name='Water'),
            damageClass=DamageClass(name='special'),
            accuracy=None,
            power=None,
            pp=None,
            move_meta=mock_move_meta,
            meta_stat_changes=[],
            target={
                'name': 'selected-pokemon',
            },
        ),
        Move(
            id=3,
            name='Move3',
            type=Type(name='Fire'),
            damageClass=DamageClass(name='physical'),
            accuracy=None,
            power=None,
            pp=None,
            move_meta=mock_move_meta,
            meta_stat_changes=[],
            target={
                'name': 'selected-pokemon',
            },
        ),
        Move(
            id=4,
            name='Move4',
            type=Type(name='Grass'),
            damageClass=DamageClass(name='status'),
            accuracy=None,
            power=None,
            pp=None,
            move_meta=mock_move_meta,
            meta_stat_changes=[],
            target={
                'name': 'selected-pokemon',
            },
        ),
    ]
    return db


def test_get_moves_to_battle_no_limit(db):
    result = db.get_moves_to_battle(types=['Fire'])
    assert len(result) == 2
    assert result[0].name == 'Move1'


def test_get_moves_to_battle_with_limit(db):
    result = db.get_moves_to_battle(types=['Fire', 'Water'], limit=1)
    assert len(result) == 1


def test_get_moves_to_battle_multiple_types(db):
    result = db.get_moves_to_battle(types=['Fire', 'Water'])
    assert len(result) == 3
    assert any(move.name == 'Move1' for move in result)
    assert any(move.name == 'Move2' for move in result)


def test_get_moves_to_battle_no_matching_type(db):
    result = db.get_moves_to_battle(types=['Electric'])
    assert len(result) == 0


def test_get_moves_to_battle_excludes_status(db):
    result = db.get_moves_to_battle(types=['Grass'])
    assert len(result) == 0
    assert len(result) == 0
