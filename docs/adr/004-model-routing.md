# ADR 004: Model Routing Strategy

## Context

NeuroFlow must decide which LLM to use for each query to balance:

* Cost
* Latency
* Capability
* Domain specialization

Available model tiers:

* Small models (fast, cheap)
* Medium models (balanced)
* Large models (high accuracy, expensive)

## Decision

We implement a **dynamic model routing system** based on query classification.

## Routing Factors

* Query complexity
* Required reasoning depth
* Domain specificity
* Latency sensitivity
* Cost constraints

## Routing Matrix

| Query Type                       | Model Tier         | Reason               |
| -------------------------------- | ------------------ | -------------------- |
| Simple factual queries           | Small model        | Low cost, fast       |
| Basic RAG queries                | Medium model       | Balanced performance |
| Complex reasoning                | Large model        | High accuracy needed |
| Domain-specific (medical, legal) | Large / fine-tuned | Precision critical   |
| Conversational / follow-ups      | Medium model       | Context handling     |

## Consequences

### Positive

* Cost optimization
* Improved latency for simple queries
* High accuracy for complex tasks
* Efficient resource utilization

### Negative

* Increased system complexity
* Risk of misclassification of queries
* Requires continuous tuning

### Failure Modes

* Routing complex queries to weak models
* Overusing expensive models unnecessarily

### Mitigation Strategies

* Confidence scoring for routing decisions
* Fallback mechanism to higher-tier models
* Continuous evaluation of routing performance
* Feedback loop from evaluation subsystem

### Trade-offs

Static routing is simple but inefficient.
Dynamic routing improves performance but adds complexity.

---
