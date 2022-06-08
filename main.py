from types import NoneType
import requests
import bs4
import fake_useragent
import re
# from headers import HEADERS
KEYWORDS = ['дизайн', 'фото', 'web', 'python','костюм', 'финансисты ']
# KEYWORDS = ['ужас']
rkeywords = KEYWORDS[0]
for kw in KEYWORDS[1:]:
    rkeywords += f'|{kw}'
print(rkeywords)

useragent_ = fake_useragent.UserAgent()
HEADERS = {'user-agent': useragent_.random}

urlfull='https://habr.com/ru/all'
url='https://habr.com'

if __name__ == '__main__':    
    pageexist = True
    while pageexist:
        try:
            response = requests.get(urlfull, headers=HEADERS)
            response.raise_for_status()
        except Exception:
            print('Ошибка при открытии страницы')
            break
        text = response.text
        soup = bs4.BeautifulSoup(text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            preview = article.find('div', class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
            if (type(preview) != NoneType) and (re.search(rkeywords, preview.text.lower())):
                # print(preview.text.lower())
                # headarticle = article.find_all('span', class_=None)[:-1]
                date = article.find_all('time')[0]['datetime'][:10]
                title = article.find_all(class_='tm-article-snippet__title-link')[0].find_all('span')[0].text
                link = url + article.find_all(class_='tm-article-snippet__title-link')[0]['href']
                print(f'{date} - {title} - {link}')
        try:
            urlfull = url + soup.find(id="pagination-next-page")['href']
            print(urlfull)
        except KeyError:
            print('Больше нет страниц')
            # pageexist = False
            break