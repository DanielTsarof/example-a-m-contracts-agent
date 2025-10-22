from typing import Any, Dict

def company_info_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stub: simulates getting a text profile of companies (TODO: later replace it with a database)
    """
    acq_id = state.get("acquirer", {}).get("id", "ACQ")
    tgt_id = state.get("target", {}).get("id", "TGT")

    info = {
        "acquirer": {
            "id": acq_id,
            "summary": f"{acq_id}: diversified operator with stable margins (stub).",
            "segments": ["Segment A", "Segment B"],
            "geo": ["NA", "EU"],
        },
        "target": {
            "id": tgt_id,
            "summary": f"{tgt_id}: niche player with growth optionality (stub).",
            "segments": ["Niche X"],
            "geo": ["EU"],
        },
    }

    # снимаем флаг ожидания company_info
    pending = {**state.get("pending", {}), "need_company_info": False}
    return {"company_info": info, "pending": pending, "messages": [f"Company info fetched (stub) for {acq_id}/{tgt_id}"]}
