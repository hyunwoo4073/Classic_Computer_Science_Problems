from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce
from layer import Layer
from util import sigmoid, derivative_sigmoid

T = TypeVar('T') # 신경망 출력 타입

class Network:
    def __init__(self, layer_structure: List[int], learning_rate: float, activation_function: Callable[[float], float] = sigmoid, derivative_activation_function: Callable[[float], float] = derivative_sigmoid) -> None:
        if len(layer_structure) < 3:
            raise ValueError("오류: 최소 3개의 층이 필요합니다(입력층, 은닉층, 출력층)!")
        self.layers: List[Layer] = []
        # 입력층
        input_layer: Layer = Layer(None, layer_structure[0], learning_rate, activation_function, derivative_activation_function)
        self.layers.append(input_layer)
        # 은닉층과 출력층
        for previous, num_neurons in enumerate(layer_structure[1::]):
            next_layer = Layer(self.layers[previous], num_neurons, learning_rate, activation_function, derivative_activation_function)
            self.layers.append(next_layer)
    
    # 입력 데이터를 첫 번째 층으로 푸시한 후,
    # 첫 번째에서 두 번째, 두 번째에서 세 번째... 층으로 출력
    def outputs(self, input: List[float]) -> List[float]:
        return reduce(lambda inputs, layer: layer.outputs(inputs), self.layers, input)

    # 출력 오류와 예상 결과를 비교하여 각 뉴런의 변화를 파악
    def backpropagate(self, expected: List[float]) -> None:
        # 출력층 뉴런에 대한 델타를 계산
        last_layer: int = len(self.layers) - 1
        self.layers[last_layer].calculate_deltas_for_output_layer(expected)
        # 은닉층에 대한 델타를 역순으로 계산
        for l in range(last_layer - 1, 0, -1):
            self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l + 1])

    # backpropagate() 메서드는 실제로 가중치를 수정하지 않음
    # 이 메서드는 backpropagate() 메서드에서 계산된 델타를 사용하여 가중치를 수정
    def update_weights(self) -> None:
        for layer in self.layers[1:]: # 입력층은 제외
            for neuron in layer.neurons:
                for w in range(len(neuron.weights)):
                    neuron.weights[w] = neuron.weights[w] + (neuron.learning_rate * (layer.previous_layer.output_cache[w]) * neuron.delta)

    # train() 메서드는 많은 입력을 통해 실행된 outputs() 메서드의 결과를 사용
    # backpropagate() 메서드에 예상값을 입력하고
    # update_weights() 메서드를 호출하여 비교
    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        for location, xs in enumerate(inputs):
            ys: List[float] = expecteds[location]
            outs: List[float] = self.outputs(xs)
            self.backpropagate(ys)
            self.update_weights()

    # validate() 메서드는 분류가 필요한 일반화된 결과에서
    # 정확한 분류 수, 테스트 된 총 샘플 수, 정확한 분류 백분율을 반환
    def validate(self, inputs: List[List[float]], expecteds: List[T], interpret_output: Callable[[List[float]], T]) -> Tuple[int, int, float]:
        correct: int = 0
        for input, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(input))
            if result == expected:
                correct += 1
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage