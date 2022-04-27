from gensim.models import Word2Vec
import json
import tqdm
import numpy as np
from sklearn.decomposition import PCA

def transform(id: str):
    total_epoch = 5000
    tick = 10
    
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

if __name__ == '__main__':
    transform('71f12296-c24f-4aac-b135-119f78b80ff9')