from discord.ext import commands
import discord
from controllers.controllerPokemon import ControllerPokemon


class CacaPokemon(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot


    @commands.command(name='cacar')
    async def get_pokemon(self, ctx):


        controllerpokemon = ControllerPokemon()   

        pokemon_aleatorio = ControllerPokemon.get_pokemon_aleatorio(1)
        image_pokemon = await controllerpokemon.get_pokemon(nome_pokemon= pokemon_aleatorio[0])


        embed = discord.Embed(
            title=pokemon_aleatorio[0],
            color=0xFF0000)

        embed.set_author(name = "VOCÊ ENCONTROU UM: ")
        embed.set_image(url=image_pokemon.arte_oficial)    

        embed.set_footer(text="1-Capturar                                                                        2-Sair")
        

        await ctx.send(embed=embed) 

           

def iniciar(bot):
    bot.add_cog(CacaPokemon(bot))           