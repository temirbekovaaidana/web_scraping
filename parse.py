import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.kivano.kg/noutbuki?brands=acer-apple"
HEADERS = {
    "users-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "accept": "*/*",
}
LINK = "https://www.kivano.kg"
CSV_FILE = "laptop.csv"

def get_html(url, headers):
    response = requests.get(url, headers=headers)
    return response

def get_content_from_html(html_text) -> list:
    soup = BeautifulSoup(html_text, "html.parser")
    items = soup.find_all("div", class_="item product_listbox oh")
    laptops = []
    for item in items:
        laptops.append(
            {
                "title": item.find("div", class_="listbox_title oh").get_text().replace("\n", ""),
                "description": item.find("div", class_="product_text pull-left").get_text().replace("\n", ""),
                "price": item.find("div", class_="listbox_price text-center").get_text().replace("\n", ""),
                "image": LINK + item.find("img").get("src"),
            }
        )
    return laptops


def save_data(laptops: list) -> None:
    with open(CSV_FILE, "w") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["Название", "Описание", "Цена", "Картинка"])
        for laptop in laptops:
            writer.writerow([laptop["title"],laptop["description"],
                             laptop["price"], laptop["image"]])

def get_result_parse():
    html = get_html(URL, HEADERS)
    if html.status_code == 200:
        laptops = get_content_from_html(html.text)
        save_data(laptops)
        return laptops

print(get_result_parse())