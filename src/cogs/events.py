import discord
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, ShechedEvent):
        guild = self.bot.get_guild(1302844590063095888)
        creatorUser = await guild.fetch_member(ShechedEvent.creator_id)

        if 1302848813509115936 in [role.id for role in creatorUser.roles]:
            forumChannel = self.bot.get_channel(1302847972748300440)
        elif 1302848869725638718 in [role.id for role in creatorUser.roles]:
            forumChannel = self.bot.get_channel(1303071016544763954)

        emebed = discord.Embed()
        emebed.add_field(name="Event location", value=ShechedEvent.location)
        emebed.add_field(
            name="Event Link", value=f"https://discord.com/events/{ShechedEvent.id}"
        )

        thread = await forumChannel.create_thread(
            name=ShechedEvent.name,
            content=ShechedEvent.description
            + f"\nEvent location: {ShechedEvent.location}\n[Event Link](https://discord.com/events/{ShechedEvent.id})",
            emebed=emebed,
        )

        await thread.add_user(creatorUser)

        await thread.send()


def setup(bot):

    bot.add_cog(events(bot))
