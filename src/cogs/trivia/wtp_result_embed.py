import discord
from typing import List

class TriviaPlayer:
    def __init__(self, user: discord.User, wins: int):
        self.user = user
        self.wins = wins

def wtp_result_embed(players: List[TriviaPlayer], trivia_runs: int) -> discord.Embed:
    embed = discord.Embed(
        color=0x0099FF,
        title=f"Fim! Rodadas: {trivia_runs}",
    )
    embed.set_image(url="attachment://silhouette.png")
    embed.set_footer(
        text="PokeBot 2024",
        icon_url="https://cdn-icons-png.flaticon.com/128/528/528101.png",
    )

    if players:
        winner = players[0]
        embed.title = f"O Vencedor é {winner.user.display_name} com {winner.wins} Acertos!"
        embed.set_thumbnail(url="https://c.tenor.com/74l5y1hUdtwAAAAj/pokemon.gif")

        if len(players) > 1:
            for player in players[1:]:
                embed.add_field(
                    name=player.user.display_name,
                    value=f"Acertos: {player.wins}",
                    inline=True,
                )
    else:
        embed.title = "Nenhum Jogador Acertou :("
        embed.set_thumbnail(url="https://i.pinimg.com/originals/80/e1/8d/80e18df0ed0ad872ac1a003d543d9613.gif")

    return embed
