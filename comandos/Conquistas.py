from discord.ext import commands
import discord
from controllers.controllerConquista import ControllerConquista

class ConquistasPokemon(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command(name='conquistas')
    async def visualiza_conquistas(self, ctx, usuario: discord.User = None):
        dados_conquista = None
        dados_usuario = None

        if usuario == None:
            dados_conquista = ControllerConquista.get_conquista(ctx.author.id)
            dados_usuario = ctx.author
        else:
            dados_conquista = ControllerConquista.get_conquista(usuario.id)
            dados_usuario = usuario

        embed = discord.Embed(color=0x992d22)
        embed.set_thumbnail(url=dados_usuario.avatar_url)
        embed.set_author(
            name=f'Partidas de - {dados_usuario.name}: {dados_conquista.partidas}')
        embed.add_field(name='Vitórias:',
                        value=dados_conquista.vitorias, inline=True)
        embed.add_field(name='Derrotas:',
                        value=dados_conquista.derrotas, inline=True)
        await ctx.send(embed=embed)

def iniciar(bot):
    bot.add_cog(ConquistasPokemon(bot))