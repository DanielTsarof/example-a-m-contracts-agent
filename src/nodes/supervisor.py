from typing import Any, Dict
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm

ALLOWED_NEXT = [
    "company_info",
    "regulatory",
    "financing",
    "aggregate_score",
    "human_approval",
    "recommendation",
]

SYSTEM_PROMPT = (
        "You are a concise router for an M&A analysis graph. "
        "Given the current state summary, choose the SINGLE next node to run. "
        "Allowed nodes: " + ", ".join(ALLOWED_NEXT) + ". "
                                                      "Return EXACTLY one token (the node name), lowercase, no punctuation, no explanation."
)


def _state_summary(state: Dict[str, Any]) -> str:
    # краткая сводка для LLM, без лишнего шума
    parts = []
    p = state.get("pending", {})
    parts.append(f"pending={p}")
    if "company_info" in state:
        parts.append("company_info=present")
    if "regulatory" in state:
        r = state["regulatory"]
        parts.append(f"regulatory={{risk:{r.get('risk')}, hhi_pre:{r.get('hhi_pre')}, hhi_post:{r.get('hhi_post')}}}")
    if "financing" in state:
        f = state["financing"]
        parts.append(f"financing={{wacc:{f.get('wacc')}, eps:{f.get('eps_effect')}}}")
    if "score" in state:
        s = state["score"]
        parts.append(
            f"score={{verdict:{s.get('verdict')}, value:{s.get('value')}, human_approved:{s.get('human_approved', False)}}}")
    return " | ".join(parts)


def _normalize_choice(text: str) -> str:
    t = (text or "").strip().lower()
    for opt in ALLOWED_NEXT:
        if t == opt or f" {opt} " in f" {t} " or t.startswith(opt):
            return opt
    return "aggregate_score"


def supervisor_node(state: Dict[str, Any]):
    """
    A router with strict rules (deterministic), followed by LLM as a prompter.
    """
    p = state.get("pending", {})

    # Жёсткие правила (приоритетнее LLM):
    if p.get("need_company_info", True) and "company_info" not in state:
        return Command(goto="company_info")
    if p.get("need_regulatory", True):
        return Command(goto="regulatory")
    if p.get("need_financing", True):
        return Command(goto="financing")
    if p.get("ready_for_aggregate", False) and "score" not in state:
        return Command(goto="aggregate_score")
    if "score" in state and "human_approved" not in state["score"]:
        return Command(goto="human_approval")
    if "score" in state and state["score"].get("human_approved") is True:
        return Command(goto="recommendation")

    # let the LLM choose the next step
    llm = get_llm()
    summary = _state_summary(state)
    resp = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=summary)])
    choice = _normalize_choice(getattr(resp, "content", ""))
    return Command(goto=choice)
