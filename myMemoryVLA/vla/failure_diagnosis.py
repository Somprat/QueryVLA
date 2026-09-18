from __future__ import annotations

import base64
import io
import json
import os
from typing import Any, Sequence
from urllib import error, request

import numpy as np
from PIL import Image


ROBOFAC_PROMPT = """
Analyze this failed robot manipulation episode. Each image is labeled with its
policy timestep. A policy timestep is one robot action decision; it is not a
video frame number or a number of seconds.

Identify the smallest timestep range in which the failure becomes observable.
Return only JSON using this schema:
{
  "failed": true,
  "failure_start_timestep": 0,
  "failure_end_timestep": 1,
  "failure_type": "",
  "explanation": "",
  "confidence": 0.0
}
""".strip()


def sample_episode_frames(
    frames: Sequence[np.ndarray], max_frames: int = 20
) -> list[tuple[int, np.ndarray]]:
    """Uniformly sample frames while preserving their policy-timestep indices."""
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
) -> dict[str, Any]:
    """Ask a RoboFAC vLLM server to locate the failure in policy timesteps."""
    sampled = sample_episode_frames(frames, max_frames=max_frames)
    if not sampled:
        raise ValueError("Cannot diagnose a failed episode without frames")

    content: list[dict[str, Any]] = []
    for timestep, frame in sampled:
        content.append({"type": "text", "text": f"Policy timestep {timestep}"})
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": _frame_data_url(frame), "detail": "low"},
            }
        )
    content.append({"type": "text", "text": ROBOFAC_PROMPT})

    base_url = os.environ.get("ROBOFAC_URL", "http://127.0.0.1:8000/v1")
    model_name = os.environ.get("ROBOFAC_MODEL", "MINT-SJTU/RoboFAC-7B")
    payload = json.dumps(
        {
            "model": model_name,
            "messages": [{"role": "user", "content": content}],
            "response_format": {"type": "text"},
            "temperature": 0,
        }
    ).encode("utf-8")
    http_request = request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            response_body = json.loads(response.read().decode("utf-8"))
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            "RoboFAC diagnosis failed. Start its vLLM OpenAI-compatible server "
            "or set ROBOFAC_URL to an existing server."
        ) from exc

    try:
        text = response_body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"Unexpected RoboFAC response: {response_body!r}") from exc

    diagnosis = parse_failure_diagnosis(text)
    sampled_timesteps = [timestep for timestep, _ in sampled]
    diagnosis["sampled_timesteps"] = sampled_timesteps
    diagnosis["raw_response"] = text

    if diagnosis["failed"]:
        diagnosis["failure_start_timestep"] = _nearest_sampled_timestep(
            diagnosis["failure_start_timestep"], sampled_timesteps
        )
        diagnosis["failure_end_timestep"] = _nearest_sampled_timestep(
            diagnosis["failure_end_timestep"], sampled_timesteps
        )
        if diagnosis["failure_start_timestep"] > diagnosis["failure_end_timestep"]:
            diagnosis["failure_start_timestep"], diagnosis["failure_end_timestep"] = (
                diagnosis["failure_end_timestep"],
                diagnosis["failure_start_timestep"],
            )

    return diagnosis


def parse_failure_diagnosis(text: str) -> dict[str, Any]:
    """Extract the JSON object from a RoboFAC response."""
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"RoboFAC did not return JSON: {text!r}")
    diagnosis = json.loads(text[start : end + 1])

    failed = diagnosis.get("failed")
    if isinstance(failed, str):
        failed = failed.strip().lower() == "true"
    if not isinstance(failed, bool):
        raise ValueError("RoboFAC diagnosis is missing boolean field 'failed'")
    diagnosis["failed"] = failed

    if failed:
        start_timestep = diagnosis.get(
            "failure_start_timestep", diagnosis.get("failure_start_frame")
        )
        end_timestep = diagnosis.get(
            "failure_end_timestep", diagnosis.get("failure_end_frame")
        )
        if start_timestep is None or end_timestep is None:
            raise ValueError("RoboFAC diagnosis is missing failure timestep bounds")
        diagnosis["failure_start_timestep"] = int(start_timestep)
        diagnosis["failure_end_timestep"] = int(end_timestep)

    return diagnosis


def _nearest_sampled_timestep(value: int, sampled_timesteps: Sequence[int]) -> int:
    return min(sampled_timesteps, key=lambda timestep: abs(timestep - int(value)))
