# AAS CLI Task Execution Template

Use this when you want a consistent fallback prompt for direct Codex CLI work.

The preferred operator command is still:

```text
Start T-<ID>.
```

If you need to be more explicit, use the templates below.

---

## 1) Start A Real Backlog Task

```text
Start T-<ID>.

Execute it under the repo's current AAS operating rules.
Treat the task as real work, not as a planning-only exercise.
```

Expected behavior:
- route the task correctly
- prepare the task workspace/checklist
- respect claims and dependencies
- resolve any named spec ids to their actual titled file paths before reading or editing specs
- do the work instead of only describing it

---

## 2) Start A Direct-Spec Task With Stronger Enforcement

```text
Start T-<ID>.

This is a real DIRECT SPEC task. Follow the hardened direct-spec path:
- prepare the task workspace/checklist
- maintain the minimal task-local audit surface
- verify the exact claimed scope before calling it clean
- validate closeout consistency before marking it DONE

Do not stop at a progress checkpoint unless you are actually blocked, HITL-gated, or ready for assessment/closeout.
```

---

## 3) Continue A Task To Completion

```text
Continue T-<ID> to completion.

Do not stop at a narrative progress checkpoint.
Stop only if:
- you hit a real claim conflict
- you hit a real HITL gate
- you need explicit operator judgment
- or the task is genuinely ready for assessment/closeout
```

---

## 4) Force Ideation-Only On A Full Pipeline Candidate

```text
Full Pipeline Task:
Treat this as a candidate FULL PIPELINE task.
Run the current ideation path only.
Use the real AAS5 ordinary ideation hierarchy; do not simulate the swarm inside one session.
Present the option set and your recommended choice.
Stop after IDEATION and wait for my decision.
```

---

## 5) Ask For A Clean Closeout Check

```text
Before marking T-<ID> DONE, run the required closeout checks and tell me:
1. whether the scoped verification is clean,
2. whether closeout consistency is valid,
3. the exact files changed,
4. any remaining blocker if the task is not legally DONE yet.
```
