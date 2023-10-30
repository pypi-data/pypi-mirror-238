class QmodSizedProxy:
    def __init__(self, size: int) -> None:
        self._size = size

    def __len__(self) -> int:
        return self._size
