from typing import Any, Dict

# TODO: replace with pdf generation
def recommendation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Creating a short Markdown report in messages."""
    s = state.get("score", {})
    reg = state.get("regulatory", {})
    fin = state.get("financing", {})
    report = f"""# M&A Recommendation

**Verdict:** {s.get('verdict')} | **Score:** {s.get('value')}
- Regulatory (HHI): **{reg.get('hhi_pre', 'n/a')} → {reg.get('hhi_post', 'n/a')}** ({reg.get('risk', 'n/a')})
- Financing: **{fin.get('eps_effect', 'n/a')}**, WACC ≈ **{(fin.get('wacc', 0.0) * 100):.1f}%**
- Contributions: {s.get('contrib')}
- Human approval: **{s.get('human_approved', False)}**
"""
    return {"messages": [report]}
