from typing import NamedTuple, List

class Item(NamedTuple):
    name: str
    weight: int
    value: float

def knapsack(items: List[Item], max_capacity: int) -> List[Item]:
    # 동적 계획법 표를 작성
    table: List[List[float]] = [[0.0 for _ in range(max_capacity + 1)] for _ in range(len(items) + 1)]
    for i, item in enumerate(items):
        for capacity in range(1, max_capacity + 1):
            previous_items_value: float = table[i][capacity]
            if capacity >= item.weight: # 물건이 배낭 용량에 맞는 경우
                value_freeing_weight_for_item: float = table[i][capacity - item.weight]
                # 이전 물건보다 더 가치가 있는 경우에만 물건을 넣음
                table[i + 1][capacity] = max(value_freeing_weight_for_item + item.value, previous_items_value)
            else: # 용량에 맞지 않아서 물건을 넣을 수 없음
                table[i + 1][capacity] = previous_items_value
    # 표에서 최상의 결과를 구함
    solution: List[Item] = []
    capacity = max_capacity
    for i in range(len(items), 0, -1): # 거꾸로 반복
        # 배낭에 이 물건이 있는가?
        if table[i - 1][capacity] != table[i][capacity]:
            solution.append(items[i - 1])
            # 용량에서 물건 무게를 뺌
            capacity -= items[i - 1].weight
    return solution

if __name__ == "__main__":
    items: List[Item] = [Item("television", 50, 500),
                            Item("candlesticks", 2, 300),
                            Item("stereo", 35, 400),
                            Item("laptop", 3, 1000),
                            Item("food", 15, 50),
                            Item("clothing", 20, 800),
                            Item("jewelry", 1, 4000),
                            Item("books", 100, 300),
                            Item("printer", 18, 30),
                            Item("refrigerator", 200, 700),
                            Item("painting", 10, 1000)]
    print(knapsack(items, 75))