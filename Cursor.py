# bagatelle
# https://github.com/Hajime-Saitou/bagatelle
#
# Copyright (c) 2026 Hajime Saito
# MIT License

class RangeCursor:
    def __init__(self, minPosition:int, maxPosition:int):
        self.position = minPosition
        self.minPosition = minPosition
        self.maxPosition = maxPosition

    def current(self) -> int:
        return self.position

    def next(self):
        self.position += 1
        return self.current()

    def previous(self):
        self.position -= 1
        return self.current()

    def hasNext(self) -> bool:
        return self.position <= self.maxPosition

    def hasPrevious(self) -> bool:
        return self.position > self.minPosition

    def isOutOfBounds(self) -> bool:
        return self.position < self.minPosition or self.position > self.maxPosition

    def reset(self):
        self.position = self.minPosition

    def clone(self):
        return RangeCursor(self.minPosition, self.maxPosition)

class SubscriptCursor(RangeCursor):
    def __init__(self, size:int):
        super().__init__(0, size - 1)
        self.size = size

    def clone(self):
        return SubscriptCursor(self.size)
