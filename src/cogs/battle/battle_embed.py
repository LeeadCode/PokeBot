import discord


def battle_embed(info) -> discord.Embed:
    embed = discord.Embed(color=0x0099FF)

    # Adicionando autor (nome + HP do Pokémon defensor)
    embed.set_author(
        name=f'{info.defend_player.pokemon.battle_name} ❤️: {info.defend_player.pokemon.base.hp}',
        icon_url=info.defend_player.user.avatar.url if info.defend_player.user and info.defend_player.user.avatar else '',
    )

    # Miniatura do Pokémon defensor
    embed.set_thumbnail(url=info.defend_player.pokemon.sprites['other']['showdown']['front_default'])

    # Adicionando informação do ataque
    embed.add_field(name=info.move_type, value=info.info_text, inline=False)

    # Imagem do Pokémon atacante
    embed.set_image(url=info.attack_player.pokemon.sprites['other']['showdown']['back_default'])

    # Rodapé (nome + HP do Pokémon atacante)
    embed.set_footer(
        text=f'{info.attack_player.pokemon.battle_name} ❤️: {info.attack_player.pokemon.base.hp}',
        icon_url=info.attack_player.user.avatar.url if info.attack_player.user and info.attack_player.user.avatar else '',
    )

    # Adicionando mudanças de status (se houver)
    for stat in info.stats_change:
        embed.add_field(name='\u200b', value=stat, inline=False)

    return embed
