class Article:
    def __init__(self, title: str, content: str, url: str):
        self.title = title
        self.content = content
        self.url = url

    def to_dict(self):
        return {"title": self.title, "content": self.content, "url": self.url}
