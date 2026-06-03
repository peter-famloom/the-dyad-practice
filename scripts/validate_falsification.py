#!/usr/bin/env python3
# Schema validator for the inter-dyad falsification channel (PROVISIONAL — see falsification/CONTRACT.md).
# Authored by dyad-steward, proposed to the Commons; a CI workflow on PRs to falsification/ is a deferred
# follow-up (Founding-gated). Mirrors validate_registry.py.
#
# Enforces the contract (falsification/CONTRACT.md) on a falsification/ ledger:
#   falsification/<claim_id>/fr.yaml
#   falsification/<claim_id>/responses/<responder_dyad_id>.yaml   (append-only; verdict immutable)
#   falsification/<claim_id>/disposition.yaml                     (optional until disposed)
# Mirrors validate_registry.py's no-framework style. The contract's HONESTY rules (genuine non-eristic
# attack) are NOT code-enforceable; this enforces the SCHEMA so echo is detectable (I4/I9), not policed.
import os
import sys

import yaml

VERDICTS = {"REFUTED", "SURVIVED-MY-ATTACK", "NEEDS-SCOPING"}
ATTACK_TYPES = {"counter-evidence", "confound", "reinterpretation", "scope-challenge"}
CLAIM_TYPES = {"denial", "affirmation", "design-model"}
GROUNDING = {"mechanism-grounded", "generic"}
DISPOSITIONS = {"accept-refutation", "contest-with-grounds", "revise"}
OUTCOMES = {"strengthened", "revised", "retracted"}
AXES = {"model", "human", "corpus", "dyad"}

FR_REQ = {"claim_id", "claim_type", "claim", "evidence", "falsification_target", "domain",
          "submitter_dyad_id", "submitter_model", "submitter_human", "submitted_at"}
RESP_REQ = {"responder_dyad_id", "responder_model", "responder_human", "divergent_axes", "grounding",
            "target_claim_hash", "responded_at", "verdict", "attack_type", "attack", "confound_surfaced"}
DISP_REQ = {"disposes_claim_id", "disposing_dyad_id", "disposed_verdicts", "disposed_at",
            "submitter_disposition", "outcome"}


def _load(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("root must be a mapping")
    return data


def _need(data, req, path):
    missing = req - set(data)
    if missing:
        print(f"FAIL {path}: missing fields {missing}")
        return False
    return True


def _enum(data, field, allowed, path):
    if data.get(field) not in allowed:
        print(f"FAIL {path}: {field}={data.get(field)!r} not in {allowed}")
        return False
    return True


def validate_fr(path):
    try:
        d = _load(path)
    except Exception as e:
        print(f"FAIL {path}: {e}")
        return False
    ok = _need(d, FR_REQ, path)
    ok &= _enum(d, "claim_type", CLAIM_TYPES, path)
    if not str(d.get("falsification_target", "")).strip():  # I8 — reject unfalsifiable
        print(f"FAIL {path}: falsification_target is required and non-empty (I8)")
        ok = False
    if ok:
        print(f"PASS {path}")
    return ok


def validate_response(path, submitter_id=None):
    try:
        d = _load(path)
    except Exception as e:
        print(f"FAIL {path}: {e}")
        return False
    ok = _need(d, RESP_REQ, path)
    ok &= _enum(d, "verdict", VERDICTS, path)
    ok &= _enum(d, "attack_type", ATTACK_TYPES, path)
    ok &= _enum(d, "grounding", GROUNDING, path)
    axes = d.get("divergent_axes") or []
    if not isinstance(axes, list) or any(a not in AXES for a in axes):
        print(f"FAIL {path}: divergent_axes must be a list ⊆ {AXES} (the §J weighting key)")
        ok = False
    if submitter_id and d.get("responder_dyad_id") == submitter_id:  # I5 — no self-response
        print(f"FAIL {path}: responder_dyad_id == submitter ({submitter_id}) — self-response (I5)")
        ok = False
    if ok:
        print(f"PASS {path}")
    return ok


def validate_disposition(path):
    try:
        d = _load(path)
    except Exception as e:
        print(f"FAIL {path}: {e}")
        return False
    ok = _need(d, DISP_REQ, path)
    ok &= _enum(d, "submitter_disposition", DISPOSITIONS, path)
    ok &= _enum(d, "outcome", OUTCOMES, path)
    if ok:
        print(f"PASS {path}")
    return ok


def validate_claim_dir(claim_dir):
    """A full ledger entry: fr (required) + responses (≥0, append-only) + disposition (optional)."""
    fr = os.path.join(claim_dir, "fr.yaml")
    if not os.path.isfile(fr):
        print(f"FAIL {claim_dir}: no fr.yaml")
        return False
    ok = validate_fr(fr)
    try:
        submitter = _load(fr).get("submitter_dyad_id")
    except Exception:
        submitter = None
    rdir = os.path.join(claim_dir, "responses")
    if os.path.isdir(rdir):
        for r in sorted(os.listdir(rdir)):
            if r.endswith((".yaml", ".yml")):
                ok &= validate_response(os.path.join(rdir, r), submitter)
    disp = os.path.join(claim_dir, "disposition.yaml")
    if os.path.isfile(disp):
        ok &= validate_disposition(disp)
    return ok


def main(argv):
    root = argv[1] if len(argv) > 1 else "falsification"
    if not os.path.isdir(root):
        print(f"Error: ledger dir {root} not found.")
        sys.exit(1)
    all_ok = True
    entries = [d for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d))]
    if not entries:
        print(f"No claim entries in {root}/")
        sys.exit(0)
    for d in entries:
        all_ok &= validate_claim_dir(os.path.join(root, d))
    print("All falsification records valid." if all_ok else "Validation failed.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main(sys.argv)
