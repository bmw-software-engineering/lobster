from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class LevelDefinition:
    name: str
    kind: str
    traces: List[str] = field(default_factory=list)
    source: List[Any] = field(default_factory=list)
    needs_tracing_up: bool = False
    needs_tracing_down: bool = False
    breakdown_requirements: List[Any] = field(default_factory=list)
    raw_trace_requirements: List[Any] = field(default_factory=list)

    # Flags for serialization - they are a workaround due to the fact that the system
    # tests do a text comparison of a generated LOBSTER file against a reference file.
    # The serialization pattern should be updated such that empty lists are not
    # serialized, but that means to update all system tests.
    # This is a temporary solution to avoid breaking existing tests.
    serialize_needs_tracing_up: bool = True
    serialize_needs_tracing_down: bool = True
    serialize_breakdown_requirements: bool = True

    def to_json(self) -> dict:
        """Convert the Level instance to a JSON-compatible dictionary."""
        result = {
            "name": self.name,
            "kind": self.kind,
            "traces": self.traces,
            "source": self.source,
        }
        if self.serialize_needs_tracing_up:
            result["needs_tracing_up"] = self.needs_tracing_up
        if self.serialize_needs_tracing_down:
            result["needs_tracing_down"] = self.needs_tracing_down
        if self.serialize_breakdown_requirements:
            result["breakdown_requirements"] = self.breakdown_requirements
        return result

    @classmethod
    def from_json(cls, data: dict) -> 'LevelDefinition':
        """Create a Level instance from a JSON-compatible dictionary."""
        return cls(
            name=data["name"],
            kind=data["kind"],
            traces=data.get("traces", []),
            source=data.get("source", []),
            needs_tracing_up=data.get("needs_tracing_up", False),
            needs_tracing_down=data.get("needs_tracing_down", False),
            breakdown_requirements=data.get("breakdown_requirements", []),
            serialize_needs_tracing_up="needs_tracing_up" in data,
            serialize_needs_tracing_down="needs_tracing_down" in data,
            serialize_breakdown_requirements="breakdown_requirements" in data,
        )
