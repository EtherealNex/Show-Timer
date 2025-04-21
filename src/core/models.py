# The custom datatypes for ShowTimer

from dataclasses import dataclass, field
import uuid

def generate_uuid():
    return uuid.uuid4()

@dataclass
class Call:
    id: str = field(default_factory=lambda: str(generate_uuid()))
    label: str = "Untitled Call" # The name for the Cal
    duration: float = 300 # Length of call in seconds, default 5m (300s)

    def to_JSON(self):
        pass # Prep it for going into JSON

    def from_JSON(self):
        pass # Prep to take from JSON
