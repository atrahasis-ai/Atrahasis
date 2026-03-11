# Atrahasis Architecture Diagram Set

Version: 1.0.0 Date: 2026-03-08

This document contains the **visual architecture models** for the
Atrahasis AASL‑native runtime. Diagrams are expressed in **Mermaid** so
they can render in GitHub, Markdown viewers, and documentation systems.

These diagrams correspond directly to the Master Specification.

------------------------------------------------------------------------

# 1. Overall Atrahasis System Architecture

``` mermaid
flowchart TD
    A[External Inputs
User / APIs / Documents]
    B[AASC Compiler]
    C[AASL Semantic Layer]
    D[CIOS Orchestration]
    E[Agent Execution Layer]
    F[Verification Layer
(Verichain)]
    G[Shared Semantic Memory]
    H[Distributed Federation]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
```

Purpose: Shows the **core intelligence pipeline** of the system.

------------------------------------------------------------------------

# 2. AASL Language Ecosystem

``` mermaid
flowchart LR
    A[AASL Source]
    B[Parser]
    C[Validator]
    D[Canonicalizer]
    E[Runtime Object Graph]
    F[Query Engine]
    G[Storage]
    H[Federation]

    A --> B --> C --> D --> E
    E --> F
    E --> G
    G --> H
```

Purpose: Shows how the language flows from text to runtime to
distributed knowledge.

------------------------------------------------------------------------

# 3. First Runtime Service Architecture

``` mermaid
flowchart TD
    Gateway[API Gateway]
    Ingress[Ingress Service]
    Coordinator[Coordinator Service]
    Agents[Agent Service]
    Verification[Verification Service]
    Memory[Memory Service]
    Query[Query Service]
    Storage[Storage Service]

    Gateway --> Ingress
    Ingress --> Coordinator
    Coordinator --> Agents
    Agents --> Verification
    Verification --> Memory
    Memory --> Storage
    Query --> Storage
    Gateway --> Query
```

Purpose: Shows the **runtime microservice layout**.

------------------------------------------------------------------------

# 4. Agent Interaction Flow

``` mermaid
sequenceDiagram
    participant User
    participant Ingress
    participant Coordinator
    participant ResearchAgent
    participant AnalysisAgent
    participant VerificationAgent
    participant Memory

    User->>Ingress: Submit request
    Ingress->>Coordinator: task_submission
    Coordinator->>Memory: memory_lookup_request

    alt Memory hit
        Memory-->>Coordinator: reusable result
        Coordinator-->>User: return result
    else Memory miss
        Coordinator->>ResearchAgent: task_assignment
        ResearchAgent-->>Coordinator: evidence bundle
        Coordinator->>AnalysisAgent: task_assignment
        AnalysisAgent-->>Coordinator: claim bundle
        Coordinator->>VerificationAgent: verification_request
        VerificationAgent-->>Coordinator: verification_result
        Coordinator->>Memory: memory_admission_request
        Memory-->>Coordinator: admission_result
        Coordinator-->>User: verified result
    end
```

Purpose: Illustrates the **complete semantic reasoning loop**.

------------------------------------------------------------------------

# 5. Verification Pipeline

``` mermaid
flowchart TD
    A[Candidate Bundle]
    B[Evidence Inspection]
    C[Independent Evaluation]
    D[Claim Comparison]
    E[Verification Result]
    F[Trusted Admission]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
```

Purpose: Shows how claims become **trusted knowledge**.

------------------------------------------------------------------------

# 6. Semantic Memory Model

``` mermaid
flowchart LR
    Bundle[Semantic Bundle]
    Objects[AASL Objects]
    References[Reference Graph]
    Provenance[Provenance Records]
    Verification[Verification Records]

    Bundle --> Objects
    Objects --> References
    Objects --> Provenance
    Objects --> Verification
```

Purpose: Shows the **bundle‑centric storage model**.

------------------------------------------------------------------------

# 7. Distributed Federation Model

``` mermaid
flowchart LR
    NodeA[Atrahasis Node A]
    NodeB[Atrahasis Node B]
    NodeC[Atrahasis Node C]

    NodeA <--> NodeB
    NodeB <--> NodeC
    NodeA <--> NodeC
```

Purpose: Shows how knowledge stores synchronize across nodes.

------------------------------------------------------------------------

# 8. End‑to‑End Knowledge Lifecycle

``` mermaid
flowchart TD
    Input[External Input]
    Compile[AASC Compile]
    Task[AASL Task Bundle]
    Execute[Agent Execution]
    Verify[Verification]
    Store[Semantic Memory]
    Reuse[Future Task Reuse]

    Input --> Compile
    Compile --> Task
    Task --> Execute
    Execute --> Verify
    Verify --> Store
    Store --> Reuse
```

Purpose: Shows how Atrahasis builds **cumulative machine knowledge**.

------------------------------------------------------------------------

# 9. Diagram Usage

These diagrams should be used in:

-   developer documentation
-   architecture reviews
-   onboarding materials
-   implementation planning
-   governance discussions

They represent the **visual model of the canonical architecture**.

------------------------------------------------------------------------

# 10. Notes

All diagrams correspond directly to the components defined in:

-   Atrahasis AASL Runtime Master Specification
-   Semantic Closure Policy
-   Implementation Milestone Plan

Any architecture change must update both the specification and these
diagrams.
