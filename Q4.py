"""Q4: Library System (Classes and Inheritance)"""

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.title == other.title and self.author == other.author

    def age(self, current_year):
        return current_year - self.year


class EBook(Book):
    def __init__(self, title, author, year, size_mb):
        super().__init__(title, author, year)
        self.size_mb = size_mb

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) [{self.size_mb} MB]"

    def download_seconds(self, mbit_per_s):
        return round((self.size_mb * 8) / mbit_per_s, 1)


class Library:
    def __init__(self):
        self.books = []

    def add(self, book):
        if book not in self.books:
            self.books.append(book)

    def find_by_author(self, author):
        return [b for b in self.books if b.author == author]

    def oldest(self):
        if not self.books:
            return None
        return min(self.books, key=lambda b: b.year)

    def __len__(self):
        return len(self.books)


if __name__ == "__main__":
    lib = Library()
    b1 = Book("1984", "George Orwell", 1949)
    b2 = Book("Animal Farm", "George Orwell", 1945)
    b3 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    e1 = EBook("Dune", "Frank Herbert", 1965, 2.5)
    e2 = EBook("Foundation", "Isaac Asimov", 1951, 1.8)

    for book in [b1, b2, b3, e1, e2]:
        lib.add(book)

    lib.add(Book("1984", "George Orwell", 1949))  # duplicate, ignored

    print("Books:", len(lib))
    print("Orwell:", [str(b) for b in lib.find_by_author("George Orwell")])
    print("Oldest:", lib.oldest())
    print("Age of 1984:", b1.age(2026))
    print("Download Dune at 10 Mbit/s:", e1.download_seconds(10), "s")
    print(e1)