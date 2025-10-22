from typing import Any, Dict
from utils import score_map


def aggregate_score_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summary scoring based on simple standards.
    There is no Valuation here (demo), the basis is regulatory + financing + integration (mock).
    """
    # Regulatory
    rmap = {"low": 1.0, "moderate": 0.6, "elevated": 0.4, "high": 0.2}
    reg_score = score_map(state.get("regulatory", {}).get("risk", "moderate"), rmap, 0.6)

    # Financing
    fmap = {"accretive": 0.8, "neutral": 0.6, "dilutive": 0.3}
    fin_score = score_map(state.get("financing", {}).get("eps_effect", "neutral"), fmap, 0.6)

    # Integration (mock): TODO: replace with real node
    integ_score = 0.6

    score = 0.25 * reg_score + 0.60 * fin_score + 0.15 * integ_score
    verdict = "Go" if score >= 0.6 else ("Borderline" if score >= 0.5 else "No-Go")

    result = {"value": round(score, 3), "verdict": verdict,
              "contrib": {"regulatory": reg_score, "financing": fin_score, "integration": integ_score}}

    return {"score": result, "messages": [f"Aggregate score: {result}"]}
