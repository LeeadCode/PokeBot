from discord.ext import commands
from comandos import BatalhaPokemon, Conquistas, Pokedex
import json
from controllers.constantes import constantes

cogs = [BatalhaPokemon, Conquistas, Pokedex]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')

    async def on_ready(self):
        constantes.ASSINATURA_POKEBOT()


bot = Bot()

for i in range(len(cogs)):
    cogs[i].iniciar(bot)

with open("secrets.json", "r") as configuracao:
    data = json.load(configuracao)
    bot.run(data["keyDiscord"])
