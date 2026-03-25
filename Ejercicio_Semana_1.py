import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.theguardian.com/international"

response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "theguardian.com" in href and "/202" in href:
        if href not in links:
            links.append(href)

count = 0

for link in links:
    if count == 5:
        break

    try:
        res = requests.get(link, headers=headers, timeout=5)
        news_soup = BeautifulSoup(res.text, "html.parser")

        author_tag = news_soup.find("a", rel="author")
        if not author_tag:
            continue
        author = author_tag.text.strip()

        title_tag = news_soup.find("h1")
        title = title_tag.text.strip() if title_tag else "No encontrado"

        
        date = "No disponible"
        meta_date = news_soup.find("meta", property="article:published_time")
        if meta_date and meta_date.has_attr("content"):
            raw_date = meta_date["content"].split("T")[0]  
            dt = datetime.strptime(raw_date, "%Y-%m-%d")
            date = dt.strftime("%d %b %Y")  

        
        print("\n----------------------")
        print("Título:", title)
        print("Enlace:", link)
        print("Autor:", author)
        print("Fecha:", date)

        count += 1

    except:
        continue

if count < 5:
    print("\n⚠️ No se encontraron 5 noticias completas")