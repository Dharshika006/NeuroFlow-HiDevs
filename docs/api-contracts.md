# API Contracts — NeuroFlow

## Authentication

All endpoints require **Bearer Token (JWT)** unless stated otherwise.

---

# 1. POST /ingest

## Description

Ingest files or URLs into the system.

## Authentication

Required

## Rate Limit

10 requests/min

## Request Body

```json
{
  "source_type": "file | url",
  "file": "binary (optional)",
  "url": "string (optional)",
  "metadata": {
    "source": "string",
    "tags": ["string"]
  }
}
```

## Response Body

```json
{
  "ingestion_id": "uuid",
  "status": "processing"
}
```

## Errors

* 400: Invalid input
* 401: Unauthorized
* 413: File too large
* 415: Unsupported file type
* 500: Internal processing error

---

# 2. POST /query

## Description

Execute RAG query.

## Authentication

Required

## Rate Limit

30 requests/min

## Request Body

```json
{
  "query": "string",
  "pipeline_id": "string",
  "top_k": 5,
  "filters": {}
}
```

## Response Body

```json
{
  "query_id": "uuid",
  "status": "streaming"
}
```

## Errors

* 400: Invalid query
* 401: Unauthorized
* 404: Pipeline not found
* 429: Rate limit exceeded
* 500: Retrieval/generation failure

---

# 3. GET /query/{query_id}/stream

## Description

Stream generated response via SSE.

## Authentication

Required

## Rate Limit

60 connections/min

## Response (SSE)

```json
{
  "token": "string",
  "done": false
}
```

## Errors

* 401: Unauthorized
* 404: Query not found
* 500: Streaming failure

---

# 4. GET /evaluations

## Description

Retrieve evaluation results (paginated)

## Authentication

Required

## Rate Limit

20 requests/min

## Query Params

* page: integer
* limit: integer

## Response Body

```json
{
  "results": [
    {
      "query_id": "uuid",
      "faithfulness": 0.91,
      "relevance": 0.87,
      "precision": 0.85,
      "recall": 0.82
    }
  ],
  "page": 1,
  "total": 100
}
```

## Errors

* 401: Unauthorized
* 400: Invalid pagination params
* 500: Database error

---

# 5. GET /evaluations/aggregate

## Description

Get rolling evaluation metrics

## Authentication

Required

## Rate Limit

10 requests/min

## Response Body

```json
{
  "avg_faithfulness": 0.88,
  "avg_relevance": 0.90,
  "avg_precision": 0.84,
  "avg_recall": 0.83
}
```

## Errors

* 401: Unauthorized
* 500: Aggregation failure

---

# 6. POST /pipelines

## Description

Create a pipeline configuration

## Authentication

Required

## Rate Limit

5 requests/min

## Request Body

```json
{
  "name": "string",
  "config": {
    "retrieval_strategy": "hybrid",
    "model": "gpt-4"
  }
}
```

## Response Body

```json
{
  "pipeline_id": "uuid",
  "status": "created"
}
```

## Errors

* 400: Invalid config
* 401: Unauthorized
* 500: Creation failure

---

# 7. GET /pipelines/{id}/runs

## Description

Fetch pipeline execution history

## Authentication

Required

## Rate Limit

15 requests/min

## Response Body

```json
{
  "runs": [
    {
      "run_id": "uuid",
      "status": "completed",
      "timestamp": "ISO8601"
    }
  ]
}
```

## Errors

* 401: Unauthorized
* 404: Pipeline not found
* 500: Retrieval error

---

# 8. POST /finetune/jobs

## Description

Submit fine-tuning job

## Authentication

Required

## Rate Limit

3 requests/min

## Request Body

```json
{
  "dataset_id": "string",
  "model": "base-model-name"
}
```

## Response Body

```json
{
  "job_id": "uuid",
  "status": "submitted"
}
```

## Errors

* 400: Invalid dataset
* 401: Unauthorized
* 500: Job submission failure

---

# 9. GET /finetune/jobs/{id}

## Description

Get fine-tuning job status

## Authentication

Required

## Rate Limit

10 requests/min

## Response Body

```json
{
  "status": "running",
  "metrics": {
    "loss": 0.12,
    "accuracy": 0.93
  }
}
```

## Errors

* 401: Unauthorized
* 404: Job not found
* 500: Status fetch error

---

# 10. GET /health

## Description

System health check

## Authentication

Not Required

## Rate Limit

Unlimited

## Response

```json
{
  "status": "ok"
}
```

---

# 11. GET /metrics

## Description

Prometheus metrics endpoint

## Authentication

Optional (internal use)

## Rate Limit

Unlimited

## Response

Plain text (Prometheus format)

---
