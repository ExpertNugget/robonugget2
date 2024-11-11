import discord, json

from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass
    
    async def create_thread(self, event):
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

        try:
            with open('data/events.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'eventsDict': {}}
        except json.JSONDecodeError:
            data = {'eventsDict': {}}

        data['eventsDict'][event.id] = thread.id

        with open('data/events.json', 'w') as f:
            json.dump(data, f)
        return thread

       
    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event):
        await self.create_thread(event)
        


        

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(1302844590063095888)
        events = guild.scheduled_events
        event_ids = []
        for event in events:
            event_ids.append(event.id)
        unique_event_ids = []
        dupe_event_ids = []
        for event_id in event_ids:
            if event_id not in unique_event_ids:
                unique_event_ids.append(event_id)
            else:
                dupe_event_ids.append(event_id)
        with open('data/events.json', 'r') as f:
            try:
                data = json.load(f)
            except:
                data = {'eventsDict': {}}
        
        for event_id in dupe_event_ids:
            print(f'event ID: {data['eventsDict'][str(event_id)]}') 
            try:
                thread_id = data['eventsDict'][str(event_id)]
                guild = self.bot.get_guild(1302844590063095888)
                thread = guild.get_channel(thread_id)
                await thread.delete()
                del data['eventsDict'][str(event_id)]
            except:
                del data['eventsDict'][str(event_id)]

        for event_id in unique_event_ids:              
            try:
                thread_id = data['eventsDict'][str(event_id)]
                guild = self.bot.get_guild(1302844590063095888)
                thread = guild.get_thread(thread_id)
            except:
                event = await guild.fetch_scheduled_event(event_id)
                thread = await self.create_thread(event)
                data['eventsDict'][str(event_id)] = thread.id

        guild = self.bot.get_guild(1302844590063095888)
        channel = guild.get_channel(1302847972748300440)
        channel2 = guild.get_channel(1303071016544763954)
        for thread in channel.threads:
            if thread.id not in data['eventsDict'].values():
                await thread.delete()
        for thread in channel2.threads:
            if thread.id not in data['eventsDict'].values():
                await thread.delete()

        with open('data/events.json', 'w') as f:
            json.dump(data, f)

            
                
        
        
            
        




        

        

        
            


            





    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        pass

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        pass

def setup(bot):
    bot.add_cog(events(bot))
