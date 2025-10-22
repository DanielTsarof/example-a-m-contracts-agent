from typing import Any, Dict
from langgraph.types import interrupt


def human_approval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "approve": "Confirm final recommendation?",
        "verdict": state.get("score", {}).get("verdict"),
        "score": state.get("score", {}).get("value"),
    }
    ok = interrupt(payload)
    return {"score": {**state.get("score", {}), "human_approved": bool(ok)}}
