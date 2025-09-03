from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ComplianceSection:
    title: str
    content: str
    page_number: int
    subsections: List[str] = None

@dataclass
class ChatMessage:
    question: str
    answer: str
    sources: List[str] = None
    timestamp: str = None

@dataclass
class DemoRequest:
    first_name: str
    last_name: str
    email: str
    company: str
    company_size: str
    message: str
