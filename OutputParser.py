import fugashi
import json
import numpy as np
import tqdm

def parseHtml(id: str, ks: int=None):
    pred_file = './Temp/' + id + '_label.npy'
    silh_file = './Temp/' + id + '_silh.npy'
    raw_file = './Temp/' + id + '_raw.json'
    token_file = './Temp/' + id + '_token.json'
    res_file = './Temp/' + id + '_result.html'

    with open(raw_file, 'r') as f:
        raws = json.load(f)
    with open(token_file, 'r') as f:
        lemmas = json.load(f)
    pred = np.load(pred_file)
    silh = np.load(silh_file)

    tagger = fugashi.Tagger()
    if ks is None:
        ks = len(set(pred))

    html_file = open(res_file, 'w', encoding='UTF-8')
    for k in tqdm.tqdm(range(ks)):
        print('<h3>cluster ' + str(k) + '</h3>', file=html_file)
        lemma_cur = []
        raw_cur = []
        silh_cur = []
        for i, sent in enumerate(lemmas):
            if pred[i] == k:
                lemma_cur.append(sent)
                raw_cur.append(raws[i])
                silh_cur.append(silh[i])
        print('total: ' + str(len(lemma_cur)) + '<br />', file=html_file)
        print('silhouette value: ' + str(sum(silh_cur) / len(silh_cur)) + '<br />', file=html_file)
        dic = {}
        for sent in lemma_cur:
            for lemma in sent:
                if lemma not in dic:
                    dic[lemma] = 1
                else:
                    dic[lemma] += 1
        sort_dic = sorted(dic.items(), key=lambda x:x[1], reverse=True)
        print('total lemma: ' + str(len(sort_dic)) + '<br />', file=html_file)
        counter = 0
        p = 0
        hot = []
        hot_count = []
        while counter < 5 and p < len(sort_dic):
            try:
                if '名詞' not in tagger(sort_dic[p][0])[0].pos or '数詞' in tagger(sort_dic[p][0])[0].pos or '代名詞' in tagger(sort_dic[p][0])[0].pos or len(sort_dic[p][0]) == 1 or sort_dic[p][0] in ["さん"]:
                    pass
                else:
                    hot.append(sort_dic[p][0])
                    hot_count.append(sort_dic[p][1])
                    counter += 1
            except:
                pass
            p += 1
        raw_refs = []
        mx = 0
        for i in range(len(raw_cur)):
            score = 0
            for h in hot:
                if h in lemma_cur[i]:
                    score += 1
            if score >= mx:
                mx = score
                raw_refs.insert(0, ''.join(raw_cur[i]))
                if len(raw_refs) > 5:
                    raw_refs.pop()
        print('<h5>中心文書</h5>', file=html_file)
        silh_cur_mx = sorted(silh_cur, reverse=True)[:5]
        for si in silh_cur_mx:
            print(''.join(raw_cur[silh_cur_mx.index(si)]) + '<br />', file=html_file)
        print('<h5>ホットワード</h5>', file=html_file)
        print(', '.join(hot) + '<br />', file=html_file)
        print(', '.join([str(c) for c in hot_count]) + '<br />', file=html_file)
        print('<h5>ホット文書</h5>', file=html_file)
        for raw_ref in raw_refs:
            tagged_words = tagger(raw_ref)
            row = ''
            for word in tagged_words:
                if word.feature.lemma in hot:
                    row = row + '<span style="color: red;">' + word.surface + '</span>'
                else:
                    row = row + word.surface
            print(row + '<br />', file=html_file)
        # print(ref)
        
    html_file.close()
    return res_file

if __name__ == '__main__':
    parseHtml('67427039-3f14-4aad-9dd1-f232b73986b5')