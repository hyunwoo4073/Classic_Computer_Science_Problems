from __future__ import annotations
from typing import List, Optional
from generic_search import bfs, Node, node_to_path

MAX_NUM: int = 3

class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries # 서쪽 강둑에 있는 선교사 수
        self.wc: int = cannibals # 서쪽 강둑에 있는 식인종 수
        self.em: int = MAX_NUM - self.wm # 동쪽 강둑에 있는 선교사 수
        self.ec: int = MAX_NUM - self.wc # 동쪽 강둑에 있는 식인종 수
        self.boat: bool = boat
    
    def __str__(self) -> str:
        return ("서쪽 강둑에는 {}명의 선교사와 {}명의 식인종이 있다.\n"
                "동쪽 강둑에는 {}명의 선교사와 {}명의 식인종이 있다.\n"
                "배는 {}쪽에 있다.")\
                .format(self.wm, self.wc, self.em, self.ec, ("서" if self.boat else "동"))

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return Fasle
        return True

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.boat: # 서쪽 강둑에 있는 배
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else: # 동쪽 강둑에 있는 배
            if self.em > 1:
