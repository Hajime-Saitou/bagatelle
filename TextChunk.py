# bagatelle
# https://github.com/Hajime-Saitou/bagatelle
#
# Copyright (c) 2026 Hajime Saito
# MIT License
import re
import os
from Cursor import SubscriptCursor

class TextChunk(list[str]):
    def __init__(self, lines:list[str]=[]):
        super().__init__(lines)
        self.cursor = SubscriptCursor(len(lines))
        self.updateCursorSize()

    def extend(self, lines:list[str]):
        super().extend(lines)
        self.updateCursorSize()

    def append(self, line:str):
        super().append(line)
        self.updateCursorSize()

    def __add__(self, value):
        self.append(value)
        return self

    def loadFromFile(self, filename:str, encoding:str="utf-8"):
        self.clear()
        self.appendFromFile(filename, encoding)
        self.updateCursorSize()

    def appendFromFile(self, filename:str, encoding:str="utf-8"):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "r", encoding=encoding) as f:
            self.extend(f.read().splitlines())

        self.updateCursorSize()

    def saveToFile(self, filename:str, encoding:str="utf-8"):
        with open(filename, "w", encoding=encoding) as f:
            f.write("\n".join(self))

    def searchForward(self, keywords:list) -> int:
        cursor = self.cursor.clone()
        while cursor.hasNext():
            line = self[cursor.current()]
            if self.matches(line, keywords):
                return cursor.current()
            cursor.next()

        return -1

    def searchBackward(self, keywords:list) -> int:
        cursor = self.cursor.clone()
        while cursor.hasPrevious():
            line = self[cursor.current()]
            if self.matches(line, keywords):
                return cursor.current()
            cursor.previous()

        return -1

    def matches(self, line:str, keywords:list):
        return any(re.match(keyword, line) for keyword in keywords)

    def pickFrom(self, startKeywords:list):
        startPosition = self.searchForward(startKeywords)
        picked = TextChunk(self[startPosition:] if startPosition != -1 else [])
        self.cursor += len(picked)
        return picked

    def pickTo(self, endKeywords:list):
        endPosition = self.searchForward(endKeywords)
        picked = TextChunk(self[self.cursor.current():endPosition if endPosition != -1 else len(self)])
        self.cursor += len(picked)
        return picked

    def pick(self, startKeywords:list, endKeywords:list):
        return TextChunk(self.pickFrom(startKeywords).pickTo(endKeywords))

    def pickRange(self, startPosition:int=None, endPosition:int=None):
        startPosition = startPosition if startPosition is not None else self.cursor.current()
        endPosition = endPosition if endPosition is not None else len(self)
        return TextChunk(self[startPosition:endPosition])

    def pickByCount(self, count:int):
        return self.pickRange(endPosition=self.cursor.current() + count ) if count > 0 else TextChunk([])

    def filter(self, keywords:list):
        return TextChunk([line for line in self if self.matches(line, keywords)])
    
    def toList(self) -> list:
        return self

    def updateCursorSize(self):
        self.cursor.size = len(self)

    def fetchCurrent(self) -> str:
        return self[self.cursor.current()]

    def fetchNext(self) -> str:
        if not self.cursor.hasNext():
            raise StopIteration("Next line is not available.")

        text = self.fetchCurrent()
        self.cursor.next()
        return text

    def fetchPrevious(self) -> str:
        if not self.cursor.hasPrevious():
            raise StopIteration("Previous line is not available.")

        text = self.fetchCurrent()
        self.cursor.previous()
        return text
