import discord
from utils.emoji_type import get_type_emojis


def battle_choice_embed(user: discord.User, choices) -> discord.Embed:
    embed = discord.Embed(color=0x0099FF, title=f'{user.mention} Choose your Pokémon!')
    embed.set_author(name=user.display_name, icon_url=user.avatar.url if user.avatar else '')
    embed.set_footer(text='PokeBot 2024', icon_url='https://cdn-icons-png.flaticon.com/128/528/528101.png')

    # Adicionando os campos com os Pokémons disponíveis
    for p in choices:
        embed.add_field(name=p.name['english'], value=get_type_emojis(p.type), inline=False)

    return embed
