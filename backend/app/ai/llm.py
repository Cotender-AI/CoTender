"""LLMClient interface. TODO(B3): Azure OpenAI implementation + fallback provider (see F4-AI)."""

from typing import Protocol

from pydantic import BaseModel


class LLMClient(Protocol):
    def extract[T: BaseModel](self, *, system: str, document_text: str, schema: type[T]) -> T:
        """Send page text (wrapped in delimiters and declared as data) and return a validated
        instance of `schema`, or raise if the output does not validate."""
        ...
