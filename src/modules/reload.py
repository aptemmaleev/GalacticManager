from discord.ext import commands

from logger import log_error, log_info, log_debug, log_warning
from config import get_color, config

class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log_info("Reload Module successfully loaded!")

    @commands.command()
    @commands.is_owner() 
    async def reload(self, ctx, *args):
        if (len(args) == 0):
            extensions = list()
            await self.bot.get_cog('MenuCog').close_all_menu()
            for extension in self.bot.extensions:
                if not (extension == 'modules.reload'): 
                    extensions.append(extension)
            for extension in extensions:
                await self.bot.unload_extension(extension)
                await self.bot.load_extension(extension)
            log_warning('All extensions are reloaded!')
            await self.bot.send_simple_embed(ctx.channel, title='Команда выполнена', description='Все модули были перезагружены!', color='success')
        else:
            reload_extensions = list()
            for module in args:
                if not (module == 'reload'): 
                    reload_extensions.append(f'modules.{module}')

            extensions = list()
            for extension in self.bot.extensions:
                if not (extension == 'modules.reload'): 
                    extensions.append(extension)
            
            for extension in extensions:
                if extension in reload_extensions:
                    await self.bot.unload_extension(extension)
                    await self.bot.load_extension(extension)
                    await ctx.send(f'{extension} перезагружен!')

    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        await self.bot.send_simple_embed(ctx.channel, title='Ping', description=f'pong in {round(self.bot.latency * 1000)} ms!', color='success', delete_after= 5)

    @ping.error
    async def ping_error(self, ctx, error):
        if (str(ctx.channel).startswith("Direct Message with")):
            return
        await self.bot.send_simple_embed(ctx.channel, title='Error', description=f'{error}', color='error', delete_after= 5)

async def setup(bot):
    await bot.add_cog(ReloadCog(bot))