import os
from langchain_openai import ChatOpenAI

from config import config


def get_llm() -> ChatOpenAI:
    """
    Returns ChatOpenAI. Requires an OPENAI_API_KEY in the environment.
    """
    # timeout в сек, temperature=0 для детерминизма в маршрутизации
    return ChatOpenAI(
        model=config.llm.model,
        temperature=config.llm.temperature,
        timeout=config.llm.timeout
    )
