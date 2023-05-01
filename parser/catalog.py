import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint

URL = "https://ru.sputnik.kg/Kyrgyzstan/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response.text


def get_data(html, target_date):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="list__item  ")

    reports = []
    for item in items:
        date_str = item.find("span", class_="list__date").string.strip()
        item_date = datetime.strptime(date_str, "%d.%m.%Y")

        if item_date == target_date:
            reports.append({
                "title": item.find("a", class_="list__title").string.strip(),
                "url": item.find("a", class_="list__title").get('href'),
                "date": date_str,
                "image": item.find("img").get('src')
            })

    pprint(reports)


target_date = datetime.strptime("30.04.2023","%d.%m.%Y")
html = get_html(URL)
get_data(html, target_date)
