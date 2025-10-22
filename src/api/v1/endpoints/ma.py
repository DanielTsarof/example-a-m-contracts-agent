from fastapi import APIRouter, HTTPException
from langgraph.types import Command

from graph import graph
from schemas.ma import (
    InvokePayload,
    ResumePayload,
)

router = APIRouter(tags=["ma-agent"])


@router.post("/run")
def run(payload: InvokePayload):
    cfg = {"configurable": {"thread_id": payload.thread_id}}
    init_state = payload.model_dump()
    init_state.pop("thread_id", None)
    try:
        out = graph.invoke(init_state, cfg)
    except Exception as e:
        raise HTTPException(500, f"invoke error: {e}")

    waiting = out.get("__interrupt__")
    if waiting is not None:
        return {"status": "waiting_for_approval", "interrupt": waiting, "thread_id": payload.thread_id}

    return {"status": "ok", "state": out, "thread_id": payload.thread_id}


@router.post("/resume")
def resume(payload: ResumePayload):
    cfg = {"configurable": {"thread_id": payload.thread_id}}
    try:
        out = graph.invoke(Command(resume=payload.approve), cfg)
    except Exception as e:
        raise HTTPException(500, f"resume error: {e}")
    return {"status": "ok", "state": out, "thread_id": payload.thread_id}


@router.get("/state/{thread_id}")
def get_state(thread_id: str):
    cfg = {"configurable": {"thread_id": thread_id}}
    try:
        st = graph.get_state(cfg)
        hist = graph.get_state_history(cfg)
    except Exception as e:
        raise HTTPException(500, f"state error: {e}")
    return {"thread_id": thread_id, "state": st, "history_len": len(hist)}


@router.get("/report/{thread_id}")
def get_report(thread_id: str):
    cfg = {"configurable": {"thread_id": thread_id}}
    st = graph.get_state(cfg)
    msgs = st.values.get("messages") or []
    report = [m for m in msgs if isinstance(m, str) and m.startswith("# M&A Recommendation")]
    if not report:
        raise HTTPException(404, "report not found; run the graph first")
    return {"thread_id": thread_id, "report": report[-1]}
