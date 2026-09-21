from __future__ import annotations

import base64
import io
import json
import math
import os
import time
from typing import Any, Sequence
from urllib import error, request

import numpy as np
from PIL import Image


class RoboFACDiagnosisError(RuntimeError):
    """Diagnosis failed after bounded retries; do not store this episode."""


ROBOFAC_PROMPT = """
Analyze this robot manipulation episode. Each image is labeled with its policy
timestep (one robot action decision, not seconds or an image ordinal).
The environment reported failure, but decide whether the images show an
observable failure. Describe the visible object and gripper behavior before
selecting the bounds. An initial approach before contact is not a failed grasp.
Identify the smallest range in which the failure is observable. Both endpoints
must be displayed timestep labels. Use the initial observation only if failure
is already visible there. If only non-completion is visible, use the final
observations. If you cannot locate an observable failure, set failed to false.
Return JSON with failed (boolean), explanation (visible evidence), failure_type
(short phrase), failure_start_timestep and failure_end_timestep (ordered integer
labels), and confidence (number between zero and one). Do not invent evidence.
""".strip()

INITIAL_ONLY_RETRY_PROMPT = """
The previous answer placed the entire failure in the initial observation.
Re-check the sequence and describe the visible evidence for the selected bounds.
An initial approach before contact is not a failed grasp. Use only displayed
labels. If you cannot locate the failure, set failed to false.
""".strip()


def sample_episode_frames(
    frames: Sequence[np.ndarray], max_frames: int = 20
) -> list[tuple[int, np.ndarray]]:
    """Uniformly sample frames while preserving their policy-timestep indices."""
    if max_frames < 1:
        raise ValueError("max_frames must be positive")
    if len(frames) == 0:
        return []
    sample_count = min(len(frames), max_frames)
    indices = np.linspace(0, len(frames) - 1, sample_count).round().astype(int)
    return [(int(index), np.asarray(frames[index])) for index in indices]


def _frame_data_url(frame: np.ndarray) -> str:
    image = Image.fromarray(np.asarray(frame, dtype=np.uint8)).convert("RGB")
    image.thumbnail((512, 512))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def diagnose_failure_with_robofac(
    frames: Sequence[np.ndarray],
    *,
    max_frames: int = 20,
    timeout_seconds: float = 300.0,
    max_attempts: int = 3,
    task_instruction: str | None = None,
) -> dict[str, Any]:
    """Locate failure using exact sampled labels, with bounded recovery retries.

    Repeated initial-only windows are conservatively treated as diagnosis errors,
    not successful rollouts or confirmed failures. No timestamps are rounded.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    sampled = sample_episode_frames(frames, max_frames=max_frames)
    if not sampled:
        raise ValueError("Cannot diagnose a failed episode without frames")
    sampled_timesteps = [timestep for timestep, _ in sampled]
    content: list[dict[str, Any]] = []
    for timestep, frame in sampled:
        content.append({"type": "text", "text": f"Policy timestep {timestep}"})
        content.append({
            "type": "image_url",
            "image_url": {"url": _frame_data_url(frame), "detail": "low"},
        })
    prompt = f"{ROBOFAC_PROMPT}\nDisplayed timestep labels: {sampled_timesteps}."
    if task_instruction:
        prompt += f"\nTask instruction: {task_instruction}"
    content.append({"type": "text", "text": prompt})
    messages = [{"role": "user", "content": content}]

    # use http because we are only using RoboFAC for evaluation anyway. It also avoids the dependencies conflict
    base_url = os.environ.get("ROBOFAC_URL", "http://127.0.0.1:8000/v1")
    model_name = os.environ.get("ROBOFAC_MODEL", "MINT-SJTU/RoboFAC-7B")
    last_error = None
    responses = []
    for attempt in range(max_attempts):
        try:
            text = _request_robofac(
                base_url, model_name, messages, timeout_seconds,
                sampled_timesteps=sampled_timesteps, attempt=attempt,
            )
            responses.append(text)
            diagnosis = parse_failure_diagnosis(text)
            _require_sampled_bounds(diagnosis, sampled_timesteps)
            if diagnosis["failed"]:
                for field in ("failure_type", "explanation"):
                    value = diagnosis.get(field)
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(f"Confirmed failure is missing {field}")
                confidence = diagnosis.get("confidence")
                if (type(confidence) not in (int, float)
                        or not math.isfinite(confidence) or not 0 <= confidence <= 1):
                    raise ValueError("Confidence must be a finite number between zero and one")
                if (len(sampled_timesteps) > 1
                        and diagnosis["failure_start_timestep"] == sampled_timesteps[0]
                        and diagnosis["failure_end_timestep"] == sampled_timesteps[0]):
                    # Keep one correction turn, not an ever-growing image history.
                    messages = [
                        {"role": "user", "content": content},
                        {"role": "assistant", "content": text},
                        {"role": "user", "content": INITIAL_ONLY_RETRY_PROMPT},
                    ]
                    raise ValueError("Initial-only failure window needs verification")
            diagnosis["sampled_timesteps"] = sampled_timesteps
            diagnosis["raw_response"] = text
            diagnosis["raw_responses"] = responses
            diagnosis["task_instruction"] = task_instruction
            diagnosis["diagnosis_version"] = 2
            return diagnosis
        except (error.URLError, TimeoutError, ValueError, KeyError, IndexError, TypeError) as exc:
            last_error = exc
            if attempt + 1 < max_attempts:
                print(
                    f"RoboFAC diagnosis retry {attempt + 1}/{max_attempts}: {str(exc)[:200]}",
                    flush=True,
                )
                time.sleep(1)
    failure = RoboFACDiagnosisError(
        f"RoboFAC diagnosis failed after {max_attempts} attempts: {str(last_error)[:200]}"
    )
    failure.raw_responses = responses
    raise failure from last_error


def _request_robofac(
    base_url, model_name, messages, timeout_seconds, *, sampled_timesteps, attempt
) -> str:
    properties = {
        "failed": {"type": "boolean"},
        "explanation": {"type": "string", "maxLength": 800},
        "failure_type": {"type": "string", "maxLength": 80},
        "failure_start_timestep": {"type": "integer", "enum": sampled_timesteps},
        "failure_end_timestep": {"type": "integer", "enum": sampled_timesteps},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    }
    payload = {
        "model": model_name,
        "messages": messages,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "failure_diagnosis", "strict": True,
                "schema": {
                    "type": "object", "properties": properties,
                    "required": list(properties), "additionalProperties": False,
                },
            },
        },
        "temperature": 0 if attempt == 0 else 0.2,
        "seed": attempt,
        "max_tokens": 768,
    }
    http_request = request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with request.urlopen(http_request, timeout=timeout_seconds) as response:
        response_body = json.loads(response.read().decode("utf-8"))
    choice = response_body["choices"][0]
    if choice.get("finish_reason") == "length":
        raise ValueError("RoboFAC exhausted its output token limit")
    text = choice["message"]["content"]
    if not isinstance(text, str):
        raise ValueError("RoboFAC returned no text content")
    return text


def parse_failure_diagnosis(text: str) -> dict[str, Any]:
    """Extract JSON without silently coercing invalid bounds or booleans."""
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"RoboFAC did not return JSON: {text[:200]!r}")
    diagnosis = json.loads(text[start : end + 1])
    if not isinstance(diagnosis, dict):
        raise ValueError("RoboFAC diagnosis must be an object")
    failed = diagnosis.get("failed")
    if isinstance(failed, str) and failed.strip().lower() in {"true", "false"}:
        failed = failed.strip().lower() == "true"
    if not isinstance(failed, bool):
        raise ValueError("RoboFAC diagnosis is missing boolean field 'failed'")
    diagnosis["failed"] = failed
    if failed:
        for field in ("failure_start_timestep", "failure_end_timestep"):
            value = diagnosis.get(field)
            if type(value) is not int:
                raise ValueError("Failure timestep bounds must be integer policy labels")
    return diagnosis


def _require_sampled_bounds(
    diagnosis: dict[str, Any], sampled_timesteps: Sequence[int]
) -> None:
    if not diagnosis["failed"]:
        return
    start = diagnosis["failure_start_timestep"]
    end = diagnosis["failure_end_timestep"]
    if start not in sampled_timesteps or end not in sampled_timesteps:
        raise ValueError(
            "RoboFAC must return exact displayed timestep labels; got "
            f"{start}--{end}, expected one of {list(sampled_timesteps)}"
        )
    if start > end:
        raise ValueError("Failure timestep bounds are reversed")
