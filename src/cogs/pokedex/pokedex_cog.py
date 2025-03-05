import discord
from discord import app_commands
from discord.ext import commands
from models.pokemon import Pokemon
from .pokedex_embed import create_pokedex_embed


class Pokedex(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='pokedex', description='Pokedex')
    @app_commands.describe(pokemon_name='Digite o nome do Pokémon')
    async def pokedex(self, interaction: discord.Interaction, pokemon_name: int):
        try:
            pokemon = self.bot.database.get_by_id(pokemon_name)
            if pokemon:
                embed = create_pokedex_embed(pokemon)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('Não foi encontrado nenhum Pokémon com suas descrições! 😢', ephemeral=True)

        except Exception as e:
            print(e)

    @pokedex.autocomplete('pokemon_name')
    async def pokedex_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            # Obter o valor do campo focado
            focused_value = current

            # Filtrar dados de Pokemon
            pokemon_list: Pokemon = self.bot.database.get_all()

            filtered = [p for p in pokemon_list if p.name.english.lower().startswith(focused_value.lower())]

            # Limitar a 25 sugestoes
            limited_filtered = filtered[:25]

            # Responder com as sugestoes
            await interaction.response.autocomplete(choices=[app_commands.Choice(name=p.name.english, value=p.id) for p in limited_filtered])
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Pokedex(bot))
