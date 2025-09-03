from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ComplianceSection:
    title: str
    content: str
    page_number: int
    subsections: List[str] = field(default_factory=list)

@dataclass
class ChatMessage:
    question: str
    answer: str
    sources: List[str] = field(default_factory=list)
    timestamp: Optional[str] = None

@dataclass
class DemoRequest:
    first_name: str
    last_name: str
    email: str
    company: str
    company_size: str
    message: str
