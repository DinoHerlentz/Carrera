import nextcord
import datetime
from nextcord import Interaction
from nextcord.ext import commands
from main import bot


class Embed(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Embed Maker")

        self.emTitle = nextcord.ui.TextInput(label = "Embed", min_length = 2, max_length = 124, required = True, placeholder = "Enter Embed Title")
        self.add_item(self.emTitle)

        self.emDesc = nextcord.ui.TextInput(label = "Description", min_length = 5, max_length = 4000, required = True, placeholder = "Enter Embed Description", style = nextcord.TextInputStyle.paragraph)
        self.add_item(self.emDesc)
    
    async def callback(self, interaction: Interaction) -> None:
        title = self.emTitle.value
        desc = self.emDesc.value

        em = nextcord.Embed(title = title, description = desc)
        em.timestamp = datetime.datetime.utcnow()

        return await interaction.response.send_message(embed = em)


class Modals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @nextcord.slash_command(name = "embed", description = "Create an embed")
    async def embed(self, interaction: Interaction):
        await interaction.response.send_modal(Embed())


def setup(bot):
    bot.add_cog(Modals(bot))
