from typing import Any, Dict
from utils import hhi


def regulatory_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    HHI-lite: take shares_pre/post from state.market, or use a simple heuristic.
    """
    market = state.get("market", {})
    shares_pre = market.get("shares_pre") or [0.28, 0.22, 0.18, 0.12, 0.20]
    shares_post = market.get("shares_post") or [0.50, 0.18, 0.12, 0.10, 0.10]

    h_pre, h_post = hhi(shares_pre), hhi(shares_post)
    delta = h_post - h_pre

    if h_post < 1500:
        risk = "low"
    elif h_post < 2500:
        risk = "moderate" if delta < 200 else "elevated"
    else:
        risk = "high" if delta >= 200 else "moderate"

    reg = {"hhi_pre": h_pre, "hhi_post": h_post, "delta": delta, "risk": risk}
    pending = {**state.get("pending", {}), "need_regulatory": False}
    return {"regulatory": reg, "pending": pending, "messages": [f"Regulatory: {reg}"]}
