import discord

from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, ShechedEvent):
        guild = self.bot.get_guild(1302844590063095888) # Hardcode
        creatorUser = await guild.fetch_member(ShechedEvent.creator_id)

        if 1302848813509115936 in [role.id for role in creatorUser.roles]:
            forumChannel = self.bot.get_channel(1302847972748300440) # Hardcode
        elif 1302848869725638718 in [role.id for role in creatorUser.roles]:
            forumChannel = self.bot.get_channel(1303071016544763954) # Hardcode

        embed = discord.Embed(description='Additional Info')
        embed.add_field(name="Event location", value=ShechedEvent.location)
        embed.add_field(
            name="Event Invite Link", value=f"https://discord.gg/pQA9BJz6XP/{ShechedEvent.id}" # Hardcode
        )
        embed.add_field(
            name="Event Date", value=f"<t:{round(ShechedEvent.start_time.timestamp())}:R> - <t:{round(ShechedEvent.end_time.timestamp())}:R>"}"
        )
        embed.add_field(name="Event Members", value=f"Creator: {creatorUser.mention}")

        thread = await forumChannel.create_thread(
            name=ShechedEvent.name,
            content=ShechedEvent.description,
            embed=embed,
        )

        await thread.add_user(creatorUser)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        await thread.send("")


def setup(bot):

    bot.add_cog(events(bot))
