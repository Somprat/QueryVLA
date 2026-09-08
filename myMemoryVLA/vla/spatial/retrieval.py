from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import exp
import re
from typing import Any, Mapping, Optional, Protocol, Sequence

import torch
import torch.nn.functional as F


class RetrievalMode(str, Enum):
    DEFAULT = "default"
    SPATIAL = "spatial"
    OBJECT_STATE = "object_state"
    TEMPORAL = "temporal"

    @classmethod
    def _missing_(cls, value):
        """Map names emitted by older configs to the four canonical modes."""
        aliases = {
            "navigation": cls.SPATIAL,
            "navigate": cls.SPATIAL,
            "semantic_spatial_recent": cls.TEMPORAL,
            "audio_temporal_visual": cls.TEMPORAL,
            "audio_temporal": cls.TEMPORAL,
            "recent": cls.TEMPORAL,
            "state": cls.OBJECT_STATE,
        }
        return aliases.get(str(value).lower())


# dataclass is a normal class but was automatically equipped with init, __repr__ and __eq__
# only thinkgs we need to do is specifying each variable
@dataclass
class MemoryRecord:
    id: str
    text: str = ""
    embedding: Optional[torch.Tensor] = None
    # embedding is the embedding of semantic feature that the model decides to store in the long term memory
    position: Optional[torch.Tensor] = None
    timestamp: Optional[float] = None
    # Sequence[str] = takes in a list/tuple of str
    # field() adds some special thing to that argumnet
    # in this case, default_factory=tuple means that if the value is not provided, it will initialized a blank tuple
    task_tags: Sequence[str] = field(default_factory=tuple)
    # we don't do Optional[Sequence][str].
    # That means if we don't provide the argument, it becomes None which is bad
    # we want it to be a blank tuple if it's not provided
    object_ids: Sequence[str] = field(default_factory=tuple)
    state: Mapping[str, Any] = field(default_factory=dict)
    modality: str = "unknown"


@dataclass
class RetrievalQuery:
    text: str
    embedding: Optional[torch.Tensor] = None
    current_position: Optional[torch.Tensor] = None
    current_time: Optional[float] = None
    task_type: Optional[str] = None
    modality_hints: Sequence[str] = field(default_factory=tuple)
    object_ids: Sequence[str] = field(default_factory=tuple)



# doesn't allowed these weights to be changed
@dataclass(frozen=True)
class RetrievalWeights:
    semantic: float = 0.40
    spatial: float = 0.30
    temporal: float = 0.30


@dataclass
class RetrievalResult:
    # the info about each aspect: posistion, emebdding, texts, etc.
    memory: MemoryRecord
    # retrieval score: higher = more relevant
    score: float
    breakdown: Mapping[str, float]
    # break down shows the various of info
    # {
#     "text_similarity": 0.72,
#     "spatial_match": 0.15,
#     "recency": 0.08
# }
    mode: RetrievalMode


class QueryModeClassifier(Protocol):
    """Optional learned or LLM-backed router.

    Implement this protocol later if you want a language model, small classifier,
    or task planner to choose retrieval modes instead of relying on heuristics.
    """

    def classify(self, query: RetrievalQuery) -> Optional[RetrievalMode]:
        ...

# comparing query(what the robot needs) vs the memory
def semantic_score(query: RetrievalQuery, memory: MemoryRecord) -> float:
    if query.embedding is None or memory.embedding is None:
        return 0.0

    # cosine simlarity expects float
    # flatten to make it a 1d array tensor
    query_embedding = query.embedding.float().flatten()
    memory_embedding = memory.embedding.float().flatten()
    if query_embedding.numel() != memory_embedding.numel():
        return 0.0

    score = F.cosine_similarity(query_embedding, memory_embedding, dim=0)
    return _clamp01(float(score.item()))


def spatial_score(
    query: RetrievalQuery,
    memory: MemoryRecord,
    spatial_scale: float = 2.0,
) -> float:
    if query.current_position is None or memory.position is None:
        return 0.0

    # do the same preprocessing
    query_position = query.current_position.float().flatten()
    memory_position = memory.position.float().flatten()
    if query_position.numel() != memory_position.numel():
        return 0.0

    # find the euclidean distance
    distance = torch.linalg.norm(query_position - memory_position).item()
    # the exp thing just mean small distance = higher score
    #  spatial scale control the influence of the distance on the score. more = less distance influence
    return exp(-distance / max(spatial_scale, 1e-6))



def temporal_score(
    query: RetrievalQuery,
    memory: MemoryRecord,
    temporal_scale: float = 60.0,
) -> float:
    if query.current_time is None or memory.timestamp is None:
        return 0.0

    # temporal score just find the difference
    age = abs(query.current_time - memory.timestamp)
    return exp(-age / max(temporal_scale, 1e-6))


MANUAL_TASK_LABELS = {
    "pick up the object and move it to a goal position.": "spatial",
    "pick up a designated object from a clutter of objects.": "object_state",
    "turn on the faucet by rotating a designated handle.": "default",
    "insert a designated object into the corresponding slot on a board.": "spatial",
    "plug the charger into the wall socket.": "spatial",
    "stack the red cube on top of the green cube.": "spatial",
    "insert the peg into the horizontal hole in a box.": "spatial",
    "pick up the red cube and move it to a goal position.": "spatial",
    "lift up the red cube by 0.2 meters.": "spatial"
}

class ManualRetrievalRouter:
    """Use the task category to select semantic/spatial/temporal weights."""

    # create dictionary pairs of the task's name and its optimal weights
    WEIGHTS = {
        RetrievalMode.DEFAULT: RetrievalWeights(),
        RetrievalMode.TEMPORAL: RetrievalWeights(
            semantic=0.30,
            spatial=0.20,
            temporal=0.50,
        ),
        RetrievalMode.OBJECT_STATE: RetrievalWeights(
            semantic=0.50,
            spatial=0.20,
            temporal=0.30,
        ),
        RetrievalMode.SPATIAL: RetrievalWeights(
            semantic=0.30,
            spatial=0.50,
            temporal=0.20,
        ),
    }

    # store the key of the last dict as its value: easy for conversion from task_type to mode
    TASK_TYPE_TO_MODE = {
        "spatial": RetrievalMode.SPATIAL,
        "navigation": RetrievalMode.SPATIAL,
        "navigate": RetrievalMode.SPATIAL,
        "object_state": RetrievalMode.OBJECT_STATE,
        "state": RetrievalMode.OBJECT_STATE,
        "temporal": RetrievalMode.TEMPORAL,
        "audio_temporal_visual": RetrievalMode.TEMPORAL,
        "audio_temporal": RetrievalMode.TEMPORAL,
        "semantic_spatial_recent": RetrievalMode.TEMPORAL,
        "recent": RetrievalMode.TEMPORAL,
    }

    SPATIAL_TERMS = (
        "go to",
        "navigate",
        "where is",
        "find",
        "return to",
        "pick up",
        "put",
        "place",
        "stack",
        "insert",
        "plug",
        "move",
        "lift",
    )
    TEMPORAL_TERMS = ("last seen", "recent", "before", "earlier", "previously")
    STATE_TERMS = (
        "state",
        "open",
        "closed",
        "turn on",
        "turn off",
        "switch on",
        "switch off",
        "moved",
        "changed",
    )

    # classify each query into different modes
    def __init__(self, classifier: Optional[QueryModeClassifier] = None) -> None:
        self.classifier = classifier

    # return the query's mode and its weight that we set up there
    def route(self, query: RetrievalQuery) -> tuple[RetrievalMode, RetrievalWeights]:
        if self.classifier is not None:
            # optional if we have classifier
            classified_mode = self.classifier.classify(query)
            # self.classifier might say I dont' know
            if classified_mode is not None:
                return classified_mode, self.WEIGHTS[classified_mode]


        mode = self._mode_from_task_type(query) or self._mode_from_text(query.text)
        return mode, self.WEIGHTS[mode]



    # both these functuons' end goals are modes
    def _mode_from_task_type(self, query: RetrievalQuery) -> Optional[RetrievalMode]:
        if query.task_type is None:
            return None
        # input the query's task type (key of the TASK_TYPE_TO_MODE dictionary) to get the mode
        # Each mode is a dictionary that stores weight of the tasks
        return self.TASK_TYPE_TO_MODE.get(query.task_type.lower())

    def _mode_from_text(self, text: str) -> RetrievalMode:
        normalized = text.lower()

        def contains_any(terms: Sequence[str]) -> bool:
            return any(
                re.search(rf"\b{re.escape(term)}\b", normalized) is not None
                for term in terms
            )

        if contains_any(self.SPATIAL_TERMS):
            return RetrievalMode.SPATIAL
        if contains_any(self.TEMPORAL_TERMS):
            return RetrievalMode.TEMPORAL
        if contains_any(self.STATE_TERMS):
            return RetrievalMode.OBJECT_STATE

        return RetrievalMode.DEFAULT


class MemoryRetriever:
    def __init__(
        self,
        router: Optional[ManualRetrievalRouter] = None,
        spatial_scale: float = 2.0,
        temporal_scale: float = 60.0,
    ) -> None:
        self.router = router or ManualRetrievalRouter()
        self.spatial_scale = spatial_scale
        self.temporal_scale = temporal_scale

    def retrieve(
        self,
        query: RetrievalQuery,
        memories: Sequence[MemoryRecord],
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        # weights here is the RetrievalWeights data class
        mode, weights = self.router.route(query)
        results = []
        # rert
        for memory in memories:
            semantic = semantic_score(query, memory)
            spatial = spatial_score(query, memory, spatial_scale=self.spatial_scale)
            temporal = temporal_score(query, memory, temporal_scale=self.temporal_scale)
            # Task type selects the weight profile; it is not itself a
            # similarity component.
            total = (
                weights.semantic * semantic
                + weights.spatial * spatial
                + weights.temporal * temporal
            )
            # at the end, append memory, score, breakdown which is just some info and mode
            results.append(
                RetrievalResult(
                    memory=memory,
                    score=total,
                    breakdown={
                        "semantic": semantic,
                        "spatial": spatial,
                        "temporal": temporal,
                    },
                    mode=mode,
                )
            )
        #sorting the result by scores which is the total variable with is the sum of ...
        results.sort(key=lambda result: result.score, reverse=True)
        # only return the top_k with the most total
        return results[:top_k]
    

# Keep the semantic score between 0 and 1.
def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))
