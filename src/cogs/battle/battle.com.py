import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from typing import Dict
from battle import Battle, BattleEvent, BattleInfo
from database import get_random_distinct_pokemons
from .battle_choice_embed import battle_choice_embed
from .battle_embed import battle_embed


class BattleCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='battle', description='Pokemon battle!')
    @app_commands.describe(user='Choose who you want to challenge!')
    async def battle(self, interaction: discord.Interaction, user: discord.User):
        if user == interaction.user:
            await interaction.response.send_message('You cannot battle yourself!', ephemeral=True)
            return

        pokemons_choices: Dict[str, dict] = {}

        async def user_choice(user: discord.User) -> discord.Interaction:
            random_pokemons = get_random_distinct_pokemons(3)
            for p in random_pokemons:
                pokemons_choices[p['name']['english']] = p

            buttons = [
                discord.ui.Button(label=p['name']['english'], style=discord.ButtonStyle.success, custom_id=p['name']['english'])
                for p in random_pokemons
            ]
            row = discord.ui.View()
            for button in buttons:
                row.add_item(button)

            await interaction.response.send_message(embed=battle_choice_embed(user, *random_pokemons), view=row)

            def check(i: discord.Interaction):
                return i.user.id == user.id and i.data['custom_id'] in pokemons_choices

            try:
                choice = await self.bot.wait_for('interaction', check=check, timeout=15.0)
                return choice
            except asyncio.TimeoutError:
                await interaction.edit_original_response(content='Timeout :(', view=None)
                return None

        choice1 = await user_choice(interaction.user)
        if not choice1:
            return
        await choice1.response.send_message(f'{choice1.user.display_name} made their choice!')

        choice2 = await user_choice(user)
        if not choice2:
            return
        await choice2.response.send_message(f'{user.display_name} made their choice!')

        pokemon1 = pokemons_choices.get(choice1.data['custom_id'])
        pokemon2 = pokemons_choices.get(choice2.data['custom_id'])
        if not pokemon1 or not pokemon2:
            return

        battle = Battle(interaction.user, user, pokemon1, pokemon2)

        async def battle_attack_handler(info: BattleInfo):
            await interaction.edit_original_response(embed=battle_embed(info), view=None)

        battle.on(BattleEvent.attack, battle_attack_handler)

        await battle.start(self.bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(BattleCommand(bot))
