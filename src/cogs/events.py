import discord, json

from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass
    
    async def create_thread(self, event):
        print("create_thread called")
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
    async def on_scheduled_event_delete(self, event):
        with open('data/events.json', 'r') as f:
            data = json.load(f)
        event_id = str(event.id)
        if event_id in data['eventsDict']:
            thread_id = data['eventsDict'][event_id]
            thread = self.bot.get_channel(thread_id)
            await thread.delete()
            del data['eventsDict'][event_id]
            with open('data/events.json', 'w') as f:
                json.dump(data, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready, running on_ready event listener")
        guild = self.bot.get_guild(1302844590063095888)
        print(f"Retrieved guild: {guild.name} (ID: {guild.id})")
        events = await guild.fetch_scheduled_events()
        print(f"Retrieved {len(events)} scheduled events")

        channels = [guild.get_channel(1302847972748300440), guild.get_channel(1303071016544763954)]
        threads = [thread for channel in channels for thread in channel.threads]
    
        with open('data/events.json', 'r') as f:
            try:
                data = json.load(f)
                print("Loaded events.json file successfully")
            except:
                data = {'eventsDict': {}}
                print("Failed to load events.json file, creating new dictionary")
    
        # Update events dictionary to reflect current state
        data['eventsDict'] = {}
        for event in events:
            thread_id = next((thread.id for thread in threads if thread.name == event.name), None)
            if thread_id:
                data['eventsDict'][str(event.id)] = thread_id
    
        # Recreate deleted threads for scheduled events
        for event in events:
            thread_id = data['eventsDict'].get(str(event.id))
            if thread_id and not guild.get_thread(thread_id):
                print(f"Thread for event {event.id} no longer exists, deleting event")
                try:
                    await event.delete()
                    del data['eventsDict'][str(event.id)]
                    print(f"Deleted event {event.id} and removed from events.json")
                except Exception as e:
                    print(f"Failed to delete event {event.id}: {str(e)}")
            elif not thread_id:
                print(f"No thread found for event {event.id}, creating new thread")
                try:
                    thread = await self.create_thread(event)
                    data['eventsDict'][str(event.id)] = thread.id
                    print(f"Created new thread for event {event.id} and added to events.json")
                except Exception as e:
                    print(f"Failed to create thread for event {event.id}: {str(e)}")
    
        # Clean up threads in channels
        channels = [guild.get_channel(1302847972748300440), guild.get_channel(1303071016544763954)]
        for channel in channels:
            print(f"Cleaning up threads in channel {channel.name} (ID: {channel.id})")
            for thread in channel.threads:
                if thread.id not in data['eventsDict'].values():
                    print(f"Deleting thread {thread.id} (not associated with an event)")
                    await thread.delete()
                else:
                    print(f"Skipping thread {thread.id} (associated with an event)")
    
        # Save updated events dictionary to file
        with open('data/events.json', 'w') as f:
            json.dump(data, f)
        print("Saved updated events.json file")

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        # delete thread from events.json and its event
        with open('data/events.json', 'r') as f:
            data = json.load(f)
        event_id_to_delete = next((event_id for event_id, thread_id in data['eventsDict'].items() if thread_id == thread.id), None)
        if event_id_to_delete:
            del data['eventsDict'][event_id_to_delete]
            with open('data/events.json', 'w') as f:
                json.dump(data, f)
            try:
                event = await thread.guild.fetch_scheduled_event(int(event_id_to_delete))
                await event.delete()
            except Exception:
                pass

def setup(bot):
    bot.add_cog(events(bot))