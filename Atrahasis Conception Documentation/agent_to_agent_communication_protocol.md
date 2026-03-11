# Agent-to-Agent Communication Protocol

## Purpose
Defines how agents exchange information inside the Collective Intelligence system.

## Message Format
{
  "agent_id": "",
  "task_type": "",
  "input_reference": "",
  "output_reference": "",
  "confidence_score": "",
  "verification_hash": ""
}

## Communication Layers
1. Task Routing
2. Result Reporting
3. Verification Messaging
4. Knowledge Updates

## Transport Methods
- REST APIs
- message queues
- event streams