from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Choice:
    index: int
    message: Message
    logprobs: Optional[dict]
    finish_reason: str

@dataclass
class Usage:
    queue_time: float
    prompt_tokens: float
    prompt_time: float
    completion_tokens: float
    completion_time: float
    total_tokens: float
    total_time: float

@dataclass
class ApiResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    error_message: Optional[str] = None
    system_fingerprint: Optional[str] = None
    x_groq: Optional[dict] = None
