import requests
from bs4 import BeautifulSoup
import json
import os

# URL del sitio de libros para scraping estático
URL = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"

def scrape_books():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text
        availability = article.select_one(".availability").text.strip()
        books.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    # Crear carpeta /data si no existe
    os.makedirs("data", exist_ok=True)

    # Guardar los resultados
    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

    print(f"[✔] {len(books)} libros guardados en data/results.json")

# Ejecutar si se llama desde main
if __name__ == "__main__":
    scrape_books()

def scrape_books():
    print("Iniciando scraping...")

