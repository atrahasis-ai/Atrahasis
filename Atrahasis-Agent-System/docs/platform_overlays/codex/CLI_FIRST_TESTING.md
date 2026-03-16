# CLI-First AAS5 Testing
**Platform:** OpenAI Codex
**Purpose:** Evaluate AAS5 in the same terminal-first workflow you normally use, without depending on the controller UI

---

## Goal

Use the new Atrahasis Agent System in the Codex CLI exactly the way you normally work:
- open Codex in the repo
- talk to it directly in the terminal
- compare that experience and output quality against the previous system

Do not treat the web controller, daemon, or App Server as required for this evaluation.

---

## Start AAS5 in the Terminal

From the repo root:

```powershell
pwsh -File scripts/start_aas5_codex.ps1
```

Optional variants:

```powershell
pwsh -File scripts/start_aas5_codex.ps1 -Alpha
pwsh -File scripts/start_aas5_codex.ps1 -Search
pwsh -File scripts/start_aas5_codex.ps1 -CodeMode
pwsh -File scripts/start_aas5_codex.ps1 -MultiAgent
```

What this does:
- starts `codex` or `codex-alpha`
- sets the working directory to the Atrahasis repo
- loads repo-local Codex config from `.codex/config.toml`
- keeps the interaction model as plain terminal conversation

---

## What To Ignore For This Test

For the first evaluation pass, ignore:
- the operator web UI
- the daemon/service controls
- App Server features
- controller-managed review and queue surfaces

Those may be useful later, but they are not the right baseline for determining whether AAS5 itself improves direct Codex performance.

---

## Recommended A/B Test Method

Use the same task in both systems.

Keep these fixed:
- same Codex binary when possible
- same model when possible
- same reasoning setting when possible
- same prompt wording
- same amount of follow-up interaction

Compare on:
- speed to useful first answer
- clarity of plan
- need for correction
- depth of repo understanding
- quality of implementation
- quality of judgment
- novelty of proposed improvements
- whether it stays on task without overbuilding

---

## Minimal Test Loop

1. Start Codex with the previous system.
2. Give it the same real task you care about.
3. Record:
   - first useful response quality
   - number of course corrections needed
   - time to acceptable result
   - final result quality
4. Start Codex with AAS5 using:

```powershell
pwsh -File scripts/start_aas5_codex.ps1
```

5. Repeat the same task.
6. Compare outcomes directly.

---

## Suggested First Evaluation Tasks

Good first tests are tasks that expose judgment, repo reading, and execution quality:
- one architecture question
- one code modification task
- one debugging task
- one task where novelty matters

Avoid using only trivial tasks, because they will not tell you much about whether AAS5 is actually better.

---

## Interpreting Results

If AAS5 is better, you should see one or more of these:
- faster orientation to repo state
- fewer dumb detours
- stronger use of canonical docs
- better handling of task structure and stage discipline
- better invention pressure when the task benefits from it
- cleaner judgment about when not to overcomplicate

If AAS5 is worse, you will usually see:
- too much setup overhead
- too much process language
- too many internal abstractions surfacing in normal conversation
- slower movement on straightforward tasks

That is the main thing to measure first.

---

## Principle

The first question is not whether the controller stack is impressive.

The first question is whether talking directly to Codex in the terminal becomes better when Codex is operating inside AAS5 than when it is operating inside the previous system.
