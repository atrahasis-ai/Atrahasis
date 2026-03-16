# Research Protocol

## Purpose

The AAS1 research protocol feeds the knowledge infrastructure used by invention reasoning. Research is controlled by `InventionPipelineManager`; it is not an independent stage controller.

## Knowledge Infrastructure Modules

1. `ResearchIngestionEngine`
2. `ResearchQualityFilter`
3. `ResearchSynthesisEngine`
4. `DiscoveryMap`
5. `TechnologyFrontierModel`

## Evidence Sources

- GCML documents under `docs/`
- task workspace artifacts
- prior art archives
- specification archives
- invention logs

## Output Artifacts

- `RESEARCH_INGESTION_REPORT.json`
- `RESEARCH_QUALITY_REPORT.json`
- `RESEARCH_SYNTHESIS_REPORT.json`
- `DISCOVERY_MAP.json`
- `TECHNOLOGY_FRONTIER_MODEL.json`
- `DISCOVERY_GAP_REPORT.json`
- `OPPORTUNITY_REPORT.json`

## Communication Rule

Research modules do not call each other directly. The pipeline manager sequences them, persists outputs, and passes structured results downstream.
