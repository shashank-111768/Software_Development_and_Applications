

class Book:

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return (
            self.title
            + " by "
            + self.author
            + " ("
            + str(self.year)
            + ")"
        )

    def age(self, current_year):
        return current_year - self.year


class EBook(Book):

    def __init__(self, title, author, year, size_mb):
        Book.__init__(self, title, author, year)
        self.size_mb = size_mb

    def __str__(self):
        return (
            Book.__str__(self)
            + " ["
            + str(self.size_mb)
            + " MB]"
        )

    def download_seconds(self, speed):
        return round(
            (self.size_mb * 8) / speed,
            1
        )


class Library:

    def __init__(self):
        self.books = {}

    def add(self, book):

        key = book.title + "|" + book.author

        self.books[key] = book

    def find_by_author(self, author):

        result = []

        for book in self.books.values():

            if book.author == author:
                result.append(book)

        return result

    def oldest(self):

        if not self.books:
            return None

        oldest_book = None

        for book in self.books.values():

            if (
                oldest_book is None
                or book.year < oldest_book.year
            ):
                oldest_book = book

        return oldest_book

    def __len__(self):
        return len(self.books)


if __name__ == "__main__":

    print("Q4: LIBRARY SYSTEM")

    library = Library()

    books = [

        Book(
            "1984",
            "George Orwell",
            1949
        ),

        Book(
            "Animal Farm",
            "George Orwell",
            1945
        ),

        Book(
            "The Great Gatsby",
            "F. Scott Fitzgerald",
            1925
        ),

        EBook(
            "Dune",
            "Frank Herbert",
            1965,
            2.5
        ),

        EBook(
            "Foundation",
            "Isaac Asimov",
            1951,
            1.8
        )
    ]

    for book in books:
        library.add(book)

    # Add the same book again
    library.add(
        Book(
            "1984",
            "George Orwell",
            1949
        )
    )

    print("Number of books:", len(library))

    print(
        "Orwell:",
        [
            str(book)
            for book in library.find_by_author(
                "George Orwell"
            )
        ]
    )

    print("Oldest:", library.oldest())

    print(
        "Age of 1984:",
        books[0].age(2026)
    )

    print(
        "Dune download time:",
        books[3].download_seconds(10),
        "seconds"
    )

    print(
        "EBook example:",
        books[3]
    )