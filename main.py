from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests
import logging
from fastapi.middleware.cors import CORSMiddleware
from models.article import Article
from models.urlData import UrlData
from utils.supabase import get_articles_table

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def scrape_article(url: str):
    # scrape the webpage at the given URL and return the title and content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text.strip()
    content = "\n\n".join(p.text.strip() for p in soup.find_all("p"))
    result = {"title": title, "content": content}
    print(result)
    return result


@app.post("/articles")
async def create_article(url: UrlData):
    # scrape the article at the given URL and save it to the database
    try:
        logging.error("here")
        article_dict = scrape_article(url.url)
        print(type(article_dict))
        article = Article(**article_dict, url=url.url)
        print(article.to_dict())
        articles_table = get_articles_table()
        res = articles_table.insert(article.to_dict()).execute()
        return res.data[0]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/articles")
async def search_article(query: str, limit: int = 10):
    # search the database for the article with the given URL containing the given query string
    try:
        articles_table = get_articles_table()
        res = articles_table.select("*").ilike("content", f"%{query}%").limit(limit).execute()
        results = []
        for article in res.data:
            content = article['content']
            snippets = []
            index = 0
            while index != -1:
                index = content.find(query, index)
                if index != -1:
                    start = max(index - 10, 0)
                    end = min(index + len(query) + 10, len(content))
                    snippets.append("..." + content[start:end] + "...")
                    index += 1
            results.append({
                'id': article['id'],
                'url': article['url'],
                'title': article['title'],
                'snippets': snippets
            })
        if not results:
            raise HTTPException(status_code=404, detail="Article not found")

        return results

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
