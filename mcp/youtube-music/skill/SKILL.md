---
name: music-recommender
description: Use when user wants music recommendations based on their YouTube Music playlists, wants to analyze their music taste, asks about similar artists or songs, or wants to discover new music matching their style
---

# Music Playlist Analyzer & Recommender

Analyze YouTube Music playlists and provide personalized music recommendations.

## Available Tools

Use these MCP tools from the `youtube-music` server:

| Tool | Purpose |
|------|---------|
| `youtube-music:get_my_playlists` | List user's playlists |
| `youtube-music:get_playlist_items` | Get songs in a playlist |
| `youtube-music:analyze_playlist` | Get taste analysis (top artists, patterns) |
| `youtube-music:search_music` | Search for music on YouTube |

## Process

### 1. Fetch Playlists
```
Use youtube-music:get_my_playlists to show available playlists
```

### 2. Analyze Selected Playlist
```
Use youtube-music:analyze_playlist with the playlist_id
```

### 3. Identify Patterns
From the analysis, identify:
- **Dominant artists**: Who appears most frequently
- **Music style**: Infer genres from artist names
- **Era/decade**: Modern, classic, mixed
- **Energy level**: Based on artist styles
- **Language/region**: If applicable

### 4. Generate Recommendations

Use your music knowledge to recommend:
- Similar artists the user might not know
- Specific songs that match the playlist vibe
- Adjacent genres to explore

For each recommendation explain **why** it matches their taste.

### 5. Optionally Search
```
Use youtube-music:search_music to find specific tracks and provide links
```

## Output Format

Structure recommendations as:

```
## Your Music Profile
- Primary genres: [identified genres]
- Top artists: [from analysis]
- Vibe: [energy/mood description]

## Recommended Artists
1. **[Artist Name]** - [Why they match]
   - Try: "[Song 1]", "[Song 2]"

2. **[Artist Name]** - [Why they match]
   - Try: "[Song 1]", "[Song 2]"

## Discovery Suggestions
- [Genre/style] exploration: [specific recommendations]
- Deep cuts from artists you like: [specific songs]
```

## Tips

- Ask which playlist to analyze if user has multiple
- Consider playlist name for context (workout, chill, party, etc.)
- Mix well-known and lesser-known recommendations
- Include YouTube Music search links when helpful
