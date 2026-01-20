"""YouTube Data API v3 client wrapper for YouTube Music playlist access."""

import os
import re
import json
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CONFIG_DIR = Path(__file__).parent
TOKEN_FILE = CONFIG_DIR / "token.json"
CLIENT_SECRETS_FILE = CONFIG_DIR / "client_secrets.json"


class YouTubeClient:
    """Client for accessing YouTube Music playlists via YouTube Data API v3."""

    def __init__(self):
        self._service = None

    def _get_credentials(self) -> Credentials:
        """Get or refresh OAuth credentials."""
        creds = None

        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CLIENT_SECRETS_FILE.exists():
                    raise FileNotFoundError(
                        f"OAuth client secrets not found at {CLIENT_SECRETS_FILE}. "
                        "Please download from Google Cloud Console and save as 'client_secrets.json'"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CLIENT_SECRETS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return creds

    @property
    def service(self):
        """Lazy-load the YouTube API service."""
        if self._service is None:
            creds = self._get_credentials()
            self._service = build("youtube", "v3", credentials=creds)
        return self._service

    def get_my_playlists(self, max_results: int = 50) -> list[dict]:
        """Get all playlists from the authenticated user's library.

        Returns:
            List of playlist dictionaries with id, title, description, item_count
        """
        playlists = []
        page_token = None

        while True:
            request = self.service.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=min(max_results, 50),
                pageToken=page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                playlists.append({
                    "id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"].get("description", ""),
                    "item_count": item["contentDetails"]["itemCount"],
                    "thumbnail": item["snippet"]["thumbnails"].get("medium", {}).get("url"),
                })

            page_token = response.get("nextPageToken")
            if not page_token or len(playlists) >= max_results:
                break

        return playlists[:max_results]

    def get_playlist_items(self, playlist_id: str, max_results: int = 200) -> list[dict]:
        """Get all items in a playlist with parsed music metadata.

        Args:
            playlist_id: The YouTube playlist ID
            max_results: Maximum number of items to return

        Returns:
            List of track dictionaries with video_id, title, artist, song, channel
        """
        items = []
        page_token = None

        while True:
            request = self.service.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(max_results, 50),
                pageToken=page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]
                title = snippet.get("title", "")
                parsed = self._parse_music_title(title)

                items.append({
                    "video_id": snippet["resourceId"]["videoId"],
                    "title": title,
                    "artist": parsed["artist"],
                    "song": parsed["song"],
                    "channel": snippet.get("videoOwnerChannelTitle", ""),
                    "position": snippet.get("position", 0),
                    "thumbnail": snippet["thumbnails"].get("medium", {}).get("url"),
                })

            page_token = response.get("nextPageToken")
            if not page_token or len(items) >= max_results:
                break

        return items[:max_results]

    def get_video_details(self, video_ids: list[str]) -> list[dict]:
        """Get detailed information for videos including duration.

        Args:
            video_ids: List of YouTube video IDs (max 50 per call)

        Returns:
            List of video detail dictionaries
        """
        if not video_ids:
            return []

        # API allows max 50 IDs per request
        video_ids = video_ids[:50]

        request = self.service.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids),
        )
        response = request.execute()

        videos = []
        for item in response.get("items", []):
            snippet = item["snippet"]
            content = item["contentDetails"]
            stats = item.get("statistics", {})

            videos.append({
                "video_id": item["id"],
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "duration": content["duration"],  # ISO 8601 duration
                "duration_seconds": self._parse_duration(content["duration"]),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "category_id": snippet.get("categoryId"),
                "tags": snippet.get("tags", []),
            })

        return videos

    def search_music(self, query: str, max_results: int = 10) -> list[dict]:
        """Search for music videos on YouTube.

        Args:
            query: Search query (e.g., "artist name song title")
            max_results: Maximum results to return

        Returns:
            List of search result dictionaries
        """
        request = self.service.search().list(
            part="snippet",
            q=query,
            type="video",
            videoCategoryId="10",  # Music category
            maxResults=min(max_results, 25),
        )
        response = request.execute()

        results = []
        for item in response.get("items", []):
            snippet = item["snippet"]
            parsed = self._parse_music_title(snippet["title"])

            results.append({
                "video_id": item["id"]["videoId"],
                "title": snippet["title"],
                "artist": parsed["artist"],
                "song": parsed["song"],
                "channel": snippet["channelTitle"],
                "thumbnail": snippet["thumbnails"].get("medium", {}).get("url"),
            })

        return results

    @staticmethod
    def _parse_music_title(title: str) -> dict:
        """Parse 'Artist - Song Title' format common in music videos.

        Handles various formats:
        - "Artist - Song"
        - "Artist | Song"
        - "Artist - Song (Official Video)"
        - "Artist - Song [Lyrics]"
        """
        # Clean up common suffixes
        clean_title = re.sub(
            r'\s*[\(\[](?:Official\s*)?(?:Music\s*)?(?:Video|Audio|Lyrics?|HD|4K|Live|Remix|Cover)[\)\]]',
            '',
            title,
            flags=re.IGNORECASE
        )

        patterns = [
            r'^(.+?)\s*[-–—:]\s*(.+?)$',  # Artist - Song or Artist: Song
            r'^(.+?)\s*[|]\s*(.+?)$',      # Artist | Song
        ]

        for pattern in patterns:
            match = re.match(pattern, clean_title.strip())
            if match:
                artist = match.group(1).strip()
                song = match.group(2).strip()
                # Skip if artist looks like a label/channel name
                if artist and song and len(artist) < 100 and len(song) < 200:
                    return {"artist": artist, "song": song}

        return {"artist": "Unknown", "song": title.strip()}

    @staticmethod
    def _parse_duration(iso_duration: str) -> int:
        """Convert ISO 8601 duration to seconds.

        Example: PT4M30S -> 270 seconds
        """
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        return hours * 3600 + minutes * 60 + seconds


# Singleton instance
_client: Optional[YouTubeClient] = None


def get_client() -> YouTubeClient:
    """Get or create the singleton YouTube client."""
    global _client
    if _client is None:
        _client = YouTubeClient()
    return _client
