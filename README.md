# destroyux

Discord raid bot - nuke, spam, chaos operations

**Credit: m3oza**

## Features

- `/nuke` - Delete all channels/roles, customize server name
- `/spam` - High-speed message spam across channels (customizable)
- `/raid` - Full nuke + spam sequence (5k+ ping capable)
- Fast batched async operations
- Customizable ping messages, channel names, server names
- Watching status showing .gg/m3oza
- Slash command support

## Setup Local

1. Create Discord bot at [developer.discord.com](https://discord.com/developers/applications)
   - Enable Message Content Intent
   - Copy bot token

2. Clone/download this repo

3. Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your values:
   ```
   BOT_TOKEN=your_bot_token_here
   OWNER_ID=your_discord_user_id_here
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run locally:
   ```bash
   python main.py
   ```

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [Railway.app](https://railway.app)
3. Create new project → GitHub Repo
4. Select this repository
5. Add environment variables in Railway dashboard:
   - `BOT_TOKEN` = your bot token
   - `OWNER_ID` = your Discord ID
6. Railway auto-deploys from main branch

## Commands

### /nuke
Delete all channels and roles, optionally customize names
```
/nuke [channels_name] [server_name]
```

### /spam
Spam messages across all channels
```
/spam [count] [message] [ping_everyone]
```

### /raid
Full nuke + spam sequence
```
/raid [ping_count] [spam_count] [server_name] [chaos]
```

## Requirements

- Python 3.9+
- discord.py 2.4.0+
- Railway account (for deployment)

**Status**: servers burn | .gg/m3oza

---
*Credit: m3oza*
