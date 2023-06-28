import discord
from discord.ext import commands
from json import load
from extensions.error_handler import Error
ConfigRead = open('config.json')
ConfigLoad = load(ConfigRead)
class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Pomoc', color=discord.Color.from_rgb(153, 0, 0))
        for cog, commands in mapping.items():
            if cog:
                name = cog.qualified_name
                filtered = await self.filter_commands(commands, sort=True)
                if filtered:
                    value = ',\u2002'.join(c.name for c in filtered)
                    if cog.description:
                        value = f'{cog.description}\n{value}'
                    embed.add_field(name=name, value=value, inline=False)
                    embed.set_footer(text=f"Aby wyświetlić sposób użycia {ConfigLoad['prefix']}help <polecenie>.")

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f'Pomoc dla kategorii {cog.qualified_name}', description=cog.description, color=discord.Color.from_rgb(153, 0, 0))
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if filtered:
            value = '\u2002'.join(c.name for c in filtered)
            embed.add_field(name='Polecenia', value=value, inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        try:
            channel = self.get_destination()
            embed = discord.Embed(title=f'Pomoc dla polecenia {command.qualified_name}', description=command.help, color=discord.Color.from_rgb(153, 0, 0))
            if command.aliases:
                embed.add_field(name='Aliasy', value=', '.join(command.aliases), inline=False)
            embed.add_field(name='Używanie', value=f"{ConfigLoad['prefix']}{command} {command.signature}", inline=False)
            await channel.send(embed=embed)
        except AttributeError as e:
            await channel.send(f"Polecenie **{command.qualified_name}** nie istnieje.")
            Error(e)
        except Exception as e:
            Error(e)

    def command_not_found(self, string: str, /) -> str:
        return f'Polecenie "{string}" nie istnieje.'