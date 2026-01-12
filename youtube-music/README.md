# YouTube Music MCP

An MCP server that connects Claude Code to your YouTube Music playlists for analysis and personalized music recommendations.

## Features

- **List Playlists** - View all your YouTube Music playlists
- **Analyze Playlist** - Get insights on your music taste (top artists, patterns)
- **Get Recommendations** - Receive personalized song suggestions based on your playlists
- **Search Music** - Search YouTube Music directly

## Prerequisites

- Python 3.10+
- Google Cloud Project with YouTube Data API v3 enabled
- OAuth 2.0 credentials

## Installation

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/YOUR_USERNAME/awesome-mcps.git
cd awesome-mcps/youtube-music
pip install -r requirements.txt
```

### 2. Set Up Google Cloud OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **YouTube Data API v3**:
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create OAuth credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Configure consent screen if prompted (External, add your email as test user)
   - Select **Desktop app** as application type
   - Download the JSON file
5. Save the file as `client_secrets.json` in this directory

### 3. Add to Claude Code

```bash
# Add the MCP server
claude mcp add youtube-music -- python /full/path/to/awesome-mcps/youtube-music/server.py

# Verify it's connected
claude mcp list
```

### 4. (Optional) Install the Skill

Copy the skill for better Claude integration:

```bash
mkdir -p ~/.claude/skills/music-recommender
cp skill/SKILL.md ~/.claude/skills/music-recommender/
```

## Usage

After installation, restart Claude Code and try:

```
Show my YouTube Music playlists
```

```
Analyze my "Favorites" playlist
```

```
Recommend songs based on my workout playlist
```

The first time you use it, a browser window will open asking you to authorize YouTube access.

## Available Tools

| Tool | Description |
|------|-------------|
| `get_my_playlists` | List all your playlists |
| `get_playlist_items` | Get songs in a specific playlist |
| `get_video_details` | Get video metadata (duration, views) |
| `search_music` | Search YouTube Music |
| `analyze_playlist` | Analyze playlist patterns and taste |

## Troubleshooting

### "MCP server not connected"
- Make sure you added the server with `claude mcp add`
- Restart Claude Code after adding
- Check status with `claude mcp list`

### "client_secrets.json not found"
- Download OAuth credentials from Google Cloud Console
- Save as `client_secrets.json` in this directory

### "Access denied" on first auth
- Make sure you added your email as a test user in OAuth consent screen
- Or publish your OAuth app (requires verification for public use)

## API Quota

YouTube Data API has a daily quota of 10,000 units:
- Read operations: 1 unit
- Search operations: 100 units

For personal use, this is usually sufficient.

## License

MIT
