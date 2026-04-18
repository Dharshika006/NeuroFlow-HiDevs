# NeuroFlow System Architecture

## Overview

NeuroFlow is a modular Retrieval-Augmented Generation (RAG) system composed of five tightly integrated subsystems:

1. Ingestion Subsystem
2. Retrieval Subsystem
3. Generation Subsystem
4. Evaluation Subsystem
5. Fine-Tuning Subsystem

Each subsystem is independently scalable and communicates via well-defined data contracts.

---

# 1. Ingestion Subsystem

## Purpose

Transforms raw multi-modal data into queryable vector embeddings.

## Supported Inputs

* PDF
* DOCX
* Images (OCR)
* CSV
* Web URLs

## Data Flow Diagram

```
User Upload / URL
        ↓
File Type Detection
        ↓
Content Extraction
(PDF Parser / OCR / HTML Scraper)
        ↓
Text Normalization
        ↓
Chunking (Semantic + Fixed Hybrid)
        ↓
Embedding Model
        ↓
Vector Store (pgvector)
        ↓
Metadata Storage (PostgreSQL)
```

## Output

* Embeddings stored in vector DB
* Metadata indexed for filtering

---

# 2. Retrieval Subsystem

## Purpose

Fetches the most relevant context for a user query using hybrid search.

## Retrieval Pipeline Diagram

```
User Query
     ↓
Query Embedding
     ↓
 ┌───────────────┬───────────────┬────────────────┐
 ↓               ↓               ↓
Vector Search   Keyword Search   Metadata Filter
(pgvector)      (BM25)           (Postgres)
 ↓               ↓               ↓
 └───────→ Merge Results ←───────┘
                ↓
Reciprocal Rank Fusion (RRF)
                ↓
Cross-Encoder Reranker
                ↓
Top-K Context Selection
```

## Output

Ranked context window (high relevance chunks)

---

# 3. Generation Subsystem

## Purpose

Generates responses using retrieved context and LLM routing.

## Flow Diagram

```
Query + Context
        ↓
Prompt Construction
        ↓
Model Router
 (cost / latency / domain)
        ↓
Selected LLM
        ↓
Token Streaming (SSE)
        ↓
Response Output
        ↓
Logging (prompt + context + output)
```

## Features

* Streaming responses
* Multi-model support
* Full trace logging for evaluation

---

# 4. Evaluation Subsystem

## Purpose

Continuously evaluates response quality asynchronously.

## Evaluation Flow

```
Logged Interaction
        ↓
LLM-as-Judge Scoring
        ↓
Metrics Computation
  - Faithfulness
  - Answer Relevance
  - Context Precision
  - Context Recall
        ↓
Store in PostgreSQL
        ↓
Aggregation Engine
        ↓
Dashboards / Metrics API
```

## Output

* Per-query scores
* Rolling averages

---

# 5. Fine-Tuning Subsystem

## Purpose

Improves model performance using high-quality evaluated data.

## Flow Diagram

```
Evaluation Logs
        ↓
Filter High-Quality Data
 (faithfulness > 0.8 AND rating ≥ 4)
        ↓
Dataset Builder (JSONL)
        ↓
Fine-Tuning Job
        ↓
Experiment Tracking (MLflow)
        ↓
Model Registry
        ↓
Model Router Update
```

## Output

* Fine-tuned models
* Improved routing decisions

---

# System End-to-End Flow

```
Ingestion → Storage → Retrieval → Generation → Evaluation → Fine-Tuning → Improved Generation
```

---

# Technology Stack

* Backend: FastAPI (Python)
* Frontend: React
* Database: PostgreSQL
* Vector Store: pgvector
* Retrieval: Hybrid (Vector + BM25)
* Orchestration: Prefect / Airflow
* Experiment Tracking: MLflow
* LLM Providers: OpenAI / Open-source models

---
