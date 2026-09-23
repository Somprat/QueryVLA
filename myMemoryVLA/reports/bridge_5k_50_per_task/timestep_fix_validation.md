# Timestep diagnosis reconciliation — 2026-09-19

The original 102 saved raw responses all reported 0–1, matching the numeric example in the prompt. Nearest-sample rounding converted both endpoints to 0. This strongly suggests template copying; it does not prove the underlying model cause.

The reconciled code removes numeric examples, constrains endpoints to exact sampled labels, passes the task instruction, and restores bounded retries and RoboFACDiagnosisError for collector compatibility. Invalid bounds, missing evidence, and repeated initial-only windows are diagnosis errors, not confirmed memories or model-negative responses. The initial-only guard is conservative: genuinely immediate failures also require separate review. Original bank data is unchanged.

Validation: nine CPU recovery tests passed, plus five existing pipeline test functions (invoked directly because pytest is not installed). The integration test also checks task-instruction propagation. git diff --check passed.

Two live server requests used existing evaluation videos, not the 200-attempt collection. Returned video-frame labels were 44–120 and 13–13; these are not verified policy-timestep ground truth. Both responses returned failed=false while describing failures, and both would be skipped by collection. Descriptions still misidentified objects. Therefore these checks verify API compatibility and absence of automatic 0–0 rounding, NOT reliable visual localization. See timestep_fix_live_checks.json for the exact responses and video paths.

Before rebuilding the training bank, validate diagnoses against manually reviewed training rollouts. Existing 0–2 feature summaries cannot recover the omitted trajectory windows; rebuilding requires original observations and features or rerunning rollouts.
