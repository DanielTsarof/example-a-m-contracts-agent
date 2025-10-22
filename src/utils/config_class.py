import os
from typing import Literal

from pydantic import BaseModel, Field


class Logger(BaseModel):
    """
    :param file_path: path to log file
    :param format: log format ("{time} | {level} | {message} | {extra} | {user} | {ip}")
    :param rotation: max log file size ("50 KB, "100 MB" etc.)
    :param enqueue: queue log messages (for multiprocessor and asynchronous programs)
    :param serialize: write log in JSON format
    :param level: log level
    """
    file_path: str = "./logs.log"
    format: str = "{time} | {level} | {name}:{function}:{line} | {message}"
    rotation: str = "50 MB"
    enqueue: bool = False
    serialize: bool = False
    level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE"]


class Uvicorn(BaseModel):
    ip: str
    port: int = Field(default=os.getenv('APP_PORT'))
    log_level: str = "info"
    enable_auto_reload: bool = True


class LLM(BaseModel):
    model: str
    temperature: float = 0.0
    timeout: float = 30.0


class Config(BaseModel):
    uvicorn: Uvicorn
    logger: Logger
    llm: LLM
