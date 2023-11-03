from bs4 import BeautifulSoup
import requests, itertools

def main() -> None:

    def gener_element() -> str:
        """gener self element"""

        for group in self_categories:
            for digit in itertools.count(start=1):

                page = active_session.get(url=f"{url}{group}{digit}.html")
                if page.status_code != 200:
                    break
                page.encoding = "UTF-8"
                
                soup_page = BeautifulSoup(page.text, "lxml")
                yield from (product.select_one("a > p").parent["href"]
                    for product in soup_page.find("div", "item_card").find_all("div", "item")
                )

               

    url, total = "http://parsinger.ru/html/", 0

    with requests.Session() as active_session:
        categories = active_session.get(url="http://parsinger.ru/html/index1_page_1.html")
        categories.encoding ="UTF-8"

        categories_soup = BeautifulSoup(categories.text, "lxml")
        self_categories = (
            category["href"].rstrip("1.html")
            for category in categories_soup.find("div", class_="nav_menu").find_all("a")
        )

        for element in gener_element():
            response = active_session.get(url=f"{url}{element}")
            response.encoding = "UTF-8"

            soup = BeautifulSoup(response.text, "lxml")
            count = int(soup.find(id="in_stock").text.lstrip("В наличии:"))
            price = int(soup.find(id="price").text.rstrip("руб"))
            total += count * price
           
        print(total)

 

if __name__ == "__main__":
    main()
