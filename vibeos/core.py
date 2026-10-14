"""Conservative, deterministic workflow-mode selection."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Assessment:
    mode: str
    reasons: tuple[str, ...]


def assess(risk: str = "medium", scope: str = "medium",
           uncertainty: str = "medium", reversibility: str = "moderate") -> Assessment:
    allowed = {
        "risk": {"low", "medium", "high"},
        "scope": {"small", "medium", "large"},
        "uncertainty": {"low", "medium", "high"},
        "reversibility": {"easy", "moderate", "hard"},
    }
    values = locals()
    for field, accepted in allowed.items():
        if values[field] not in accepted:
            raise ValueError(f"Invalid {field}: {values[field]}; expected {sorted(accepted)}")

    deep_reasons = []
    if risk == "high":
        deep_reasons.append("high consequence/security risk")
    if reversibility == "hard":
        deep_reasons.append("hard-to-reverse changes")
    if uncertainty == "high":
        deep_reasons.append("high uncertainty")
    if scope == "large":
        deep_reasons.append("large cross-cutting scope")
    if deep_reasons:
        return Assessment("DEEP", tuple(deep_reasons))

    if risk == "low" and scope == "small" and uncertainty == "low" and reversibility == "easy":
        return Assessment("QUICK", ("low-risk, small, well-understood, reversible change",))
    return Assessment("STANDARD", ("default for nontrivial or partially uncertain changes",))
