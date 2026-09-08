from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import torch


def _load_retrieval_module():
    module_path = Path(__file__).with_name("retrieval.py")
    spec = importlib.util.spec_from_file_location("spatial_retrieval_test_module", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


retrieval = _load_retrieval_module()


def test_last_seen_mug_prefers_temporal_match():
    query = retrieval.RetrievalQuery(
        text="Where did I last see the mug?",
        embedding=torch.tensor([1.0, 0.0, 0.0]),
        current_position=torch.tensor([0.0, 0.0, 0.0]),
        current_time=100.0,
        task_type="temporal",
        object_ids=("mug",),
        modality_hints=("visual", "spatial"),
    )
    memories = [
        retrieval.MemoryRecord(
            id="recent_near_mug",
            embedding=torch.tensor([1.0, 0.0, 0.0]),
            position=torch.tensor([0.2, 0.0, 0.0]),
            timestamp=95.0,
            task_tags=("temporal",),
            object_ids=("mug",),
            modality="visual",
        ),
        retrieval.MemoryRecord(
            id="old_near_mug",
            embedding=torch.tensor([1.0, 0.0, 0.0]),
            position=torch.tensor([0.2, 0.0, 0.0]),
            timestamp=10.0,
            task_tags=("temporal",),
            object_ids=("mug",),
            modality="visual",
        ),
        retrieval.MemoryRecord(
            id="recent_near_plate",
            embedding=torch.tensor([0.0, 1.0, 0.0]),
            position=torch.tensor([0.1, 0.0, 0.0]),
            timestamp=99.0,
            task_tags=("temporal",),
            object_ids=("plate",),
            modality="visual",
        ),
    ]

    results = retrieval.MemoryRetriever().retrieve(query, memories, top_k=3)
    results_by_id = {result.memory.id: result for result in results}

    assert results[0].memory.id == "recent_near_mug"
    assert results[0].mode == retrieval.RetrievalMode.TEMPORAL
    assert results[0].breakdown["semantic"] > 0.99
    assert (
        results_by_id["recent_near_mug"].breakdown["temporal"]
        > results_by_id["old_near_mug"].breakdown["temporal"]
    )


def test_object_state_mode_prefers_semantically_matching_state_observation():
    query = retrieval.RetrievalQuery(
        text="Have I already opened this drawer?",
        embedding=torch.tensor([0.0, 1.0, 0.0]),
        current_position=torch.tensor([1.0, 0.0, 0.0]),
        current_time=50.0,
        task_type="object_state",
        object_ids=("drawer_1",),
        modality_hints=("visual",),
    )
    memories = [
        retrieval.MemoryRecord(
            id="drawer_1_open",
            embedding=torch.tensor([0.0, 1.0, 0.0]),
            position=torch.tensor([1.1, 0.0, 0.0]),
            timestamp=40.0,
            task_tags=("object_state",),
            object_ids=("drawer_1",),
            state={"open": True},
            modality="visual",
        ),
        retrieval.MemoryRecord(
            id="drawer_2_open",
            embedding=torch.tensor([1.0, 0.0, 0.0]),
            position=torch.tensor([1.1, 0.0, 0.0]),
            timestamp=49.0,
            task_tags=("object_state",),
            object_ids=("drawer_2",),
            state={"open": True},
            modality="visual",
        ),
        retrieval.MemoryRecord(
            id="drawer_1_unrelated_audio",
            embedding=torch.tensor([1.0, 0.0, 0.0]),
            position=torch.tensor([4.0, 0.0, 0.0]),
            timestamp=49.0,
            task_tags=("temporal",),
            object_ids=("drawer_1",),
            state={},
            modality="audio",
        ),
    ]

    results = retrieval.MemoryRetriever().retrieve(query, memories, top_k=3)

    assert results[0].memory.id == "drawer_1_open"
    assert results[0].memory.state["open"] is True
    assert results[0].mode == retrieval.RetrievalMode.OBJECT_STATE


def test_sound_query_prefers_near_time_audio_and_near_visual_observation():
    query = retrieval.RetrievalQuery(
        text="What made that sound?",
        embedding=torch.tensor([0.0, 0.0, 1.0]),
        current_position=torch.tensor([2.0, 0.0, 0.0]),
        current_time=200.0,
        task_type="temporal",
        modality_hints=("audio", "visual"),
    )
    memories = [
        retrieval.MemoryRecord(
            id="near_recent_audio",
            embedding=torch.tensor([0.0, 0.0, 1.0]),
            position=torch.tensor([2.1, 0.0, 0.0]),
            timestamp=199.0,
            task_tags=("temporal",),
            modality="audio",
        ),
        retrieval.MemoryRecord(
            id="near_recent_visual",
            embedding=torch.tensor([0.0, 0.0, 0.9]),
            position=torch.tensor([2.2, 0.0, 0.0]),
            timestamp=198.0,
            task_tags=("temporal",),
            modality="visual",
        ),
        retrieval.MemoryRecord(
            id="old_audio",
            embedding=torch.tensor([0.0, 0.0, 1.0]),
            position=torch.tensor([2.1, 0.0, 0.0]),
            timestamp=20.0,
            task_tags=("temporal",),
            modality="audio",
        ),
        retrieval.MemoryRecord(
            id="far_recent_audio",
            embedding=torch.tensor([0.0, 0.0, 1.0]),
            position=torch.tensor([20.0, 0.0, 0.0]),
            timestamp=199.0,
            task_tags=("temporal",),
            modality="audio",
        ),
    ]

    results = retrieval.MemoryRetriever().retrieve(query, memories, top_k=4)
    top_ids = [result.memory.id for result in results[:2]]

    assert results[0].memory.id == "near_recent_audio"
    assert "near_recent_visual" in top_ids
    assert results[0].mode == retrieval.RetrievalMode.TEMPORAL


def test_spatial_weights_spatial_relevance_more_than_recency():
    query = retrieval.RetrievalQuery(
        text="go to the drawer",
        embedding=torch.tensor([0.0, 1.0, 0.0]),
        current_position=torch.tensor([0.0, 0.0, 0.0]),
        current_time=100.0,
        object_ids=("drawer",),
        modality_hints=("visual", "spatial"),
    )
    memories = [
        retrieval.MemoryRecord(
            id="near_old_drawer",
            embedding=torch.tensor([0.0, 1.0, 0.0]),
            position=torch.tensor([0.1, 0.0, 0.0]),
            timestamp=0.0,
            task_tags=("spatial",),
            object_ids=("drawer",),
            modality="visual",
        ),
        retrieval.MemoryRecord(
            id="far_recent_drawer",
            embedding=torch.tensor([0.0, 1.0, 0.0]),
            position=torch.tensor([10.0, 0.0, 0.0]),
            timestamp=99.0,
            task_tags=("spatial",),
            object_ids=("drawer",),
            modality="visual",
        ),
    ]

    results = retrieval.MemoryRetriever().retrieve(query, memories, top_k=2)

    assert results[0].memory.id == "near_old_drawer"
    assert results[0].mode == retrieval.RetrievalMode.SPATIAL
    assert results[0].breakdown["spatial"] > results[1].breakdown["spatial"]
    assert results[0].breakdown["temporal"] < results[1].breakdown["temporal"]


def test_retrieval_modes_are_exactly_the_four_canonical_task_types():
    assert {mode.value for mode in retrieval.RetrievalMode} == {
        "spatial",
        "object_state",
        "temporal",
        "default",
    }


def test_bridge_placement_instructions_route_to_spatial_mode():
    router = retrieval.ManualRetrievalRouter()
    instructions = (
        "put carrot on plate",
        "stack green cube on yellow cube",
        "put eggplant in basket",
        "put spoon on tablecloth",
    )

    for instruction in instructions:
        mode, _ = router.route(retrieval.RetrievalQuery(text=instruction))
        assert mode == retrieval.RetrievalMode.SPATIAL


def test_on_and_off_only_route_to_object_state_as_state_change_phrases():
    router = retrieval.ManualRetrievalRouter()

    for instruction in ("turn on the faucet", "switch off the light"):
        mode, _ = router.route(retrieval.RetrievalQuery(text=instruction))
        assert mode == retrieval.RetrievalMode.OBJECT_STATE


def test_legacy_task_labels_map_to_canonical_modes():
    assert retrieval.RetrievalMode("navigation") == retrieval.RetrievalMode.SPATIAL
    assert (
        retrieval.RetrievalMode("semantic_spatial_recent")
        == retrieval.RetrievalMode.TEMPORAL
    )


def test_task_type_is_not_a_similarity_component():
    weights = retrieval.ManualRetrievalRouter.WEIGHTS
    assert all(not hasattr(mode_weights, "task") for mode_weights in weights.values())
    assert all(
        abs(
            mode_weights.semantic
            + mode_weights.spatial
            + mode_weights.temporal
            - 1.0
        )
        < 1e-9
        for mode_weights in weights.values()
    )

    query = retrieval.RetrievalQuery(
        text="What happened earlier?",
        embedding=torch.tensor([1.0, 0.0]),
        current_time=10.0,
        task_type="temporal",
    )
    memories = [
        retrieval.MemoryRecord(
            id="canonical_tag",
            embedding=torch.tensor([1.0, 0.0]),
            timestamp=9.0,
            task_tags=("temporal",),
        ),
        retrieval.MemoryRecord(
            id="unrelated_tag",
            embedding=torch.tensor([1.0, 0.0]),
            timestamp=9.0,
            task_tags=("spatial",),
        ),
    ]

    results = retrieval.MemoryRetriever().retrieve(query, memories, top_k=2)
    assert results[0].score == results[1].score
    assert set(results[0].breakdown) == {"semantic", "spatial", "temporal"}
    assert (
        retrieval.RetrievalMode("audio_temporal_visual")
        == retrieval.RetrievalMode.TEMPORAL
    )
