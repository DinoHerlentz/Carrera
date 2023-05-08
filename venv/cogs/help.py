import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from typing import Optional, Set
from main import bot
from requests import options


class HelpDropdown(nextcord.ui.Select):
    def __init__(self, help_command: "MyHelpCommand", options: list[nextcord.SelectOption]):
        super().__init__(placeholder = "Choose a category", min_values = 1, max_values = 1, options = options)
        self._help_command = help_command
    
    async def callback(self, interaction: Interaction):
        embed = (await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(self.values[0])) if self.values[0] != self.options[0].value else await self._help_command.bot_help_embed(self._help_command.get_bot_mapping()))
        await interaction.response.edit_message(embed = embed)


class HelpView(nextcord.ui.View):
    def __init__(self, help_command: "MyHelpCommand", options: list[nextcord.SelectOption], *, timeout: Optional[float] = 120.0):
        super().__init__(timeout = timeout)
        self.add_item(HelpDropdown(help_command, options))
        self._help_command = help_command
    
    async def on_timeout(self) -> None:
        self.clear_items()
        await self._help_command.response.edit(view = self)
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return self._help_command.context.author == interaction.user


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
    
    async def _cog_select_options(self) -> list[nextcord.SelectOption]:
        options: list[nextcord.SelectOption] = []
        options.append(nextcord.SelectOption(label = "Home", emoji = "🏠", description = "Back to the main menu"))

        for cog, command_set in self.get_bot_mapping().items():
            filtered = await self.filter_commands(command_set, sort = True)

            if not filtered:
                continue

            options.append(nextcord.SelectOption(label = cog.qualified_name if cog else "No Category", description = cog.description[:100] if cog and cog.description else None))
        
        return options
    
    async def _help_embed(self, title: str, description: Optional[str] = None, mapping: Optional[str] = None, command_set: Optional[Set[commands.Command]] = None, set_author: bool = False) -> nextcord.Embed:
        embed = nextcord.Embed(title = title)

        if description:
            embed.description = description
        
        if set_author:
            avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            embed.set_author(name = self.context.bot.user.name, icon_url = avatar.url)
        
        if command_set:
            filtered = await self.filter_commands(command_set, sort = True)

            for command in filtered:
                embed.add_field(name = self.get_command_signature(command), value = command.short_doc or "No Description Provided", inline = False)
        
        if mapping:
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort = True)
            
                if not filtered:
                    continue

            name = cog.quailfied_name if cog else "No Category"
            cmd_list = "\u2002".join(f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered)
            value = (f"{cog.description}\n{cmd_list}" if cog and cog.description else cmd_list)
            embed.add_field(name = name, value = value)
        
        return embed
    
    async def bot_help_embed(self, mapping: dict) -> nextcord.Embed:
        return await self._help_embed(title = "Commands (>>)", description = self.context.bot.description, mapping = mapping, set_author = True)
    
    async def send_bot_help(self, mapping: dict):
        embed = await self.bot_help_embed(mapping)
        options = await self._cog_select_options()
        self.response = await self.get_destination().send(embed = embed, view = HelpView(self, options))

    async def send_command_help(self, command: commands.Command):
        embed = await self._help_embed(title = command.qualified_name, description = command.help, command_set = commands.commands if isinstance(command, commands.Group) else None)
        await self.get_destination().send(embed = embed)
    
    async def cog_help_embed(self, cog: commands.Cog) -> nextcord.Embed:
        return await self._help_embed(title = cog.qualified_name, description = cog.description, command_set = cog.get_commands())

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.cog_help_embed(cog)
        await self.get_destination().send(embed = embed)

    senf_group_help = send_command_help


class HelpCog(commands.Cog, name = "Help"):
    def __init__(self, bot):
        self.original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
    
    def cog_unload(self):
        self.bot.help_command = self.original_help_command


def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))