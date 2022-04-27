from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import tqdm

def clustering(id: str):
    ds = np.load('./Temp/' + id + '_pca.npy')

    ks = [k for k in range(10, 26)]
    silhouette = []
    for k in tqdm.tqdm(ks):
        cluster = KMeans(n_clusters=k, max_iter=5000)
        cluster.fit(ds)
        silhouette.append(silhouette_score(ds, cluster.labels_))

    best_k = ks[silhouette.index(max(silhouette))]

    cluster = KMeans(n_clusters=best_k, max_iter=5000)
    cluster.fit(ds)
    np.save('./Temp/' + id + '_label', cluster.labels_)
    return best_k

if __name__ == '__main__':
    clustering('71f12296-c24f-4aac-b135-119f78b80ff9')