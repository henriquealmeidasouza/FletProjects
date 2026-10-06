class Book(object):
    def __init__(self, title: str, author: str, desc: str, price: float, image_url: str = ""):
        self.title = title
        self.author = author = author
        self.desc = desc
        self.price = price
        self.image_url = image_url or ""

def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, desc={self.desc}, price={self.price}, image_url={self.image_url})"