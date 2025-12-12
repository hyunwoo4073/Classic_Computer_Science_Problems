from data_point import DataPoint
from plotting import plot_kmeans_clusters_2d

points = DataPoint.from_csv("score.csv")

for p in points:
    print(p, p.num_dimensions)


plot_kmeans_clusters_2d(points, k=3, save_path="clusters.png")