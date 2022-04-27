from WebScraper import WebScraper
from Tokenizer import parseToken
from Analysis import transform
from Clusering import clustering
from OutputParser import parseHtml

if __name__ == '__main__':
    new_crapper = WebScraper()
    new_crapper.scrap()
    if new_crapper.is_scraped:
        parseToken(new_crapper.id)
        transform(new_crapper.id)
        clustering(new_crapper.id)
        parseHtml(new_crapper.id)