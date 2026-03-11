# Human-in-the-Loop Policy (v1.0)
**Owner:** User (policy), Director (enforcement)

## Principle
The system runs autonomously by default, except for categories with outsized consequences for IP, direction, or resource commitment.

## Mandatory Approval Categories
Director must request explicit approval before proceeding when the work includes:

1. **Concept selection**
   - Choosing which invention concepts to pursue further from Ideation Council output

2. **Pivot decisions**
   - Fundamentally changing the invention direction after research or assessment

3. **External research**
   - Accessing external databases, APIs, or services for prior art searches

4. **Resource-intensive prototyping**
   - Building prototypes requiring significant compute, external services, or paid APIs

5. **Patent-related decisions**
   - Any decision about patent claims, filing strategy, or IP ownership

6. **Public disclosure risk**
   - Any action that could constitute public disclosure of the invention (destroying patent novelty)

7. **Abandonment**
   - Deciding to stop pursuing an invention line entirely

## Approval Payload
Director presents:
- the exact action or plan requiring approval
- risks and implications
- what will happen after approval

User responds with:
- `APPROVED` or `REJECTED` (and optional constraints)

Approval is recorded in `docs/AGENT_STATE.md` under `approvals_pending` / resolution notes.
