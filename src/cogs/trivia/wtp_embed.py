import discord

def wtp_embed():
    embed = discord.Embed(
        title="Quem é esse Pokémon?",
        color=0x0099FF
    )
    embed.set_author(name="Who's That Pokémon?")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/128/528/528101.png")
    embed.set_image(url="attachment://silhouette.png")
    embed.set_footer(
        text="PokeBot 2024",
        icon_url="https://cdn-icons-png.flaticon.com/128/528/528101.png"
    )
    return embed
