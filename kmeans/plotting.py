import matplotlib.pyplot as plt
from typing import List
from data_point import DataPoint
from kmeans import KMeans

def plot_kmeans_clusters_2d(points: List[DataPoint], 
                            k: int = 3, 
                            max_iter: int = 100,
                            save_path: str = "kmeans_result.png"):
    
    kmeans = KMeans[DataPoint](k=k, points=points)
    clusters = kmeans.run(max_iterations=max_iter)

    colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta"]

    plt.figure(figsize=(8, 6))

    for idx, cluster in enumerate(clusters):
        xs = [p.dimensions[0] for p in cluster.points]
        ys = [p.dimensions[1] for p in cluster.points]

        plt.scatter(xs, ys, c=colors[idx % len(colors)], label=f"Cluster {idx}", s=40)

        # 중심 표시
        cx, cy = cluster.centroid.dimensions[:2]
        plt.scatter(cx, cy, c="black", marker="X", s=120)

    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.title("K-Means Clustering Results (2D)")
    plt.legend()
    plt.grid(True)

    # CLI 환경: 이미지 파일로 저장
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"그래프 저장 완료 → {save_path}")

    plt.close()  # 메모리 정리 (CLI 환경에서는 특히 중요)
