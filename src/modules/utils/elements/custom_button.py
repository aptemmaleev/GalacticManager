import discord

from discord.ui import Button
from logger import log_debug

class CustomButton(Button):
    def __init__(self, style: discord.ButtonStyle, label: str = None, emoji: str = None):
        self.callback_function = None
        super().__init__(style=style, label=label, emoji=emoji)
    
    def set_callback(self, function):
        self.callback_function = function

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if (not self.disabled):
            self.disabled = 1
            if (self.callback_function != None):
                await self.callback_function()
    
    def reset(self):
        self.disabled = 0