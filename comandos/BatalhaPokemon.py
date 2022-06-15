from turtle import title
from controllers.controllerConquista import ControllerConquista
from controllers.constantes.constantes import BatalhaPokemom
from time import sleep
from discord.ext import commands
import random
import discord
from controllers.controllerPokemon import ControllerPokemon
from entidades.usuarioDiscord import UsuarioDiscord


class Pokemon(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    def get_embed_carregando(self) -> discord.Embed:
        embed = discord.Embed(color=0x992d22, title='CARREGANDO...')
        embed.set_thumbnail(url=BatalhaPokemom.CARREGANDO_PIKACHU)
        embed.set_image(url=BatalhaPokemom.CARREGANDO_CHARMANDER)
        return embed

    # Check

    def check(self, author):
        '''Checa se o usuário que responder é o usuário desafiado'''
        def inner_check(message):
            return message.author == author and message.content in ['1', '2', '3']
        return inner_check

    # choice
    async def escolha(self, usuario: discord.User, ctx, lista) -> bool:
        '''Faz a escolha do usuário'''
        controller_pokemon = ControllerPokemon()

        pokemons = ControllerPokemon.get_pokemon_aleatorio(3)

        embed = discord.Embed(color=0x71368a,
                              title='{} Escolha um pokemon:'.format(usuario.name))
        embed.set_author(name=usuario.name, icon_url=usuario.avatar_url)

        for pokemon in pokemons:
            dados_pokemon = await controller_pokemon.get_pokemon(
                pokemon, False, False, False)

            imagem_tipos = ControllerPokemon.get_imagem_tipo(dados_pokemon)

            if len(imagem_tipos) == 2:
                emoji1 = self.bot.get_emoji(imagem_tipos[0])
                emoji2 = self.bot.get_emoji(imagem_tipos[1])

                embed.add_field(name=dados_pokemon.nome,
                                value='{} {}'.format(emoji1, emoji2))
            else:
                emoji = self.bot.get_emoji(imagem_tipos[0])

                embed.add_field(name=dados_pokemon.nome,
                                value=emoji)

        await ctx.send(embed=embed)

        msg = await self.bot.wait_for('message', check=self.check(usuario))
        lista.append(pokemons[int(msg.content) - 1])
        await msg.delete()
        return True

    async def CadastraPartida(self, ctx, oponente, pokemon_desafio, pokemon_adversario):
        usuario_desafio = UsuarioDiscord(
            id=ctx.author.id, nome=ctx.author.name)

        usuario_adversario = UsuarioDiscord(
            id=oponente.id, nome=oponente.name)

        ganhador = None
        perdedor = None
        pokemon_ganhador = None
        pokemon_perdedor = None
        imagem_ganhador = ''

        if pokemon_adversario.get_hp() > pokemon_desafio.get_hp():
            ganhador = usuario_adversario
            perdedor = usuario_desafio
            pokemon_ganhador = pokemon_adversario
            pokemon_perdedor = pokemon_desafio
            imagem_ganhador = oponente.avatar_url
        else:
            ganhador = usuario_desafio
            perdedor = usuario_adversario
            pokemon_ganhador = pokemon_desafio
            pokemon_perdedor = pokemon_adversario
            imagem_ganhador = ctx.author.avatar_url

        if usuario_adversario.id == usuario_desafio.id:
            await ctx.send('Você não ganhará pontos pois sua partida não teve um adversário!')
            return

        # Cadastra vitoria e derrota
        dados_ganhador = ControllerConquista.post_conquista(
            ganhador, True)  # vitória
        ControllerConquista.post_conquista(perdedor)  # derrota

        # cria embed resultado
        embed_resultado = discord.Embed(
            color=0x992d22, title=f'Vitória de {ganhador.nome}')
        embed_resultado.set_thumbnail(url=pokemon_ganhador.imagem)
        embed_resultado.set_image(url=BatalhaPokemom.ADEUS_PIKACHU)
        embed_resultado.add_field(
            name='Vitórias:', value=dados_ganhador.vitorias, inline=True)
        embed_resultado.add_field(
            name='Derrotas:', value=dados_ganhador.derrotas, inline=True)
        embed_resultado.add_field(  
            name=f'Partidas de {ganhador.nome}:', value=dados_ganhador.partidas, inline=False)
        await ctx.send(embed=embed_resultado)

    async def prepara_duelo(self, ctx: commands.Context, oponente: discord.User):
        escolhas = []

        if(not await self.escolha(ctx.author, ctx, escolhas)):
            exit
        if(not await self.escolha(oponente, ctx, escolhas)):
            exit

        controller_pokemon = ControllerPokemon()

        msg_carregando = await ctx.send(embed=self.get_embed_carregando())

        pokemon_desafio = await controller_pokemon.get_pokemon(escolhas[0])
        pokemon_adversario = await controller_pokemon.get_pokemon(escolhas[1])

        await msg_carregando.delete()
        return (pokemon_desafio, pokemon_adversario)

    @commands.command(name='duelo')
    async def duelo(self, ctx: commands.Context, oponente: discord.User):
        pokemon_desafio, pokemon_adversario = await self.prepara_duelo(ctx, oponente)

        # embed de batalha
        def get_embed_desafio():
            embed_desafio = discord.Embed(color=0x992d22)
            embed_desafio.set_thumbnail(url=pokemon_adversario.imagem)
            embed_desafio.set_image(url=pokemon_desafio.imagem_costas)
            embed_desafio.set_author(name='Vida - {}: {}'.format(pokemon_adversario.get_nome(
            ), pokemon_adversario.get_hp()), icon_url=oponente.avatar_url)
            embed_desafio.set_footer(text='Vida - {}: {}'.format(pokemon_desafio.get_nome(
            ), pokemon_desafio.get_hp()), icon_url=ctx.author.avatar_url)
            return embed_desafio

        def get_embed_adversario():
            embed_adversario = discord.Embed(color=0x206694)
            embed_adversario.set_thumbnail(url=pokemon_desafio.imagem)
            embed_adversario.set_image(url=pokemon_adversario.imagem_costas)
            embed_adversario.set_author(name='Vida - {}: {}'.format(
                pokemon_desafio.get_nome(), pokemon_desafio.get_hp()), icon_url=ctx.author.avatar_url)
            embed_adversario.set_footer(text='Vida - {}: {}'.format(
                pokemon_adversario.get_nome(), pokemon_adversario.get_hp()), icon_url=oponente.avatar_url)
            return embed_adversario

        pokemons = []
        jogadores = []
        embeds = []
        atacante = 0
        defensor = 1
        msg_embed = None

        while True:
            if pokemon_adversario.get_hp() <= 0 or pokemon_desafio.get_hp() <= 0:
                await self.CadastraPartida(ctx, oponente, pokemon_desafio, pokemon_adversario)
                break

            pokemons.clear()
            jogadores.clear()
            embeds.clear()

            if pokemon_desafio.velocidade > pokemon_adversario.velocidade:
                pokemons.append(pokemon_desafio)
                jogadores.append(ctx.author)
                embeds.append(get_embed_desafio())

                pokemons.append(pokemon_adversario)
                jogadores.append(oponente)
                embeds.append(get_embed_adversario())
            else:
                pokemons.append(pokemon_adversario)
                jogadores.append(oponente)
                embeds.append(get_embed_adversario())

                pokemons.append(pokemon_desafio)
                jogadores.append(ctx.author)
                embeds.append(get_embed_desafio())

            habilidade = random.choice(pokemons[atacante].habilidades)
            embeds[atacante].add_field(
                name='ataque', value=pokemons[atacante].atacar(pokemons[defensor], habilidade))

            if msg_embed == None:
                msg_embed = await ctx.send(embed=embeds[atacante])
            else:
                await msg_embed.edit(embed=embeds[atacante])

            if atacante == 0:
                atacante = 1
                defensor = 0
            elif atacante == 1:
                atacante = 0
                defensor = 1

            sleep(6)


def iniciar(bot):
    bot.add_cog(Pokemon(bot))
