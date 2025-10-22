from typing import Any, Dict, List, TypedDict, Annotated
import operator

class MAState(TypedDict, total=False):
    messages: Annotated[List[Any], operator.add]
    acquirer: Dict[str, Any]
    target: Dict[str, Any]
    market: Dict[str, Any]
    financials: Dict[str, Any]
    valuation: Dict[str, Any]
    synergy: Dict[str, Any]
    regulatory: Dict[str, Any]
    financing: Dict[str, Any]
    integration: Dict[str, Any]
    score: Dict[str, Any]
    company_info: Dict[str, Any]
    pending: Dict[str, Any]

def intake_node(state: MAState) -> MAState:
    acq = state.get("acquirer") or {}
    tgt = state.get("target") or {}
    market = state.get("market") or {}

    return {
        "acquirer": acq,
        "target": tgt,
        "market": market,
        "pending": {
            "need_company_info": True,
            "need_regulatory": True,
            "need_financing": True,
            "ready_for_aggregate": False,
        },
        "messages": [f"Intake OK: acquirer={acq['id']} target={tgt['id']}"],
    }