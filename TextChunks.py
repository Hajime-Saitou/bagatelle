# abgatelle
# https://github.com/Hajime-Saitou/bagatelle
#
# Copyright (c) 2026 Hajime Saito
# MIT License
import re
import os

class LoadableTextChunks(list[str]):
    def __init__(self, lines:list[str]=[]):
        super().__init__(lines)

    def loadFromFile(self, filename:str, encoding:str="utf-8"):
        self.clear()
        self.appendFromFile(filename, encoding)

    def appendFromFile(self, filename:str, encoding:str="utf-8"):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "r", encoding=encoding) as f:
            self.extend(f.read().splitlines())

class SearchableTextChunks(LoadableTextChunks):
    def __init__(self, lines:list[str]=[]):
        super().__init__(lines)

    def forwardSearch(self, keywords:list) -> int:
        for index, line in enumerate(self):
            if self.matches(line, keywords):
                return index
        else:
            return -1

    def backwardSearch(self, keywords:list) -> int:
        for index, line in enumerate(reversed(self)):
            if self.matches(line, keywords):
                return len(self) - 1 - index
        else:
            return -1

    def matches(self, line:str, keywords:list):
        return any(re.match(keyword, line) for keyword in keywords)

class PickableTextChunks(SearchableTextChunks):
    def __init__(self, lines:list[str]=[]):
        super().__init__(lines)

    def pickFrom(self, startKeywords:list):
        startIndex = self.forwardSearch(startKeywords)
        return PickableTextChunks(self[startIndex:] if startIndex != -1 else [])

    def pickTo(self, endKeywords:list):
        endIndex:int = self.forwardSearch(endKeywords)
        return PickableTextChunks(self[:endIndex + 1 if endIndex != -1 else len(self)])
    
    def pick(self, startKeywords:list, endKeywords:list):
        return PickableTextChunks(self.pickFrom(startKeywords).pickTo(endKeywords))
