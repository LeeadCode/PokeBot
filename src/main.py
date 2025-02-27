import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import Database
import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Carrega vars do .env
load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents, application_id=os.getenv("DISCORD_ID"))

        # Inicializa o banco de dados
        self.database = Database()

    async def setup_hook(self):
        # Caminho base para os cogs
        cogs_path = "./src/cogs"

        # Percorrer subpastas
        for root, dirs, files in os.walk(cogs_path):
            for file in files:
                # Verificar se o arquivo termina com _cog.py e não é um arquivo __init__.py
                if file.endswith("_cog.py") and file != "__init__.py":
                    # Gerar o caminho relativo do cog
                    cog_path = os.path.relpath(os.path.join(root, file), start=cogs_path)
                    # Remover o _cog.py e substituir os separadores de pasta por "."
                    cog_name = cog_path.replace(os.sep, ".")[:-3]

                    try:
                        # Carregar o cog
                        await self.load_extension(f"cogs.{cog_name}")
                        print(f"Cog {cog_name} carregado com sucesso!")
                    except Exception as e:
                        print(f"Erro ao carregar o cog {cog_name}: {e}")

        # Sincronizar os comandos do bot
        #await self.tree.sync()
        print("Slash commands sincronizados!")

bot = MyBot()

async def main():
    #await bot.setup_hook()
    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:  # Se o loop ja estiver rodando
        loop = asyncio.get_event_loop()
        loop.create_task(main())
