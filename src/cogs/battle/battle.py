import asyncio
import random
from discord import User
from emmiter import emitter


class BattleEvent:
    ATTACK = 'ATTACK'
    BATTLE_END = 'BATTLE_END'


class BattlePokemon:
    def __init__(self, pokemon):
        self.__dict__.update(pokemon.__dict__)
        self.battle_name = pokemon.name['english']
        self.base['accuracy'] = 100
        self.base['evasion'] = 100
        self.max_hp = pokemon.base['hp']
        self.battle_info = BattleInfo()

    def handle_stats_change(self, target, move):
        if not hasattr(move, 'meta_stat_changes'):
            return

        if move.move_effect_chance and move.move_effect_chance <= random.randint(0, 100):
            return

        modifiers = [1 / 4, 2 / 7, 1 / 3, 2 / 5, 1 / 2, 2 / 3, 1, 3 / 2, 2, 5 / 2, 3, 7 / 2, 4]

        for s in move.meta_stat_changes:
            index = s.change + 6
            target.base[s.stat.name] *= modifiers[index]
            change_text = f'{target.battle_name} {s.stat.name} {"+" if s.change > 0 else ""}{s.change}'
            self.battle_info.add_stats_change(change_text)

    def handle_drain(self, target, move):
        damage = self.calc_damage(target, move)
        heal = (move.move_meta[0].drain / 100) * damage
        target.base['hp'] -= damage
        self.base['hp'] += heal
        self.battle_info.add_stats_change(f'{self.battle_name} drained {heal} hp')

    def calc_damage(self, target, move):
        atk_power = self.base['sp_attack'] if move.damage_class.name == 'special' else self.base['attack']
        defense_eff = target.base['sp_defense'] if move.damage_class.name == 'special' else target.base['defense']

        stab = 1.5 if move.type.name in self.type else 1

        critical = 1.5 if move.move_meta and move.move_meta[0].crit_rate < random.randint(0, 100) else 1

        damage = round(((((2 * 1 / 5 + 2) * atk_power * move.power / defense_eff) / 50) + 2) * stab * 1 * critical * (80 / 100))

        self.battle_info.add_info(f"""\U0001f4a5 {self.battle_name} used
                                  {move.name} dealing {damage} damage""")
        return damage

    def handle_move(self, target, move):
        hit = move.accuracy * (self.base['accuracy'] / target.base['evasion']) >= random.randint(0, 100)
        if not hit:
            self.battle_info.add_info(f'{self.battle_name} missed {move.name}!')
            return

        category = move.move_meta[0].meta_category.name
        self.battle_info.set_move_type(category)

        if category == 'damage':
            target.base['hp'] -= self.calc_damage(target, move)
        elif category in {'damage+raise', 'damage+lower'}:
            self.handle_stats_change(target if category == 'damage+lower' else self, move)
            target.base['hp'] -= self.calc_damage(target, move)
        elif category == 'damage+heal':
            self.handle_drain(target, move)
        elif category == 'ohko':
            target.base['hp'] = 0
            self.battle_info.add_info(
                f"""\U0001f94a {self.battle_name} used
                {move.name} and knocked out {target.battle_name}"""
            )
        else:
            self.battle_info.add_info('sem implementação ainda')

    def attack(self, target):
        self.battle_info.reset()
        move = random.choice(self.moves)
        self.handle_move(target, move)
        return self.battle_info


class BattleInfo:
    def __init__(self):
        self.move_type = ''
        self.info_text = ''
        self.stats_change = []
        self.attack_player = None
        self.defend_player = None

    def add_stats_change(self, stat):
        self.stats_change.append(stat)

    def add_info(self, info):
        self.info_text = info

    def set_move_type(self, type_name):
        move_types = {
            'damage': 'Attack ⚔️',
            'ailment': 'Ailment ⚰️',
            'net-good-stats': 'Good Stats 🎲',
            'heal': 'Heal 💚',
            'damage+ailment': 'Attack ⚔️ and Ailment ⚰️',
            'swagger': 'Swagger 🕶️',
            'damage+lower': 'Attack ⚔️ and Lower 📉',
            'damage+raise': 'Attack ⚔️ and Raise 📈',
            'damage+heal': 'Attack ⚔️ and Heal 💚',
            'ohko': 'KO! 🥊',
        }
        self.move_type = move_types.get(type_name, 'Unknown Move')

    def reset(self):
        self.info_text = ''
        self.move_type = ''
        self.stats_change = []

    def __str__(self):
        return self.info_text


class Battle(emitter):
    def __init__(self, player1: User, player2: User, pokemon1, pokemon2):
        super().__init__()
        self.player1 = {'user': player1, 'pokemon': BattlePokemon(pokemon1)}
        self.player2 = {'user': player2, 'pokemon': BattlePokemon(pokemon2)}

    async def start(self, client):
        self.player1['pokemon'].moves = client.database.get_moves_to_battle(self.player1['pokemon'].type)

        self.player2['pokemon'].moves = client.database.get_moves_to_battle(self.player2['pokemon'].type)

        if self.player1['pokemon'].base['speed'] > self.player2['pokemon'].base['speed']:
            await self.battle(self.player1, self.player2)
        else:
            await self.battle(self.player2, self.player1)

    async def battle(self, attack_player, defend_player):
        info = attack_player['pokemon'].attack(defend_player['pokemon'])
        info.attack_player = attack_player
        info.defend_player = defend_player
        self.emit(BattleEvent.ATTACK, info)

        if defend_player['pokemon'].base['hp'] <= 0:
            self.emit(BattleEvent.BATTLE_END, {'winner': attack_player, 'loser': defend_player})
            return

        await asyncio.sleep(3)
        await self.battle(defend_player, attack_player)
