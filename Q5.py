"""Q5: Movie Review Extraction Pipeline (LLM + JSON)"""

import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Set to True to print the raw prompt + reply (to capture a transcript),
# then set back to False for normal runs.
DEBUG_TRANSCRIPT = False


def try_parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def ask_llm(prompt: str, system: str, temperature: float = 0) -> str:
    response = client.chat.completions.create(
        model="qwen3-0.6b",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    reply = response.choices[0].message.content
    if DEBUG_TRANSCRIPT:
        print("=" * 60)
        print("SYSTEM:", system)
        print("-" * 60)
        print("PROMPT:", prompt)
        print("-" * 60)
        print("RAW REPLY:", reply)
        print("=" * 60)
    return reply


def build_prompt(text: str) -> str:
    return (
        "Extract the movie review as a JSON object with exactly these keys: "
        '"title" (string), "rating" (integer 1-10), "sentiment" ("positive" or "negative"). '
        "Reply with ONLY the JSON object, nothing else.\n\n"
        f"Review: {text}"
    )


def extract_review(text: str) -> dict:
    system = "You extract structured data from movie reviews and reply with only JSON."
    reply = ask_llm(build_prompt(text), system)
    return try_parse_json(reply)


def check_review(d) -> str:
    if d is None:
        return "not valid JSON"
    if set(d.keys()) != {"title", "rating", "sentiment"}:
        return f"keys must be exactly title, rating, sentiment (got {list(d.keys())})"
    if not isinstance(d["title"], str) or not d["title"]:
        return "title must be a non-empty string"
    if isinstance(d["rating"], bool) or not isinstance(d["rating"], int):
        return "rating must be an integer"
    if not (1 <= d["rating"] <= 10):
        return "rating must be between 1 and 10"
    if d["sentiment"] not in ("positive", "negative"):
        return 'sentiment must be "positive" or "negative"'
    return ""


def extract_with_retry(text: str, max_attempts=3, temperature: float = 0):
    """
    Returns (result_dict_or_None, retries).
    retries = number of extra attempts beyond the first that were needed.
    """
    system = "You extract structured data from movie reviews and reply with only JSON."
    prompt = build_prompt(text)
    error = ""
    for attempt in range(max_attempts):
        if attempt > 0:
            prompt = (
                f"Your previous reply was invalid: {error}\n"
                f"Return corrected JSON with only the keys title, rating, sentiment.\n\n"
                f"Review: {text}"
            )
        reply = ask_llm(prompt, system, temperature=temperature)
        d = try_parse_json(reply)
        error = check_review(d)
        if error == "":
            return d, attempt  # attempt == number of retries used
    print(f"FAILED after {max_attempts} attempts: {text!r} -> {error}")
    return None, max_attempts


REVIEWS = [
    "Saw Dune yesterday — absolutely loved it, easily 9/10!",
    "Barbie was ok I guess. 6 out of 10",
    "Oppenheimer was a slow, boring mess. Would give it a 3.",
    "The Matrix still holds up. Gave it a nine.",
    "Cats (2019) was painful to watch. 1/10, avoid.",
]


def run_pipeline(temperature: float = 0):
    """Run all reviews at a given temperature. Returns (results, total_retries, failures)."""
    results = []
    total_retries = 0
    failures = 0
    for review in REVIEWS:
        d, retries = extract_with_retry(review, temperature=temperature)
        total_retries += retries
        if d is not None:
            results.append(d)
        else:
            failures += 1
    return results, total_retries, failures


if __name__ == "__main__":
    # --- Main pipeline (temperature = 0) ---
    results, retries, failures = run_pipeline(temperature=0)

    print(f"\n{'Title':<20} {'Rating':<8} {'Sentiment'}")
    print("-" * 40)
    for r in results:
        print(f"{r['title']:<20} {r['rating']:<8} {r['sentiment']}")

    pos = sum(1 for r in results if r["sentiment"] == "positive")
    neg = sum(1 for r in results if r["sentiment"] == "negative")
    print(f"\nPositive: {pos}  Negative: {neg}")

    # --- BONUS: temperature 0 vs 1.5 comparison ---
    print("\n" + "=" * 40)
    print("BONUS: temperature comparison")
    print("=" * 40)

    _, retries_0, fails_0 = run_pipeline(temperature=0)
    _, retries_15, fails_15 = run_pipeline(temperature=1.5)

    print(f"temperature=0.0 -> retries: {retries_0}, failures: {fails_0}")
    print(f"temperature=1.5 -> retries: {retries_15}, failures: {fails_15}")

# Bonus observation (based on the actual run):
    # In this run both temperature=0 and temperature=1.5 produced valid JSON on
    # the first attempt for all 5 reviews (0 retries, 0 failures each). The reviews
    # are short and unambiguous and the target schema is tiny and rigid, so even
    # high randomness left little room for malformed output. Temperature mainly
    # affects wording variety, and there are very few valid ways to write this JSON.
    # With messier reviews or a larger schema, temperature=1.5 would be expected to
    # cause more retries and failures than temperature=0.


# ============================================================================
# REAL TRANSCRIPT (captured from an actual run against LM Studio / qwen3-0.6b)
# ============================================================================
# SYSTEM: You extract structured data from movie reviews and reply with only JSON.
# PROMPT: Extract the movie review as a JSON object with exactly these keys:
#         "title" (string), "rating" (integer 1-10), "sentiment" ("positive" or
#         "negative"). Reply with ONLY the JSON object, nothing else.
#         Review: Saw Dune yesterday — absolutely loved it, easily 9/10!
# RAW REPLY: {"title":"Dune","rating":9,"sentiment":"positive"}
# ============================================================================