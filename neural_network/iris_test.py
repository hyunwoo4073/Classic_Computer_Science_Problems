import csv
from typing import List
from util import normalize_by_feature_scaling
from network import Network
from random import shuffle

if __name__ == "__main__":
    iris_parameters: List[List[float]] = []
    iris_classifications: List[List[float]] = []
    iris_species: List[str] = []
    with open('iris.csv', mode='r') as iris_file:
        irises: List = list(csv.reader(iris_file))
        shuffle(irises) # 데이터를 무작위로 섞음
        for iris in irises:
            parameters: List[float] = [float(n) for n in iris[0:4]]
            iris_parameters.append(parameters)
            species: str = iris[4]
            if species == "Iris-setosa":
                iris_classifications.append([1.0, 0.0, 0.0])
            elif species == "Iris-versicolor":
                iris_classifications.append([0.0, 1.0, 0.0])
            else:
                iris_classifications.append([0.0, 0.0, 1.0])
            iris_species.append(species)
    normalize_by_feature_scaling(iris_parameters)
    iris_network: Network = Network([4, 6, 3], 0.3)

    def iris_interpret_output(output: List[float]) -> str:
        if max(output) == output[0]:
            return "Iris-setosa"
        elif max(output) == output[1]:
            return "Iris-versicolor"
        else:
            return "Iris-virginica"
    
    # 데이터셋에서 처음 140개의 붓꽃을 50회 훈련
    iris_trainers: List[List[float]] = iris_parameters[0:140]
    iris_trainers_corrects: List[List[float]] = iris_classifications[0:140]
    for _ in range(50):
        iris_network.train(iris_trainers, iris_trainers_corrects)
    
    # 데이터셋에서 마지막 10개의 붓꽃을 테스트
    iris_testers: List[List[float]] = iris_parameters[140:150]
    iris_testers_corrects: List[str] = iris_species[140:150]
    iris_results = iris_network.validate(iris_testers, iris_testers_corrects, iris_interpret_output)
    print(f"정확도: {iris_results[0]}/{iris_results[1]} = {iris_results[2] * 100}%")
