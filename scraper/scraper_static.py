import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib

URL = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"

def descargar_imagen(url, nombre_archivo):
    response = requests.get(url)
    ruta = f"downloads/{nombre_archivo}"
    with open(ruta, "wb") as f:
        f.write(response.content)
    return ruta

def calcular_hash(path):
    with open(path, "rb") as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()

def scrape_books():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    books = []
    files = []

    os.makedirs("downloads", exist_ok=True)

    for i, article in enumerate(soup.select("article.product_pod")):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text
        availability = article.select_one(".availability").text.strip()

        img_src = article.find("img")["src"].replace("../../", "https://books.toscrape.com/")
        nombre_archivo = f"book_{i+1}.jpg"
        ruta = descargar_imagen(img_src, nombre_archivo)
        hash_valor = calcular_hash(ruta)

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "image": nombre_archivo
        })

        files.append({
            "filename": nombre_archivo,
            "path": ruta,
            "sha256": hash_valor
        })

    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

    with open("data/files.json", "w", encoding="utf-8") as f:
        json.dump(files, f, indent=4, ensure_ascii=False)

    print(f"[✔] {len(books)} libros y {len(files)} archivos guardados.")

if __name__ == "__main__":
    scrape_books()

def scrape_books():
    print("Iniciando scraping...")

