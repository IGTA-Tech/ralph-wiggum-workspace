#!/usr/bin/env python3
"""
YouTube Transcript Fetcher
Searches YouTube and extracts transcripts for RAG processing.

Usage:
    python fetch_transcripts.py --search "Ralph Wiggum AI coding"
    python fetch_transcripts.py --channel "UCxxxxxx" --max-videos 10
    python fetch_transcripts.py --video "dQw4w9WgXcQ"
    python fetch_transcripts.py --creator "Ryan Carson"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    from googleapiclient.discovery import build
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
OUTPUT_DIR = Path(__file__).parent / "transcripts"


def get_youtube_client():
    """Initialize YouTube API client."""
    if not API_KEY:
        print("ERROR: YOUTUBE_API_KEY not found in environment.")
        print("Create a .env file with your API key (see .env.example)")
        sys.exit(1)
    return build("youtube", "v3", developerKey=API_KEY)


def search_videos(query: str, max_results: int = 10) -> list:
    """Search YouTube for videos matching query."""
    youtube = get_youtube_client()

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
        order="relevance",
        videoCaption="closedCaption"  # Only videos with captions
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        videos.append({
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "description": item["snippet"]["description"],
            "published": item["snippet"]["publishedAt"],
            "url": f"https://youtube.com/watch?v={item['id']['videoId']}"
        })
    return videos


def search_channel_videos(channel_id: str, max_results: int = 10) -> list:
    """Get recent videos from a specific channel."""
    youtube = get_youtube_client()

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        type="video",
        maxResults=max_results,
        order="date"
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        videos.append({
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "description": item["snippet"]["description"],
            "published": item["snippet"]["publishedAt"],
            "url": f"https://youtube.com/watch?v={item['id']['videoId']}"
        })
    return videos


def search_by_creator_name(creator_name: str, max_results: int = 10) -> list:
    """Search for videos by creator name."""
    # Search for the creator's content
    query = f"{creator_name}"
    return search_videos(query, max_results)


def get_transcript(video_id: str) -> str | None:
    """Fetch transcript for a video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all text segments
        full_text = " ".join([entry["text"] for entry in transcript_list])
        return full_text
    except TranscriptsDisabled:
        print(f"  Transcripts disabled for video {video_id}")
        return None
    except NoTranscriptFound:
        print(f"  No transcript found for video {video_id}")
        return None
    except Exception as e:
        print(f"  Error getting transcript for {video_id}: {e}")
        return None


def save_transcript(video: dict, transcript: str, output_dir: Path):
    """Save transcript as markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create safe filename
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in video["title"])
    safe_title = safe_title[:80]  # Limit length
    filename = f"{safe_title}.md"
    filepath = output_dir / filename

    content = f"""# {video["title"]}

## Video Info
- **Channel:** {video["channel"]}
- **URL:** {video["url"]}
- **Published:** {video["published"]}

## Description
{video["description"]}

---

## Transcript

{transcript}
"""

    filepath.write_text(content, encoding="utf-8")
    print(f"  Saved: {filepath}")
    return filepath


def save_metadata(videos: list, output_dir: Path):
    """Save metadata JSON for all fetched videos."""
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = output_dir / "_metadata.json"

    metadata = {
        "fetched_at": datetime.now().isoformat(),
        "video_count": len(videos),
        "videos": videos
    }

    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Metadata saved: {metadata_file}")


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcripts for RAG")
    parser.add_argument("--search", "-s", help="Search query")
    parser.add_argument("--channel", "-c", help="Channel ID")
    parser.add_argument("--creator", help="Creator name to search for")
    parser.add_argument("--video", "-v", help="Single video ID")
    parser.add_argument("--max-videos", "-m", type=int, default=5, help="Max videos to fetch")
    parser.add_argument("--output", "-o", help="Output directory", default=str(OUTPUT_DIR))

    args = parser.parse_args()
    output_dir = Path(args.output)

    if not any([args.search, args.channel, args.creator, args.video]):
        parser.print_help()
        print("\nExample usage:")
        print('  python fetch_transcripts.py --search "AI coding workflow"')
        print('  python fetch_transcripts.py --creator "Ryan Carson"')
        print('  python fetch_transcripts.py --video "VIDEO_ID"')
        sys.exit(1)

    videos = []

    if args.video:
        # Single video
        youtube = get_youtube_client()
        request = youtube.videos().list(part="snippet", id=args.video)
        response = request.execute()
        if response["items"]:
            item = response["items"][0]
            videos = [{
                "id": args.video,
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "description": item["snippet"]["description"],
                "published": item["snippet"]["publishedAt"],
                "url": f"https://youtube.com/watch?v={args.video}"
            }]
    elif args.search:
        print(f"Searching for: {args.search}")
        videos = search_videos(args.search, args.max_videos)
    elif args.creator:
        print(f"Searching for creator: {args.creator}")
        videos = search_by_creator_name(args.creator, args.max_videos)
    elif args.channel:
        print(f"Fetching from channel: {args.channel}")
        videos = search_channel_videos(args.channel, args.max_videos)

    print(f"Found {len(videos)} videos")

    successful = 0
    for video in videos:
        print(f"\nProcessing: {video['title']}")
        transcript = get_transcript(video["id"])
        if transcript:
            save_transcript(video, transcript, output_dir)
            video["has_transcript"] = True
            successful += 1
        else:
            video["has_transcript"] = False

    save_metadata(videos, output_dir)
    print(f"\nDone! {successful}/{len(videos)} transcripts saved to {output_dir}")


if __name__ == "__main__":
    main()
