from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.request import Request

headers = {"User-Agent": "Mozilla/5.0"}
urls = {
    "most-active": "https://finance.yahoo.com/most-active",
    "gainers": "https://finance.yahoo.com/gainers",
    "losers": "https://finance.yahoo.com/losers"
}

def get_stocks(section, amount):
    amount = min(20, max(amount, 1))
    request = Request(urls[section], headers=headers)
    connection = urlopen(request)
    page_html = connection.read()
    connection.close()
    page = bs(page_html, "html.parser")

    container = page.find("tbody")
    symbol_info_rows = container.findAll("tr")
    symbol_list = []
    for i in range(amount):
        cols = symbol_info_rows[i].findAll("td")

        info = {
            "symbol": cols[0].a.text,
            "name": cols[1].text,
            "percent_change": cols[4].text
        }

        symbol_list.append(info)

    return symbol_list
