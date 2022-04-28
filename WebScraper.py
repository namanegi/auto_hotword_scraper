from bs4 import BeautifulSoup
import requests
import json
import unicodedata
from uuid import uuid4
from urllib.parse import urlparse
from multiprocessing import Pool
import pickle

class WebScraper:
    def __init__(self, key_list=[], epoch=10000):
        self.VISITED = set()
        self.STACK = []
        self.SEEDS = [
            "https://www3.nhk.or.jp/news/",
            "https://corona.go.jp/news/",
            "https://news.yahoo.co.jp/",
            "https://portal.auone.jp/",
            "https://news.livedoor.com/"
        ]
        self.id = str(uuid4())
        self.epoch = epoch
        self.key_list = key_list
        self.sent_file = './Temp/' + self.id + '_scraped.json'
        self.workers = 4
        self.is_scraped = False
    
    def is_japanese(self, string):
        for ch in string:
            try:
                name = unicodedata.name(ch) 
            except:
                continue
            if "CJK UNIFIED" in name \
            or "HIRAGANA" in name \
            or "KATAKANA" in name:
                return True
        return False

    def urlPooling(self, l):
        for u in l:
            if u not in self.VISITED and u not in self.STACK:
                self.STACK.append(u)

    def jsonPooling(self):
        json_url1 = "https://www3.nhk.or.jp/news/json16/specialcontents.json"
        js_body = json.loads(requests.get(json_url1).content)['item']
        for item in js_body:
            if 'link' in item:
                new_url = ('https:' + item["link"]) if 'http' not in item['link'] else (item["link"])
                if new_url not in self.VISITED and new_url not in self.STACK:
                    self.STACK.append(new_url)
        json_url2 = "https://www3.nhk.or.jp/news/json16/morenews.json"
        js_body = json.loads(requests.get(json_url2).content)
        for v in js_body.values():
            if 'link' in v:
                new_url = ('https:' + v["link"]) if 'http' not in v['link'] else (v["link"])
                if new_url not in self.VISITED and new_url not in self.STACK:
                    self.STACK.append(new_url)

    def pageScraping(self, url: str):
        print('scraping ', url)
        content_res = []
        url_res = []
        try:
            resp = requests.get(url, timeout=(3.0, 7.5))
            soup = BeautifulSoup(resp.content, 'html.parser', from_encoding='utf-8')
        except:
            return content_res, url_res
        a_pool = soup.find_all('a')
        for a in a_pool:
            o = a.get('href')
            if o:
                if 'http' in o:
                    url_res.append(o[:])
                elif o[:2] == '//':
                    new_o = 'https:' + o
                    url_res.append(new_o[:])
                elif o[0] == '/':
                    cur_url = urlparse(url)
                    new_o = cur_url.scheme + '://' + cur_url.netloc + o
                    url_res.append(new_o[:])
        if self.key_list != []:
            for key in self.key_list:
                if key in resp.text:
                    break
            else:
                return content_res, url_res
        p_pool = soup.find_all('p')
        for p in p_pool:
            if len(p.text) > 15 and self.is_japanese(p.text):
                tmp = p.text.replace('<br>', '。').replace('<br />', '。').replace('<br/>', '。').split('。')
                content_res += [sent for sent in tmp if len(sent) >= 12 and 'JavaScript' not in sent and 'Copyright' not in sent]
        return content_res, url_res

    def saveSent(self, l):
        try:
            with open(self.sent_file, 'r') as f:
                old = json.load(f)
        except:
            with open(self.sent_file, 'w') as f:
                old = []
                json.dump(old, f, indent=2)
        for s in l:
            if s not in old:
                old.append(s.replace(' ', '').replace('  ', '').replace('\u3000', '').replace('\n', ''))
        with open(self.sent_file, 'w') as f:
            json.dump(old, f, indent=2)
        return old

    def scrap(self):
        for u in self.SEEDS:
            self.STACK.append(u)
        self.jsonPooling()
        sents = self.saveSent([])
        while len(sents) <= self.epoch and self.STACK != []:
            p = len(self.STACK)
            pl = Pool(self.workers)
            while p > 0:
                cur_urls = []
                while len(cur_urls) < self.workers:
                    if p > 0:
                        url = self.STACK.pop(0)
                        cur_urls.append(url)
                        self.VISITED.add(url)
                        p -= 1
                    else:
                        break
                pool_res = pl.map(self.pageScraping, cur_urls) # [(c1,u1), (c2, u2), (c3, u3)...]
                cont, urls = [], []
                for res in pool_res:
                    cont.extend(res[0])
                    urls.extend(res[1])
                sents = self.saveSent(cont)
                print(len(sents), 'sentences recorded,', len(self.STACK), ' URLs in pool, and', len(self.VISITED), 'URLs visited')
                if len(sents) > self.epoch:
                    break
                self.urlPooling(urls)
            pl.close()
        self.is_scraped = True

if __name__ == '__main__':
    new_crapper = WebScraper(epoch=100)
    new_crapper.scrap()