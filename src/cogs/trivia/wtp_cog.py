import discord
from discord import app_commands
from discord.ext import commands
from .trivia import Trivia, TriviaEvent
from utils.create_black_silhouette import create_black_silhouette_from_url
from .wtp_embed import wtp_embed
from .wtp_successful_embed import wtp_successful_embed
from .wtp_result_embed import wtp_result_embed

class WTP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="wtp", description="Who's That Pokémon? :)")
    async def wtp(self, interaction: discord.Interaction):
        random_pokemon = None
        silhouette_file = None

        # Setup Run Event
        async def on_run():
            # Escolher Pokémon aleatório
            nonlocal random_pokemon
            random_pokemon = self.bot.database.get_random()
            print(random_pokemon["name"]["english"])

        # Setup Reply Event
        async def on_reply():
            # Criar silhouette do Pokémon
            nonlocal silhouette_file 
            silhouette_file = await create_black_silhouette_from_url(
            random_pokemon["sprites"]["other"]["oficialArtWork"]["default"]
            )

            file = discord.File(silhouette_file, filename="silhouette.png")
            embed = wtp_embed()

            if not interaction.response.is_done():
                await interaction.response.send_message(embed=embed, file=file)
            else:
                await interaction.followup.send(embed=embed, file=file)

        # Setup Correct Answer Event
        async def on_correct_answer(response: discord.Message):
            embed = wtp_successful_embed(response.author, random_pokemon)
            await interaction.followup.send(embed=embed)

        # Setup End Event
        async def on_end():
            embed = wtp_result_embed(trivia.players, trivia.section_number)
            await interaction.followup.send(embed=embed)

        # Criar instância do Trivia
        def check_answer(message: discord.Message):
            return message.content.lower() == random_pokemon["name"]["english"].lower()

        trivia = Trivia(self.bot, check_answer)
        trivia.on(TriviaEvent.RUN, on_run)
        trivia.on(TriviaEvent.REPLY, on_reply)
        trivia.on(TriviaEvent.CORRECT_ANSWER, on_correct_answer)
        trivia.on(TriviaEvent.END, on_end)

        # Iniciar Trivia
        await trivia.start(interaction)

async def setup(bot):
    await bot.add_cog(WTP(bot))
