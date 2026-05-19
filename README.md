# LLM-causal-knowledge-extraction-system
LLM Causal Knowledge Extraction System automatically extracts causal scientific knowledge from research papers using LLMs and ontology-guided pipelines. The framework converts unstructured literature into structured JSON and knowledge graphs for scientific reasoning, machine learning, and discovery workflows.

## Overview

This project is a scientific literature understanding framework designed to automatically extract causal scientific knowledge from research papers and convert it into structured machine-readable representations.

The system uses large language models (LLMs), ontology-guided extraction, and structured reasoning pipelines to transform unstructured scientific literature into reusable scientific knowledge graphs and databases.

The framework is primarily designed for materials science and oxidation-related literature, but the architecture is generalizable to broader scientific domains.

---

# Key Features

- Extraction of causal scientific relationships
- Structured ontology-aligned JSON outputs
- Scientific evidence and provenance tracking
- Extraction of materials compositions and processing history
- Oxidation experiment and characterization extraction
- PDF and XML/TEI paper processing
- Docker-compatible scalable workflows
- Machine-learning-ready scientific database generation

---

# Extracted Knowledge Types

## Materials Information
- Alloy compositions
- Dopants and additives
- Material systems

## Processing Information
- Annealing conditions
- Thermal history
- Fabrication procedures
- Cooling methods

## Experimental Information
- Oxidation temperatures
- Exposure durations
- Atmosphere conditions
- Characterization procedures

## Oxidation Results
- Oxide morphologies
- Oxidation products
- Scale structures
- Spallation behavior
- SEM observations

## Causal Knowledge
- Cause-effect relationships
- Mechanism descriptions
- Scientific reasoning chains
- Evidence-supported conclusions

---

# Architecture

```text
Scientific Papers
        │
        ▼
PDF/XML Parsing (GROBID)
        │
        ▼
LLM Extraction Pipeline
        │
        ▼
Structured JSON Output
        │
        ▼
Knowledge Graph / Database
```

This repository features generalized prototypes and architectural workflows related to the manuscript 'Automated pipeline for causal knowledge extraction through LLM', currently under review at Npj Computational Materials. Core proprietary datasets and specialized weights are withheld pending publication.


