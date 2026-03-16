# T-211 Pre-Ideation Analogy Brief

## Useful analogies

### 1. Instruction-set design, not sentence writing
`T-211` is closer to defining an instruction set than adding prose-level verbs. Too many opcodes create ambiguity and implementation drag; too few force overloaded meanings. The right design is a compact, orthogonal inventory.

### 2. Filesystem watch APIs versus file reads
Resource updates should not automatically become separate message classes. Modern systems often separate:
- the control action that creates a watch, from
- the stream that delivers later events.

That supports the `resource_subscribe` plus `stream_*` pattern.

### 3. HTTP methods versus application resources
Some interactions deserve distinct response classes because the reply is semantically different from the request (`tool_result`, `sampling_result`). Others can reuse one class across request and response when the contract is symmetric (`resource_list`, `prompt_get`).
