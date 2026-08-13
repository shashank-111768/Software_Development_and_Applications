"""
Q1: Movie Ratings (Lists and Strings)
Parse movie ratings from a string, calculate averages, find best movie, count ratings.
"""

def parse_ratings(data: str) -> list:

    ratings = []
    entries = data.split(",")
    for entry in entries:
        entry = entry.strip()
        if ":" in entry:
            title, rating_str = entry.split(":")
            title = title.strip()
            rating = int(rating_str.strip())
            ratings.append((title, rating))
    return ratings


def average_rating(ratings: list, title: str) -> float:
    
    movie_ratings = [rating for t, rating in ratings if t == title]
    if not movie_ratings:
        return 0.0
    return round(sum(movie_ratings) / len(movie_ratings), 1)


def best_movie(ratings: list) -> str:
    
    if not ratings:
        return ""
    
    movies = {}
    for title, rating in ratings:
        if title not in movies:
            movies[title] = []
        movies[title].append(rating)
    
    # Calculate averages
    averages = {title: sum(rs) / len(rs) for title, rs in movies.items()}
    
    # Return title with highest average
    return max(averages, key=averages.get) # type: ignore


def rating_counts(ratings: list) -> dict:
   
    counts = {}
    for title, rating in ratings:
        counts[title] = counts.get(title, 0) + 1
    return counts


# ============================================================================
# DEMO BLOCK
# ============================================================================

if __name__ == "__main__":
    data = "Dune:8, Dune:9, Barbie:7, Dune:10, Barbie:9, Oppenheimer:9, Barbie:6"
    
    print("=" * 60)
    print("Q1: MOVIE RATINGS DEMO")
    print("=" * 60)
    
    print("\n1. RAW DATA:")
    print(f"   {data}")
    
    # Parse ratings
    ratings = parse_ratings(data)
    print("\n2. PARSED RATINGS (list of tuples):")
    print(f"   {ratings}")
    
    # Average rating for each movie
    print("\n3. AVERAGE RATINGS:")
    for movie in ["Dune", "Barbie", "Oppenheimer"]:
        avg = average_rating(ratings, movie)
        print(f"   {movie}: {avg}")
    
    # Unknown movie
    print(f"   Unknown Movie: {average_rating(ratings, 'Avatar')}")
    
    # Best movie
    best = best_movie(ratings)
    print(f"\n4. BEST MOVIE (highest average):")
    print(f"   {best}")
    
    # Rating counts
    counts = rating_counts(ratings)
    print(f"\n5. RATING COUNTS (per movie):")
    for movie, count in sorted(counts.items()):
        print(f"   {movie}: {count} ratings")
    
    print("\n" + "=" * 60)
    print("TEST: Extra whitespace handling")
    print("=" * 60)
    data_messy = "  Dune  : 8 , Barbie : 9  , Dune : 10  "
    ratings_messy = parse_ratings(data_messy)
    print(f"Messy data: {data_messy}")
    print(f"Parsed:     {ratings_messy}")