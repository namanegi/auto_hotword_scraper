from gensim.models import Word2Vec

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

import numpy as np

from multiprocessing import Pool
import json
import tqdm

def transform(id: str):
    total_epoch = 2000
    tick = 20
    
    file_name = './Temp/' + id + '_token.json'
    with open(file_name, 'r') as f:
        token_data = json.load(f)
    model = Word2Vec(sentences=token_data, vector_size=100, window=5, min_count=1, workers=4)
    
    for i in tqdm.tqdm(range(total_epoch // tick)):
        model.train(token_data, total_examples=len(token_data), epochs=tick)

    ds = []
    for row in token_data:
        cur = []
        for i in range(64):
            if i < len(row):
                cur.append(model.wv.get_vector(row[i], norm=True))
            else:
                cur.append(np.zeros((100, )))
        ds.append(cur[:])

    token_data = None
    
    ds = np.array(ds, dtype=np.float32)
    print(ds.shape)
    
    pca_1 = PCA(n_components=800)
    pca_2 = PCA(n_components=350)
    features_1 = pca_1.fit_transform(ds.reshape((-1, 6400)))
    print(features_1.shape)
    features_2 = pca_2.fit_transform(features_1)
    print(features_2.shape)

    np_file = './Temp/' + id + '_pca'
    np.save(np_file, features_2)


def sim_k(k, ds):
    cluster = KMeans(n_clusters=k, max_iter=5000)
    cluster.fit(ds)
    return silhouette_score(ds, cluster.labels_)

def wrap_sim_k(args):
    return sim_k(*args)

def clustering(id: str):
    workers = 4
    ds = np.load('./Temp/' + id + '_pca.npy')

    ks = [k for k in range(5, 21)]
    silhouette = []

    p = Pool(workers)
    for kh in tqdm.tqdm(range(5, 21, 4)):
        silhouette = silhouette + p.map(wrap_sim_k, [(k, ds) for k in range(kh, kh + 4)])

    # for k in tqdm.tqdm(ks):
    #     cluster = KMeans(n_clusters=k, max_iter=5000)
    #     cluster.fit(ds)
    #     silhouette.append(silhouette_score(ds, cluster.labels_))



    best_k = ks[silhouette.index(max(silhouette))]

    cluster = KMeans(n_clusters=best_k, max_iter=5000)
    cluster.fit(ds)
    np.save('./Temp/' + id + '_label', cluster.labels_)
    sil_values = silhouette_samples(ds, cluster.labels_)
    np.save('./Temp/' + id + '_silh', sil_values)
    return best_k

if __name__ == '__main__':
    k = clustering('67427039-3f14-4aad-9dd1-f232b73986b5')
    print(k)