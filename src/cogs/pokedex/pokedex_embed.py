import discord
from utils.emoji_type import get_type_emojis
from utils.status_bar import status_bar

def create_pokedex_embed(pokemon):
    embed = discord.Embed(
        color=0x0099ff,
        title=f"{pokemon['name']['english']} - {pokemon['species']}",
    )
    
    # Author (autor da embed)
    embed.set_author(
        name="Pokedex",
        icon_url=pokemon['sprites']['frontDefault']
    )
    
    # Thumbnail
    embed.set_thumbnail(url=pokemon['sprites']['other']['showdown']['frontDefault'])
    
    # Adicionando os campos principais
    embed.add_field(
        name="Weight",
        value=str(pokemon['profile']['weight']),
        inline=True
    )
    embed.add_field(
        name="Height",
        value=str(pokemon['profile']['height']),
        inline=True
    )
    embed.add_field(
        name="Type",
        value=get_type_emojis(pokemon['type']),
        inline=True
    )
    
    # Imagem principal
    embed.set_image(url=pokemon['sprites']['other']['oficialArtWork']['default'])
    
    # Adicionando os campos de status
    embed.add_field(
        name="💚 HP",
        value=status_bar(pokemon['base']['hp']),
        inline=False
    )
    embed.add_field(
        name="⚔️ Attack",
        value=status_bar(pokemon['base']['attack']),
        inline=True
    )
    embed.add_field(
        name="🛡️ Defense",
        value=status_bar(pokemon['base']['defense']),
        inline=False
    )
    embed.add_field(
        name="🪄 Sp. Attack",
        value=status_bar(pokemon['base']['spAttack']),
        inline=False
    )
    embed.add_field(
        name="✨ Sp. Defense",
        value=status_bar(pokemon['base']['spDefense']),
        inline=False
    )
    embed.add_field(
        name="⚡ Speed",
        value=status_bar(pokemon['base']['speed']),
        inline=False
    )
    
    # Footer
    embed.set_footer(
        text=pokemon['description'],
        icon_url="https://cdn-icons-png.flaticon.com/128/528/528101.png"
    )
    
    return embed
