import typing
from collections import Counter


class PortToWireNameGenerator:
    def __init__(self) -> None:
        self._name_counter: typing.Counter[str] = Counter()

    def get(self, port_name: str) -> str:
        counter = self._name_counter[port_name]
        self._name_counter[port_name] += 1
        return f"{port_name}_{counter}"
