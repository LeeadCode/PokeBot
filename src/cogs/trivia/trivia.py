import asyncio
import discord
from discord.ext import commands
from enum import Enum
from typing import List, Optional
from emmiter import emitter

class TriviaEvent(Enum):
    RUN = "RUN"
    START = "START"
    REPLY = "REPLY"
    END = "END"
    CORRECT_ANSWER = "CORRECT_ANSWER"

class TriviaPlayer:
    def __init__(self, user: discord.Usern, wins: int):
        self.user = user
        self.wins = 0

class Trivia(emitter):
    def __init__(self, bot: commands.Bot, collector_filter):
        self.bot = bot
        self.players: List[TriviaPlayer] = []
        self.correct_answer: Optional[discord.Message] = None
        self.section_number = 1
        self.collector_filter = collector_filter
        super().__init__()

    async def start(self, interaction: discord.Interaction):
        """Inicia a Trivia."""
        await self.emit(TriviaEvent.START)
        await self.run(interaction)

    async def run(self, interaction: discord.Interaction):
        """Executa uma rodada da Trivia."""
        await self.emit(TriviaEvent.RUN)

        # Enviar pergunta
        await self.emit(TriviaEvent.REPLY)

        try:
            response = await self.bot.wait_for(
                "message",
                timeout=15,
                check=self.collector_filter
            )
        except asyncio.TimeoutError:
            response = None

        if response:
            await self.emit(TriviaEvent.CORRECT_ANSWER, response)

            # Adiciona ou atualiza o jogador
            player = next((p for p in self.players if p.user.id == response.author.id), None)
            if player:
                player.wins += 1
                print(player.wins)
            else:
                self.players.append(TriviaPlayer(response.author, 1))

            self.section_number += 1
            await asyncio.sleep(5)
            await self.run(interaction)
        else:
            self.players.sort(key=lambda p: p.wins, reverse=True)
            await self.emit(TriviaEvent.END)
