# PRD Generator Project Instructions

## Overview

This Claude Project is designed to help you create Product Requirement Documents (PRDs) and convert them to JSON format for use with autonomous AI agent loops like Ralph Wiggum and Claude Code.

**Based on:**
- Ryan Carson's ai-dev-tasks system (https://github.com/snarktank/ai-dev-tasks)
- Ryan Carson's Ralph autonomous agent loop (https://github.com/snarktank/ralph)
- Anthropic's Ralph Wiggum plugin for Claude Code (https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)

---

## PHASE 1: Creating a PRD (Markdown Format)

### Purpose
Create a detailed Product Requirements Document (PRD) in Markdown format that is clear, actionable, and suitable for a junior developer to understand and implement.

### Workflow

#### Step 1: Receive Initial Prompt
The user provides a brief description or request for a new feature or functionality.

#### Step 2: Ask Clarifying Questions
Before writing the PRD, ask only the most essential clarifying questions needed to write a clear PRD.

**Rules:**
- Limit questions to 3-5 critical gaps in understanding
- Focus on the "what" and "why" of the feature, not the "how"
- Provide options in letter/number lists for easy response
- Only ask when the answer isn't reasonably inferable from the initial prompt

**Common Areas Needing Clarification:**

| Area | Example Question |
|------|------------------|
| Problem/Goal | "What problem does this feature solve for the user?" |
| Core Functionality | "What are the key actions a user should be able to perform?" |
| Scope/Boundaries | "Are there any specific things this feature should NOT do?" |
| Success Criteria | "How will we know when this feature is successfully implemented?" |

**Question Format Example:**
```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Generate additional revenue

2. Who is the target user for this feature?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only

3. What is the expected timeline?
   A. Urgent (1-2 weeks)
   B. High priority (3-4 weeks)
   C. Standard (1-2 months)
   D. Future consideration (3+ months)
```

The user can respond with selections like "1A, 2C, 3B"

#### Step 3: Generate PRD

After receiving clarifying answers, generate the PRD using this structure:

### PRD Structure

```markdown
# [Feature Name]

## Introduction/Overview
Briefly describe the feature and the problem it solves. State the goal.

## Goals
List the specific, measurable objectives for this feature.
- Goal 1
- Goal 2
- Goal 3

## User Stories
Detail the user narratives describing feature usage and benefits.
- As a [user type], I want [feature] so that [benefit]
- As a [user type], I want [feature] so that [benefit]

## Functional Requirements
List the specific functionalities the feature must have. Use clear, concise language.
1. The system must allow users to [action]
2. The system must [action]
3. The system must [action]

## Non-Goals (Out of Scope)
Clearly state what this feature will NOT include to manage scope.
- Will not include X
- Will not support Y

## Design Considerations (Optional)
Link to mockups, describe UI/UX requirements, or mention relevant components/styles.

## Technical Considerations (Optional)
Mention any known technical constraints, dependencies, or suggestions.
- Should integrate with existing [module]
- Must use [technology/pattern]

## Success Metrics
How success will be measured.
- Metric 1
- Metric 2

## Open Questions
List any remaining questions or areas needing further clarification.
```

#### Step 4: Save PRD
Save the generated document as `prd-[feature-name].md` inside the `/tasks` directory.

**Important:** Assume the primary reader of the PRD is a junior developer. Requirements should be explicit, unambiguous, and avoid jargon where possible.

---

## PHASE 2: Converting PRD to JSON (prd.json)

### Purpose
Convert the markdown PRD to a JSON format that autonomous AI agent loops (like Ralph) can execute.

### JSON Schema

```json
{
  "project": "Project Name",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description from PRD title/intro]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2",
        "npm run typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Critical Rules for User Stories

#### 1. Size Matters - Keep Stories Small
Each story must be completable in ONE agent iteration (~one context window).

**Right-sized stories:**
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

**Too big (split these):**
- "Build the entire dashboard"
- "Add authentication"
- "Refactor the API"

**Rule of thumb:** If you can't describe the change in 2-3 sentences, it's too big.

#### 2. Priority Order
- Stories execute in priority order (1 = highest)
- Earlier stories must NOT depend on later ones
- Lower priority numbers execute first

#### 3. Acceptance Criteria Must Be Verifiable
Each criterion must be something the agent can CHECK, not something vague.

**Good criteria:**
- "npm run typecheck passes"
- "User can click 'Save' button and see success toast"
- "Database migration creates 'status' column on 'orders' table"
- "API returns 200 with correct JSON structure"

**Bad criteria:**
- "Code is clean" (subjective)
- "Works well" (vague)
- "Feels fast" (not measurable)

#### 4. Frontend Stories Need Browser Verification
Frontend stories must include "Verify in browser" in acceptance criteria:
```json
{
  "acceptanceCriteria": [
    "Component renders without errors",
    "Verify in browser: button is visible and clickable",
    "Clicking button triggers correct action"
  ]
}
```

### JSON Conversion Process

1. **Extract project name** from PRD title
2. **Generate branchName** in format `ralph/[feature-name-kebab-case]`
3. **Convert each user story** from the PRD:
   - Assign unique ID (US-001, US-002, etc.)
   - Keep the "As a... I want... so that..." format
   - Break functional requirements into acceptance criteria
   - Ensure each story is small enough for one iteration
4. **Set all `passes` to `false`** initially
5. **Assign priorities** based on dependencies and importance

### Example Conversion

**From PRD:**
```markdown
# Friends Outreach Feature

## User Stories
- As a user, I want to mark investors as "friends" for warm outreach

## Functional Requirements
1. Toggle between cold/friend on investor list
2. Friends get shorter follow-up sequence (3 instead of 5)
3. Different message template asking for deck feedback
4. Filter list by type
```

**To JSON:**
```json
{
  "project": "Untangle",
  "branchName": "ralph/friends-outreach",
  "description": "Add ability to mark investors as friends for warm outreach",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add friend toggle to investor list",
      "description": "As a user, I want to toggle between cold/friend on investor list so that I can mark warm contacts",
      "acceptanceCriteria": [
        "Toggle button visible on each investor row",
        "Clicking toggle updates investor.isFriend in database",
        "npm run typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Shorter follow-up sequence for friends",
      "description": "As a user, I want friends to get shorter follow-up sequence (3 instead of 5) so that warm outreach feels personal",
      "acceptanceCriteria": [
        "Friends receive 3 follow-up emails instead of 5",
        "Sequence logic checks isFriend flag",
        "npm run typecheck passes"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Friend-specific message template",
      "description": "As a user, I want a different message template for friends asking for deck feedback",
      "acceptanceCriteria": [
        "New email template created for friends",
        "Template asks for deck feedback",
        "Correct template selected based on isFriend flag"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter investor list by type",
      "description": "As a user, I want to filter the investor list by type (cold/friend) so that I can manage outreach",
      "acceptanceCriteria": [
        "Filter dropdown added to investor list",
        "Selecting 'Friends' shows only friends",
        "Selecting 'Cold' shows only cold contacts",
        "Verify in browser: filter works correctly"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## PHASE 3: Running with Ralph (Autonomous Loop)

### Overview
Ralph is an autonomous AI agent loop that executes prd.json user stories one at a time until all pass.

### Setup

#### Copy Files to Your Project
```bash
mkdir -p scripts/ralph
cp ralph.sh scripts/ralph/
cp prompt.md scripts/ralph/
chmod +x scripts/ralph/ralph.sh
```

### ralph.sh Script

```bash
#!/bin/bash
# Usage: ./ralph.sh [max_iterations]

set -e

MAX_ITERATIONS=${1:-10}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRD_FILE="$SCRIPT_DIR/prd.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"
ARCHIVE_DIR="$SCRIPT_DIR/archive"
LAST_BRANCH_FILE="$SCRIPT_DIR/.last-branch"

# Archive previous run if branch changed
if [ -f "$PRD_FILE" ] && [ -f "$LAST_BRANCH_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || echo "")

  if [ -n "$CURRENT_BRANCH" ] && [ -n "$LAST_BRANCH" ] && [ "$CURRENT_BRANCH" != "$LAST_BRANCH" ]; then
    DATE=$(date +%Y-%m-%d)
    FOLDER_NAME=$(echo "$LAST_BRANCH" | sed 's|^ralph/||')
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$DATE-$FOLDER_NAME"

    mkdir -p "$ARCHIVE_FOLDER"
    [ -f "$PRD_FILE" ] && cp "$PRD_FILE" "$ARCHIVE_FOLDER/"
    [ -f "$PROGRESS_FILE" ] && cp "$PROGRESS_FILE" "$ARCHIVE_FOLDER/"

    # Reset progress for new feature
    rm -f "$PROGRESS_FILE"

    echo "Archived previous run to $ARCHIVE_FOLDER"
  fi
fi

# Save current branch
if [ -f "$PRD_FILE" ]; then
  jq -r '.branchName // empty' "$PRD_FILE" > "$LAST_BRANCH_FILE" 2>/dev/null || true
fi

# Run iterations
for ((i=1; i<=MAX_ITERATIONS; i++)); do
  echo "=== Ralph Iteration $i of $MAX_ITERATIONS ==="

  # Run Claude Code / Amp with the prompt
  # For Claude Code:
  OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | claude --dangerously-allow-all 2>&1 | tee /dev/stderr) || true

  # For Amp:
  # OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | amp --dangerously-allow-all 2>&1 | tee /dev/stderr) || true

  # Check for completion
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo "=== All stories complete! ==="
    exit 0
  fi

  echo "=== Iteration $i complete, continuing... ==="
done

echo "=== Max iterations reached ==="
```

### prompt.md Template

```markdown
# Ralph Agent Instructions

## Setup
1. Read the PRD at prd.json (in the same directory as this file)
2. Read the progress log at progress.txt (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD branchName. If not, check it out or create from main.

## Pick a Story
Pick the highest priority user story where `passes: false`

## Implement the Story
1. Implement ONLY that single story
2. Follow the acceptance criteria exactly
3. Run quality checks (typecheck, tests)
4. Commit if checks pass

## Update Files
1. Update prd.json to mark the story as `passes: true`
2. Append learnings to progress.txt

## Codebase Patterns
If you discover a reusable pattern that future iterations should know, add it to the "## Codebase Patterns" section at the TOP of progress.txt:

```
## Codebase Patterns
- Example: Use `sql<number>` template for aggregations
- Example: Always use `IF NOT EXISTS` for migrations
- Example: Export types from actions.ts for UI components
```

Only add patterns that are general and reusable, not story-specific details.

## Completion Check
After completing a user story, check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:

<promise>COMPLETE</promise>

If there are still stories with `passes: false`, end your response normally (another iteration will pick up the next story).
```

### Key Files

| File | Purpose |
|------|---------|
| `ralph.sh` | The bash loop that spawns fresh agent instances |
| `prompt.md` | Instructions given to each agent instance |
| `prd.json` | User stories with `passes` status (the task list) |
| `progress.txt` | Append-only learnings for future iterations |

### How Ralph Works

1. Create a feature branch (from PRD `branchName`)
2. Pick the highest priority story where `passes: false`
3. Implement that single story
4. Run quality checks (typecheck, tests)
5. Commit if checks pass
6. Update prd.json to mark story as `passes: true`
7. Append learnings to progress.txt
8. Repeat until all stories pass or max iterations reached

### Critical Concepts

#### Each Iteration = Fresh Context
Each iteration spawns a new agent instance with clean context. The only memory between iterations is:
- Git history (commits from previous iterations)
- `progress.txt` (learnings and context)
- `prd.json` (which stories are done)

#### Stop Condition
When all stories have `passes: true`, Ralph outputs `<promise>COMPLETE</promise>` and the loop exits.

---

## Using with Claude Code (Ralph Wiggum Plugin)

If using Claude Code instead of a bash script, use the ralph-wiggum plugin:

### Installation
```bash
/plugin ralph-wiggum
```

### Usage
```bash
/ralph-loop "Your task description" --completion-promise "DONE" --max-iterations 20
```

### How It Works
1. You run `/ralph-loop` once
2. Claude works on the task
3. Claude tries to exit
4. Stop hook blocks exit and feeds the same prompt back
5. Repeat until completion promise is found or max iterations reached

### Example with TODO File
```bash
/ralph-loop "Go through TODO.md step-by-step and check off every step once complete. When all tasks are done, output <promise>DONE</promise>" --completion-promise "DONE" --max-iterations 50
```

---

## Quick Reference Commands

### Create PRD
```
Create a PRD for [describe your feature]
```

### Convert to JSON
```
Convert this PRD to prd.json format
```

### Check Progress
```bash
# See which stories are done
cat prd.json | jq '.userStories[] | {id, title, passes}'

# See learnings from previous iterations
cat progress.txt

# Check git history
git log --oneline -10
```

---

## Best Practices

1. **Be Specific** - The more context and clear instructions you provide, the better the output
2. **Keep Stories Small** - Each story should complete in one context window
3. **Make Criteria Verifiable** - Acceptance criteria must be checkable, not subjective
4. **Order Dependencies** - Higher priority stories should not depend on lower priority ones
5. **Use Consistent Naming** - Follow kebab-case for branch names
6. **Document Patterns** - Add reusable learnings to progress.txt

---

## Troubleshooting

### Story Too Big
If an agent runs out of context before finishing, the story is too big. Split it into smaller stories.

### Stuck in Loop
If Ralph keeps failing on the same story:
1. Check progress.txt for patterns
2. Add more specific acceptance criteria
3. Break the story into smaller parts

### Quality Checks Failing
Ensure acceptance criteria include quality checks:
- `npm run typecheck passes`
- `npm run test passes`
- `npm run lint passes`
