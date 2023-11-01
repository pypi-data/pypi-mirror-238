from enum import Enum


class Scorers(str, Enum):
    toxicity = "toxicity"
    factuality = "factuality"
    correctness = "factuality"
    groundedness = "groundedness"
    context_adherence = "groundedness"
    pii = "pii"
    latency = "latency"
    context_relevance = "context_relevance"
    sexist = "sexist"
    tone = "tone"
