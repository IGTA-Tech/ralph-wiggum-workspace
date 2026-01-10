# Advanced Ralph Wiggum Techniques

Synthesized best practices from Geoffrey Huntley, Matt Pocock, Dexter Horthy, and Ryan Carson.

---

## The Three Modes of Ralph

### 1. HITL (Human-in-the-Loop) Ralph
**When:** Active development, exploring new areas, critical code

- You watch Ralph work in real-time
- Intervene when it goes off-track
- Provide feedback after each iteration
- Best for: Learning the codebase, complex decisions

### 2. AFK (Away-From-Keyboard) Ralph
**When:** Well-defined tasks, overnight runs, repetitive work

- Set it up, walk away, review later
- Requires excellent specs and acceptance criteria
- Must have strong automated feedback (tests, typecheck)
- Best for: Bulk refactoring, feature implementation

### 3. Scheduled Ralph
**When:** Continuous improvement, maintenance tasks

- Run focused, narrow tasks on intervals
- Daily incremental improvements
- Non-critical path work
- Best for: Code quality, consistency enforcement

---

## Context Engineering Principles

### 1. Carve Off Small Independent Contexts

**The Key Insight:** Ralph's power is NOT "run forever" but in breaking work into independent context windows.

```
BAD:  "Build the entire user authentication system"
GOOD: "Add password field to users table"
      "Create login form component"
      "Add session validation middleware"
      "Create logout endpoint"
```

**Rule of Thumb:** If you can't describe it in 2-3 sentences, split it.

### 2. Declarative Over Imperative

**BAD (Imperative):**
```
1. First, open the file
2. Then find the function
3. Add a new parameter
4. Update the return type
5. Save the file
```

**GOOD (Declarative):**
```
The getUserById function should accept an optional
`includeDeleted` boolean parameter (default: false).
When true, include soft-deleted users in results.
```

### 3. Spec Quality = Output Quality

> "If the specs are bad, the results will be meh" - Dexter Horthy

**Invest time in:**
- Clear acceptance criteria
- Example inputs/outputs
- Edge cases
- What NOT to do (non-goals)

### 4. Failures Are Data

Don't sanitize errors. Let Ralph see:
- Full error messages
- Stack traces
- Test failures
- TypeScript errors

The agent learns from confronting its mistakes.

### 5. Fresh Context > Extended Sessions

When things go wrong:
```bash
# DON'T: Try to fix in same session
# DO: Re-run the same prompt on fresh code

git stash  # or reset
# Re-run Ralph with same prompt
```

---

## The Perfect PROMPT.md Structure

```markdown
# Task: [Clear Title]

## Context
[What the agent needs to know about the codebase]

## Objective
[Declarative description of the end state]

## Acceptance Criteria
- [ ] Criterion 1 (verifiable)
- [ ] Criterion 2 (verifiable)
- [ ] npm run typecheck passes
- [ ] npm run test passes

## Non-Goals
- Do NOT change [specific files/patterns]
- Do NOT add [specific features]

## Examples
[Input/output examples if helpful]

## Completion
When all criteria pass, output:
<promise>COMPLETE</promise>
```

---

## Feedback Loop Hierarchy

**Strongest (Best for AFK Ralph):**
1. Compiler errors (TypeScript strict mode)
2. Test failures (unit, integration)
3. Linting errors (ESLint, Prettier)
4. Type coverage tools

**Medium:**
5. Build failures
6. Runtime errors in dev
7. Browser dev tools errors

**Weakest (Requires HITL):**
8. Visual/UI issues
9. Performance problems
10. User experience concerns

---

## The Ralph Tuning Process

From Geoffrey Huntley's philosophy:

```
1. Ralph produces bad output
   ↓
2. Don't blame the tool
   ↓
3. Analyze what went wrong
   ↓
4. Update PROMPT.md with:
   - Clearer instructions
   - Warning about the pitfall
   - Example of correct behavior
   ↓
5. Re-run Ralph
   ↓
6. Repeat until pattern is learned
```

**Think of it like tuning a guitar** - small adjustments, test, adjust again.

---

## Progress Tracking Pattern

### progress.txt Structure

```markdown
## Codebase Patterns
[General patterns that ALL iterations should know]
- Use `sql<number>` template for aggregations
- Always use `IF NOT EXISTS` for migrations
- Export types from actions.ts for UI

## Session Log

### Iteration 1 - [timestamp]
- Thread: [amp thread ID or reference]
- Story: US-001 - Add user status field
- Status: PASSED
- Files changed: db/migrations/001.sql, src/models/user.ts
- Learnings: Migration syntax requires specific format

### Iteration 2 - [timestamp]
- Thread: [amp thread ID]
- Story: US-002 - Add status filter UI
- Status: PASSED
- Files changed: src/components/UserList.tsx
- Learnings: Filter component pattern in /components/filters/
```

### AGENTS.md Pattern

Place in folders to give context to agents:

```markdown
# /src/components/AGENTS.md

## Conventions
- All components use TypeScript strict mode
- Use Tailwind CSS for styling
- Import types from ../types/index.ts

## Gotchas
- DatePicker requires specific timezone handling
- Modal components must use Portal

## Examples
See UserCard.tsx for the standard component pattern
```

---

## When NOT to Use Ralph

### Don't use Ralph for:
- **Exploration** - When you don't know what you're building yet
- **Architecture decisions** - Needs human judgment
- **Security-critical code** - Requires careful review
- **Performance optimization** - Needs profiling and human analysis
- **Ambiguous requirements** - Will produce ambiguous results

### Do use Ralph for:
- **Well-defined features** - Clear specs, known patterns
- **Refactoring** - Consistent changes across codebase
- **Boilerplate** - Repetitive but necessary code
- **Test writing** - Given clear function signatures
- **Documentation** - Generating docs from code

---

## Cost Optimization

From Geoffrey Huntley's $50k → $297 case:

### Strategies:
1. **Small context windows** - Don't load unnecessary files
2. **Focused prompts** - One task per iteration
3. **Strong feedback loops** - Fail fast, don't waste tokens
4. **Incremental commits** - Don't redo work
5. **AGENTS.md** - Reduce re-learning across iterations

### Typical Costs:
- Simple feature: $3-5 per iteration
- Complex feature: $10-15 per iteration
- Full feature (10 iterations): $30-50

---

## Quick Reference Commands

```bash
# Original Ralph (Geoffrey Huntley style)
while :; do cat PROMPT.md | claude-code ; done

# With iteration limit
for i in {1..10}; do cat PROMPT.md | claude-code; done

# Ryan Carson's ralph.sh
./ralph.sh 10  # 10 iterations max

# Claude Code Plugin
/ralph-loop "Your prompt" --max-iterations 10 --completion-promise "DONE"

# Check progress
cat prd.json | jq '.userStories[] | {id, title, passes}'
```

---

## The Meta-Insight

> "Dumb things can work surprisingly well"

Simple, continuous loops with clear prompts achieve complex outcomes through:
- **Repetition** - Keep trying until it works
- **Context engineering** - Right information at right time
- **Strong feedback** - Let failures teach the agent
- **Persistence** - Don't give up after first failure

The sophistication is in the PROMPT.md, not the tooling.
