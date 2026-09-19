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
Use only one of the displayed policy-timestep labels for each bound. Do not
copy a placeholder value from this instruction. Timestep 0 is valid only when
the failure is visibly present in the first observation. If the task merely
fails to complete by the end of the episode, locate the failure at the final
observations rather than at timestep 0.

Return only JSON in this format:
{
  "failed": true,
  "failure_start_timestep": <one displayed label>,
  "failure_end_timestep": <one displayed label>,
  "failure_type": "",
  "explanation": "",
  "confidence": 0.0
}
""".strip()


INITIAL_ONLY_RETRY_PROMPT = """
Your previous bounds were 0–0. Re-check every labeled observation. Do not use
0–0 unless the first observation itself visibly contains the failure. For a
task that only fails to complete, choose the final labeled observation(s).
Return the same JSON format and use only displayed labels.
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
    sampled_timesteps = [timestep for timestep, _ in sampled]
    content.append(
        {
            "type": "text",
            "text": (
                f"Displayed policy-timestep labels: {sampled_timesteps}.\n\n"
                f"{ROBOFAC_PROMPT}"
            ),
        }
    )

    base_url = os.environ.get("ROBOFAC_URL", "http://127.0.0.1:8000/v1")
    model_name = os.environ.get("ROBOFAC_MODEL", "MINT-SJTU/RoboFAC-7B")
    text = _request_robofac(
        base_url, model_name, [{"role": "user", "content": content}], timeout_seconds
    )
    diagnosis = parse_failure_diagnosis(text)
    _reject_invalid_bounds(diagnosis, sampled_timesteps)

    # A repeated 0--0 with generic text is usually the JSON template being
    # copied, not a localized failure. Ask once more before discarding it.
    if (
        len(sampled_timesteps) > 1
        and diagnosis["failed"]
        and diagnosis["failure_start_timestep"] == sampled_timesteps[0]
        and diagnosis["failure_end_timestep"] == sampled_timesteps[0]
    ):
        retry_messages = [
            {"role": "user", "content": content},
            {"role": "assistant", "content": text},
            {"role": "user", "content": INITIAL_ONLY_RETRY_PROMPT},
        ]
        retry_text = _request_robofac(
            base_url, model_name, retry_messages, timeout_seconds
        )
        retry_diagnosis = parse_failure_diagnosis(retry_text)
        _reject_invalid_bounds(retry_diagnosis, sampled_timesteps)
        if (
            retry_diagnosis["failed"]
            and retry_diagnosis["failure_start_timestep"] == sampled_timesteps[0]
            and retry_diagnosis["failure_end_timestep"] == sampled_timesteps[0]
        ):
            retry_diagnosis["failed"] = False
            retry_diagnosis["rejected_reason"] = "repeated_initial_only_diagnosis"
        diagnosis = retry_diagnosis
        text = retry_text

    diagnosis["sampled_timesteps"] = sampled_timesteps
    diagnosis["raw_response"] = text

    return diagnosis


def _request_robofac(base_url, model_name, messages, timeout_seconds) -> str:
    payload = json.dumps(
        {
            "model": model_name,
            "messages": messages,
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
        return response_body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"Unexpected RoboFAC response: {response_body!r}") from exc


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
        diagnosis["failure_start_timestep"], diagnosis["failure_end_timestep"] = (
            end,
            start,
        )


def _reject_invalid_bounds(
    diagnosis: dict[str, Any], sampled_timesteps: Sequence[int]
) -> None:
    try:
        _require_sampled_bounds(diagnosis, sampled_timesteps)
    except ValueError as exc:
        # Do not let one malformed VLM answer abort a long collection run or
        # silently snap an invalid value to timestep 0.
        diagnosis["failed"] = False
        diagnosis["rejected_reason"] = str(exc)
