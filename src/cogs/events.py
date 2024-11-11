import discord

from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event):
        guild = self.bot.get_guild(1302844590063095888)
        creator = await guild.fetch_member(event.creator_id)

        if 1302848813509115936 in [role.id for role in creator.roles]:
            channel = self.bot.get_channel(1302847972748300440)
        elif 1302848869725638718 in [role.id for role in creator.roles]:
            channel = self.bot.get_channel(1303071016544763954)

        embed = discord.Embed(description='Additional Info')
        embed.add_field(name='Location', value=event.location)
        embed.add_field(name='Invite Link', value=f'https://discord.gg/pQA9BJz6XP/{event.id}')
        embed.add_field(name='Date', value=f'<t:{int(event.start_time.timestamp())}:R> - <t:{int(event.end_time.timestamp())}:R>')
        embed.add_field(name='Event Members', value=f'Creator: {creator.mention}')

        thread = await channel.create_thread(
            name=event.name,
            content=event.description,
            embed=embed,
        )

        await thread.add_user(creator)
        




    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        pass

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        pass

def setup(bot):
    bot.add_cog(events(bot))
