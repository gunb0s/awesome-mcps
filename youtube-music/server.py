#!/usr/bin/env python3
"""MCP Server for YouTube Music playlist analysis and recommendations."""

import asyncio
import json
from collections import Counter
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from youtube_client import get_client, YouTubeClient

# Initialize MCP server
server = Server("youtube-music")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_my_playlists",
            description="Get all playlists from your YouTube Music library. Returns playlist ID, title, description, and item count.",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of playlists to return (default: 50)",
                        "default": 50,
                    }
                },
            },
        ),
        Tool(
            name="get_playlist_items",
            description="Get all songs in a specific playlist with parsed artist and song metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {
                        "type": "string",
                        "description": "The YouTube playlist ID",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of items to return (default: 200)",
                        "default": 200,
                    },
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="get_video_details",
            description="Get detailed information for videos including duration, view count, and tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of YouTube video IDs (max 50)",
                    }
                },
                "required": ["video_ids"],
            },
        ),
        Tool(
            name="search_music",
            description="Search for music videos on YouTube Music.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'artist name song title')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 10)",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="analyze_playlist",
            description="Analyze a playlist to extract music taste patterns including top artists, genres inferred from artists, and playlist statistics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {
                        "type": "string",
                        "description": "The YouTube playlist ID to analyze",
                    }
                },
                "required": ["playlist_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    client = get_client()

    try:
        if name == "get_my_playlists":
            max_results = arguments.get("max_results", 50)
            playlists = client.get_my_playlists(max_results=max_results)
            return [TextContent(type="text", text=json.dumps(playlists, indent=2))]

        elif name == "get_playlist_items":
            playlist_id = arguments["playlist_id"]
            max_results = arguments.get("max_results", 200)
            items = client.get_playlist_items(playlist_id, max_results=max_results)
            return [TextContent(type="text", text=json.dumps(items, indent=2))]

        elif name == "get_video_details":
            video_ids = arguments["video_ids"]
            details = client.get_video_details(video_ids)
            return [TextContent(type="text", text=json.dumps(details, indent=2))]

        elif name == "search_music":
            query = arguments["query"]
            max_results = arguments.get("max_results", 10)
            results = client.search_music(query, max_results=max_results)
            return [TextContent(type="text", text=json.dumps(results, indent=2))]

        elif name == "analyze_playlist":
            playlist_id = arguments["playlist_id"]
            analysis = await analyze_playlist_patterns(client, playlist_id)
            return [TextContent(type="text", text=json.dumps(analysis, indent=2))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except FileNotFoundError as e:
        return [TextContent(
            type="text",
            text=f"Setup required: {str(e)}\n\nPlease follow these steps:\n"
                 "1. Go to Google Cloud Console\n"
                 "2. Create a project and enable YouTube Data API v3\n"
                 "3. Create OAuth 2.0 credentials (Desktop app)\n"
                 "4. Download and save as 'client_secrets.json' in the server directory"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def analyze_playlist_patterns(client: YouTubeClient, playlist_id: str) -> dict:
    """Analyze a playlist to extract music taste patterns.

    Returns:
        Dictionary with artist frequencies, inferred styles, and statistics
    """
    items = client.get_playlist_items(playlist_id, max_results=500)

    if not items:
        return {"error": "Playlist is empty or not found"}

    # Count artists
    artist_counter = Counter()
    channel_counter = Counter()
    songs_by_artist: dict[str, list[str]] = {}

    for item in items:
        artist = item["artist"]
        if artist != "Unknown":
            artist_counter[artist] += 1
            if artist not in songs_by_artist:
                songs_by_artist[artist] = []
            songs_by_artist[artist].append(item["song"])

        channel = item["channel"]
        if channel:
            channel_counter[channel] += 1

    # Get video details for duration analysis (sample first 50)
    video_ids = [item["video_id"] for item in items[:50]]
    video_details = client.get_video_details(video_ids) if video_ids else []

    total_duration = sum(v.get("duration_seconds", 0) for v in video_details)
    avg_duration = total_duration / len(video_details) if video_details else 0

    # Build analysis result
    top_artists = artist_counter.most_common(15)
    top_channels = channel_counter.most_common(10)

    return {
        "total_tracks": len(items),
        "unique_artists": len(artist_counter),
        "top_artists": [
            {
                "artist": artist,
                "track_count": count,
                "sample_songs": songs_by_artist.get(artist, [])[:3],
            }
            for artist, count in top_artists
        ],
        "top_channels": [
            {"channel": channel, "track_count": count}
            for channel, count in top_channels
        ],
        "duration_stats": {
            "sample_size": len(video_details),
            "total_minutes": round(total_duration / 60, 1),
            "avg_track_minutes": round(avg_duration / 60, 2),
        },
        "sample_tracks": [
            {"artist": item["artist"], "song": item["song"]}
            for item in items[:10]
        ],
    }


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
