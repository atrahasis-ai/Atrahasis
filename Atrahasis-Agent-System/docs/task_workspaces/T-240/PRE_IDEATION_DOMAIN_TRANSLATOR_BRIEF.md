# T-240 Domain Translator Brief

Domain:
- sovereign tool connectivity protocol
- semantically typed invocation and accountable result handling
- native replacement for `MCP`-style tool workflows

Problem statement:
- How should `AACP v2` expose tools so that agents can discover available tool
  contracts, invoke them with canonical typed inputs, receive accountable
  outputs, and track tool-catalog changes without collapsing discovery,
  security, runtime, and provenance into one ambiguous API surface?

## Analogy 1: Clinical laboratory orders

Source domain:
- hospital or clinic lab ordering and result return

Structural parallel:
- a clinician orders a specific test from a known catalog,
- the order must match a valid specimen type and required fields,
- the lab instrument executes the test,
- the returned result includes metadata, source, and reference context,
- corrections or test unavailability are announced separately.

Where the analogy breaks:
- biological samples have physical handling constraints that software calls do
  not.
- the pace and irreversibility of lab work differ from software execution.

Design insight:
- invocation should bind tightly to a specific typed contract,
- result objects should carry explicit execution context and accountability
  metadata,
- catalog changes should be modeled independently from one static catalog fetch.

## Analogy 2: CNC tool crib plus machining job sheet

Source domain:
- machine-shop tool inventory and CNC job execution

Structural parallel:
- a machine advertises which cutters and fixtures are currently available,
- a job references specific tools, tolerances, and material assumptions,
- execution produces both a work result and machine-context traces,
- worn or removed tools trigger inventory updates.

Where the analogy breaks:
- mechanical wear and physical reservation are stronger than many software tool
  cases.
- some software tools are stateless and multi-tenant in ways a physical tool
  crib is not.

Design insight:
- `tool_discovery` and `tool_change_notification` should be first-class and not
  inferred from invocation failures alone,
- tool identity, version, and compatibility state should stay stable across
  calls,
- execution results should be distinct artifacts from the invocation request.

## Analogy 3: Container shipping manifest and customs seal

Source domain:
- international container logistics

Structural parallel:
- cargo is declared through a manifest,
- each container has an identity and a chain of custody,
- handoffs are validated at checkpoints,
- tamper evidence matters as much as the payload description,
- status updates can occur independently of the original booking.

Where the analogy breaks:
- transport custody is physical and location-bound; protocol interactions are
  usually faster and more reversible.
- software results can be partially computed or regenerated.

Design insight:
- provenance and tamper-evident lineage should travel with the tool result, not
  be retrofitted later,
- the protocol should distinguish native execution from translated or bridged
  execution,
- inventory updates need their own authenticated event trail.

## Analogy 4: Restaurant expeditor tickets and the "86" board

Source domain:
- kitchen ticketing and service orchestration in a restaurant

Structural parallel:
- a menu describes durable offerings,
- each ticket adds typed modifiers and special constraints,
- stations execute their portion of the request,
- the expeditor verifies completion and passes the final plated result,
- the "86" board announces temporary unavailability or substitutions without
  rewriting the whole menu.

Where the analogy breaks:
- restaurant execution is highly human and informal compared with protocol
  machinery.
- substitutions may be socially negotiated in ways software protocols should
  avoid.

Design insight:
- the protocol should canonicalize invocation modifiers instead of treating them
  as loose free text,
- result packaging should separate "done" from "done and accountability-wrapped,"
- change notifications should support temporary and versioned catalog changes
  without turning the manifest into live telemetry.

## Cross-domain synthesis

Shared structural lessons:
1. Catalog truth, invocation truth, and result truth are related but distinct.
2. Side-effectful execution needs stronger policy and accountability than simple
   data retrieval.
3. Availability and catalog-change signals need their own lifecycle.
4. Stable tool identity must outlive any one session or invocation.

Translation guidance for the Ideation Council:
- prefer concepts that keep discovery, invocation, result, and change
  notification separate but connected,
- preserve explicit contract pinning, authorization, and provenance,
- avoid concepts that overload the manifest or that drag all runtime/streaming
  behavior into the core tool protocol too early.
