# Ralph Workspace - Reference Toolkit

Everything you need to use the Ralph autonomous AI coding loop with Claude Code.

## Quick Start

1. **Read the basics:** `RALPH-INSTRUCTIONS.md` - covers PRD → JSON → Ralph workflow
2. **Learn from experts:** `RALPH-EXPERTS.md` - key personalities and their insights
3. **Advanced techniques:** `ADVANCED-RALPH-TECHNIQUES.md` - synthesized best practices
4. **Run Ralph** using the `/ralph-loop` command or `ralph.sh`

## Key Documents

| File | Description |
|------|-------------|
| `RALPH-INSTRUCTIONS.md` | Step-by-step PRD → JSON → Ralph workflow |
| `RALPH-EXPERTS.md` | Geoffrey Huntley, Matt Pocock, Dexter Horthy, Ryan Carson insights |
| `ADVANCED-RALPH-TECHNIQUES.md` | Synthesized best practices from all experts |

## Folder Structure

```
ralph-workspace/
|
+-- RALPH-INSTRUCTIONS.md      <-- Core workflow guide
+-- RALPH-EXPERTS.md           <-- Expert insights & quotes
+-- ADVANCED-RALPH-TECHNIQUES.md <-- Advanced best practices
|
+-- skills/                    Skills/prompts for AI agents
|   +-- prd/                   PRD generator skill
|   +-- ralph/                 PRD-to-JSON converter skill
|   +-- dev-browser/           Browser control for testing frontend
|   +-- transcript-to-guide/   Convert video transcripts to guides
|
+-- templates/                 Copy these to your projects
|   +-- prompt.md              System prompt for Ralph iterations
|   +-- prd.json.example       Example prd.json format
|   +-- ralph.sh               Bash loop script
|   +-- AGENTS.md              Template for project learnings
|
+-- tools/                     Utility tools
|   +-- youtube-rag/           Fetch YouTube transcripts for RAG
|       +-- fetch_transcripts.py
|       +-- requirements.txt
|       +-- README.md
|
+-- source-guides/             Original guides from repos
|   +-- create-prd.md          PRD creation guide
|   +-- generate-tasks.md      Task generation guide
|
+-- claude-code-plugin/        Claude Code integration
    +-- ralph-wiggum/          Adds /ralph-loop command
```

## Using with Claude Code

```bash
/ralph-loop "Your task" --completion-promise "DONE" --max-iterations 20
```

## YouTube RAG Tool

Fetch transcripts from AI coding experts:

```bash
cd tools/youtube-rag
pip install -r requirements.txt
python fetch_transcripts.py --creator "Ryan Carson" --max-videos 5
```

See `tools/youtube-rag/README.md` for full setup.

## Key Expert Resources

| Expert | Contribution | Link |
|--------|-------------|------|
| Geoffrey Huntley | Original Ralph creator | https://ghuntley.com/ralph/ |
| Matt Pocock | 11 Tips for Ralph | https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum |
| Dexter Horthy | Context Engineering | https://www.humanlayer.dev/blog/brief-history-of-ralph |
| Ryan Carson | PRD Workflow | https://github.com/snarktank/ralph |
| Boris Cherny | Anthropic Plugin | https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum |

## Source Repos

- [snarktank/ralph](https://github.com/snarktank/ralph) - Core Ralph system
- [snarktank/ai-dev-tasks](https://github.com/snarktank/ai-dev-tasks) - PRD workflow
- [snarktank/amp-skills](https://github.com/snarktank/amp-skills) - Skills library
- [anthropics/claude-code ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) - Claude Code plugin

## Credits

- Ralph pattern by Geoffrey Huntley
- PRD workflow by Ryan Carson
- Context Engineering by Dexter Horthy
- TypeScript tips by Matt Pocock
- Official plugin by Anthropic (Boris Cherny)
