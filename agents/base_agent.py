from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.state: Dict[str, Any] = {}

    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def validate_output(self, output_data: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        raise NotImplementedError
