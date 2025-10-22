from typing import Any, Dict
from utils import wacc

DEFAULT_MACRO = {"rf": 0.04, "erp": 0.05, "tax": 0.23, "kd": 0.055, "debt_ratio": 0.4}


def financing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    WACC-lite + accretion heuristic.
    If there are no finances, we use safe beta and P/E defaults.
    """
    a = (state.get("financials", {}) or {}).get("acquirer") or {"beta": 1.1, "pe": 22.0}
    t = (state.get("financials", {}) or {}).get("target") or {"pe": 15.0}
    macro = {**DEFAULT_MACRO, **(state.get("macro") or {})}

    w = wacc(beta=a.get("beta", 1.1), rf=macro["rf"], erp=macro["erp"],
             kd=macro["kd"], tax=macro["tax"], debt_ratio=macro["debt_ratio"])

    eps_effect = "accretive" if a.get("pe", 20.0) > t.get("pe", 15.0) else "dilutive"

    fin = {"wacc": round(w, 4), "eps_effect": eps_effect}
    pending = {**state.get("pending", {}), "need_financing": False, "ready_for_aggregate": True}
    return {"financing": fin, "pending": pending, "messages": [f"Financing: {fin}"]}
