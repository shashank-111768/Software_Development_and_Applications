

def parse_ratings(data):
    movies = {}

    for item in data.split(","):
        item = item.strip()

        if ":" in item:
            title, number = item.split(":", 1)
            title = title.strip()
            rating = int(number.strip())

            if title not in movies:
                movies[title] = []

            movies[title].append(rating)

    return movies


def average_rating(movies, title):
    if title not in movies:
        return 0.0

    ratings = movies[title]
    return round(sum(ratings) / len(ratings), 1)


def best_movie(movies):
    best = ""
    best_average = -1

    for title in movies:
        average = average_rating(movies, title)

        if average > best_average:
            best = title
            best_average = average

    return best


def rating_counts(movies):
    counts = {}

    for title in movies:
        counts[title] = len(movies[title])

    return counts


if __name__ == "__main__":
    data = "Dune:8, Dune:9, Barbie:7, Dune:10, Barbie:9, Oppenheimer:9, Barbie:6"

    print("Q1: MOVIE RATINGS")

    movies = parse_ratings(data)

    print("Parsed movies:", movies)
    print("Dune average:", average_rating(movies, "Dune"))
    print("Barbie average:", average_rating(movies, "Barbie"))
    print("Oppenheimer average:", average_rating(movies, "Oppenheimer"))

    print("Unknown movie:", average_rating(movies, "Avatar"))

    print("Best movie:", best_movie(movies))
    print("Rating counts:", rating_counts(movies))

    # Extra whitespace test
    messy = "  Dune : 8 , Barbie : 9 , Dune : 10 "
    print("Extra spaces test:", parse_ratings(messy))