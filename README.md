# NeuroFlow-HiDevs

NeuroFlow is a modular **Retrieval-Augmented Generation (RAG)** system designed to support scalable, high-quality AI pipelines with ingestion, retrieval, generation, evaluation, and fine-tuning capabilities.

## 📌 Overview

This project focuses on designing a production-ready architecture before implementation. It emphasizes system design, API contracts, and architectural decision-making.

## ⚙️ Core Subsystems

* **Ingestion Subsystem**
  Processes raw data (PDF, DOCX, images, CSV, URLs) into embeddings.

* **Retrieval Subsystem**
  Hybrid search (vector + keyword + metadata) with reranking.

* **Generation Subsystem**
  LLM-based response generation with streaming and logging.

* **Evaluation Subsystem**
  Automated scoring using faithfulness, relevance, precision, and recall.

* **Fine-Tuning Subsystem**
  Extracts high-quality data for model improvement.

---

## 📁 Project Structure

```
backend/
frontend/
pipelines/
evaluation/
infra/
docs/
```

---

## 🧠 Key Features

* Hybrid Retrieval (Vector + BM25)
* Reciprocal Rank Fusion (RRF)
* Cross-Encoder Reranking
* LLM Routing Strategy
* Automated Evaluation (LLM-as-judge)
* Fine-Tuning Pipeline with MLflow

---

## 🚀 Status

🚧 Architecture & API design completed
⏳ Implementation in progress

---

## 📄 Documentation

* `docs/architecture.md` → System design
* `docs/api-contracts.md` → REST API definitions
* `docs/adr/` → Architecture Decision Records

---
