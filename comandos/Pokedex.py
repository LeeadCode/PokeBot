from discord.ext import commands
import discord
import requests
from controllers.controllerPokemon import ControllerPokemon


class Pokedex(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command(name='pokedex')
    async def get_pokemon(self, ctx, pokemon):
        try:
            controller_pokemon = ControllerPokemon()
            dados_pokemon = await controller_pokemon.get_pokemon(
                pokemon, False, False)

            embed = discord.Embed(
                title=dados_pokemon.nome,
                color=0xFF0000)

            embed.set_author(
                name="Pokemon:", icon_url='https://cdn-icons-png.flaticon.com/128/188/188931.png')
            embed.set_image(url=dados_pokemon.arte_oficial)

            embed.set_thumbnail(
                url='https://cdn-icons-png.flaticon.com/128/528/528101.png')

            imagem_tipos = ControllerPokemon.get_imagem_tipo(dados_pokemon)

            if len(imagem_tipos) == 2:
                emoji1 = self.bot.get_emoji(imagem_tipos[0])
                emoji2 = self.bot.get_emoji(imagem_tipos[1])

                embed.add_field(
                    name='Tipo', value='{} {}'.format(emoji1, emoji2), inline=False)
            else:
                emoji = self.bot.get_emoji(imagem_tipos[0])
                embed.add_field(
                    name='Tipo', value=emoji, inline=False)

            embed.add_field(name="Peso", value="{} Kg".format(
                dados_pokemon.peso / 10))
            embed.add_field(name="Altura", value='{} m'.format(
                dados_pokemon.tamanho / 10))

            await ctx.send(embed=embed)
        except requests.exceptions.JSONDecodeError:
            await ctx.send('Pokémon não encontrado!')


def iniciar(bot):
    bot.add_cog(Pokedex(bot))
