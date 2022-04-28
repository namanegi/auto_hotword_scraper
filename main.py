from typing import List
from WebScraper import WebScraper
from Tokenizer import parseToken
from Analysis import transform, clustering
from OutputParser import parseHtml

def autoProcess(keys: List[str]=[], epoch=10000):
    new_crapper = WebScraper(keys, epoch)
    new_crapper.scrap()
    if new_crapper.is_scraped:
        parseToken(new_crapper.id)
        transform(new_crapper.id)
        k = clustering(new_crapper.id)
        html = parseHtml(new_crapper.id, k)
        print(html)
    else:
        print('RUNTIME ERROR')