# YouTube RAG Tool

Fetch YouTube transcripts and convert them into implementation-ready guides.

## Setup

### 1. Install Dependencies
```bash
cd tools/youtube-rag
pip install -r requirements.txt
```

### 2. Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select existing)
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy the API key

### 3. Configure API Key
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
YOUTUBE_API_KEY=your_actual_key_here
```

**IMPORTANT:** Never commit your `.env` file to git!

## Usage

### Search for Videos
```bash
# Search by topic
python fetch_transcripts.py --search "AI coding workflow"

# Search by creator name
python fetch_transcripts.py --creator "Ryan Carson"

# Limit results
python fetch_transcripts.py --search "Ralph Wiggum" --max-videos 3
```

### Fetch Single Video
```bash
python fetch_transcripts.py --video "VIDEO_ID_HERE"
```

### Output
Transcripts are saved to `transcripts/` folder as markdown files:
```
transcripts/
├── _metadata.json       # Info about all fetched videos
├── Video Title 1.md     # Transcript with metadata
├── Video Title 2.md
└── ...
```

## Converting to Implementation Guides

After fetching transcripts, use Claude to convert them:

```
I have a transcript at transcripts/Video-Title.md

Please use the transcript-to-guide skill to convert this
into an implementation guide.
```

Or reference the skill directly:
```
@skills/transcript-to-guide/SKILL.md

Convert this transcript to an implementation guide:
[paste transcript]
```

## Workflow

1. **Fetch transcripts** from key experts:
   ```bash
   python fetch_transcripts.py --creator "Ryan Carson" --max-videos 5
   python fetch_transcripts.py --creator "Matt Pocock" --max-videos 5
   ```

2. **Review transcripts** in `transcripts/` folder

3. **Convert to guides** using Claude + the transcript-to-guide skill

4. **Save guides** to your workspace for reference

## Key Creators to Follow

| Creator | Focus | Search Term |
|---------|-------|-------------|
| Geoffrey Huntley | Ralph creator | `"Geoffrey Huntley Ralph"` |
| Ryan Carson | PRD workflow | `"Ryan Carson AI coding"` |
| Matt Pocock | TypeScript + AI | `"Matt Pocock Ralph"` |
| Dexter Horthy | Context engineering | `"Dexter Horthy HumanLayer"` |

## Troubleshooting

### "Transcripts disabled"
Some videos don't have captions. Try different videos from the same creator.

### "API quota exceeded"
YouTube API has daily limits. Wait 24 hours or create a new project.

### "No transcript found"
The video might only have auto-generated captions in a different language. Try adding `--language en` (feature coming soon).

## File Structure
```
youtube-rag/
├── fetch_transcripts.py   # Main script
├── requirements.txt       # Python dependencies
├── .env.example          # API key template
├── .env                  # Your API key (don't commit!)
├── README.md             # This file
└── transcripts/          # Output folder
    ├── _metadata.json
    └── *.md
```
