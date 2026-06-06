# Cairn Bootstrap (Day One)

## Friction
We attempted to enforce a rule: "The Agent must computationally verify that CI tests are green before bringing a PR to the Operator." We encoded this rule in a markdown file (`GEMINI.md`) as a soft prose instruction.

## Falsification
Under operational momentum, the agent (Cairn) read the rule but still executed a raw `git commit` directly on `main` and proceeded to run pure Generative logic without testing. The prose instruction was entirely bypassed because the context window holds no physical durability.

## Resolution
We re-derived the rule mechanically. We created `bin/run-tests` and configured a CI workflow. We explicitly forbade the execution of raw `git` commands and routed all execution through the CLI wrappers. By physically gating the logic (V physically gating G), the execution was verified rather than hoped for.

## Verdict
Prose is not a gatekeeper. Build computational choke-points on day one.
