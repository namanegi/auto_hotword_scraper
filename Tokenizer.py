import json
import fugashi

def parseToken(id: str):
    tagger = fugashi.Tagger()
    zen = "！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀>？＠ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～"
    han = zen.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

    file_name = './Temp/' + id + '_scraped.json'
    raw_name = './Temp/' + id + '_raw.json'
    token_name = './Temp/' + id + '_token.json'

    with open(file_name, 'r') as f:
        data = json.load(f)
    p = 0
    while p < len(data):
        data[p] = data[p].replace(' ', '').replace('  ', '').replace('\u3000', '').replace('\n', '')
        for i, c in enumerate(zen):
            data[p] = data[p].replace(c, han[i])
        p += 1
    raw_sent = []
    token_sent = []
    for sent in data:
        cur_raw = []
        cur_token = []
        for word in tagger(sent):
            if '補助記号' in word.pos:
                continue
            if word.feature.lemma is None:
                cur_raw.append(word.surface)
                cur_token.append(word.surface)
            else:
                cur_raw.append(word.surface)
                cur_token.append(word.feature.lemma)
        if 5 <= len(cur_raw) <= 64:
            raw_sent.append(cur_raw[:])
            token_sent.append(cur_token[:])

    with open(raw_name, 'w') as f:
        json.dump(raw_sent, f, indent=2)
    with open(token_name, 'w') as f:
        json.dump(token_sent, f, indent=2)

if __name__ == '__main__':
    parseToken('71f12296-c24f-4aac-b135-119f78b80ff9')