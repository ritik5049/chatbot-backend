## Web Scraping and Searching API

This is a FastAPI based API that can scrape articles from given URLs and store them in a database. It also provides a search endpoint that can search for articles in the database containing a given query string.

### Installation

- Clone the repository and navigate to the project directory.
- Create a virtual environment and activate it.
- Install the requirements from depedencies below.

### Running the API

- Start the API using the command uvicorn main:app --reload
- The API will be available at http://localhost:8000

### Endpoints

#### POST /articles
This endpoint accepts a URL and scrapes the article at the given URL. The scraped article is saved to the database. The request body should be a JSON object with the following format:

```
{
    "url": "https://example.com/article"
}
```

#### GET /articles
This endpoint searches the database for articles containing the given query string. The response contains a list of articles with matching snippets of the query string in their content. The request query parameters should be:

- query (required): The query string to search for
- limit (optional): The maximum number of results to return (default 10)

### Dependencies

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- BeautifulSoup: A Python library used to extract data from HTML and XML files.
- Requests: A Python library used to send HTTP requests.
- logging: A Python module that allows for event logging.
- CORS Middleware: A middleware for adding Cross-Origin Resource Sharing (CORS) support to FastAPI applications.
- Supabase: A backend-as-a-service platform that provides a database, auth, and storage APIs.
