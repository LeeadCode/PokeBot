import discord
from typing import Optional
from discord import User
from models.pokemon import Pokemon


def wtp_successful_embed(user: Optional[User], pokemon: Pokemon) -> discord.Embed:
    embed = discord.Embed(title=f'{user.display_name if user else "Alguém"} Acertou!', color=0x0099FF)

    avatar_url = (
        f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpeg'
        if user and user.avatar
        else f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon.id}.png'
    )

    embed.set_author(name=pokemon.name.english, icon_url=avatar_url)
    embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/128/528/528101.png')
    embed.set_image(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon.id}.png')
    embed.set_footer(text='PokeBot 2024', icon_url='https://cdn-icons-png.flaticon.com/128/528/528101.png')

    return embed
