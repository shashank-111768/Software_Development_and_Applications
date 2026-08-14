
import json
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


# Set to True if you want to print the prompt and raw model reply.
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
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
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
        '"title" (string), "rating" (integer 1-10), '
        '"sentiment" ("positive" or "negative"). '
        "Reply with ONLY the JSON object, nothing else.\n\n"
        f"Review: {text}"
    )


def extract_review(text: str) -> dict:

    system = (
        "You extract structured data from movie reviews "
        "and reply with only JSON."
    )

    reply = ask_llm(
        build_prompt(text),
        system
    )

    return try_parse_json(reply)


def check_review(d) -> str:

    if d is None:
        return "not valid JSON"

    if set(d.keys()) != {
        "title",
        "rating",
        "sentiment"
    }:
        return (
            "keys must be exactly title, rating, sentiment "
            f"(got {list(d.keys())})"
        )

    if not isinstance(d["title"], str) or not d["title"]:
        return "title must be a non-empty string"

    if isinstance(d["rating"], bool) or not isinstance(d["rating"], int):
        return "rating must be an integer"

    if not (1 <= d["rating"] <= 10):
        return "rating must be between 1 and 10"

    if d["sentiment"] not in (
        "positive",
        "negative"
    ):
        return 'sentiment must be "positive" or "negative"'

    return ""


def extract_with_retry(
    text: str,
    max_attempts=3,
    temperature: float = 0
):

    """
    Returns:
        (result_dictionary, retries)

    retries = number of extra attempts needed
    after the first attempt.
    """

    system = (
        "You extract structured data from movie reviews "
        "and reply with only JSON."
    )

    prompt = build_prompt(text)

    error = ""

    for attempt in range(max_attempts):

        if attempt > 0:

            prompt = (
                f"Your previous reply was invalid: {error}\n"
                "Return corrected JSON with only the keys "
                "title, rating, sentiment.\n\n"
                f"Review: {text}"
            )

        reply = ask_llm(
            prompt,
            system,
            temperature=temperature
        )

        d = try_parse_json(reply)

        error = check_review(d)

        if error == "":
            return d, attempt

    print(
        f"FAILED after {max_attempts} attempts: "
        f"{text!r} -> {error}"
    )

    return None, max_attempts


# ------------------------------------------------------------
# Movie reviews
# ------------------------------------------------------------

REVIEWS = [

    "Saw Dune yesterday — absolutely loved it, easily 9/10!",

    "Barbie was ok I guess. 6 out of 10",

    "Liger was disappointing. I would give it a 3 out of 10.",

    "Akhanda was exciting and entertaining. "
    "I would give it an 8 out of 10.",

    "Tenet was confusing at first, but I enjoyed it. "
    "I would give it a 7 out of 10."

]


def run_pipeline(temperature: float = 0):

    """
    Run all reviews at a selected temperature.

    Returns:
        results
        total_retries
        failures
    """

    results = []

    total_retries = 0

    failures = 0

    for review in REVIEWS:

        d, retries = extract_with_retry(
            review,
            temperature=temperature
        )

        total_retries += retries

        if d is not None:
            results.append(d)

        else:
            failures += 1

    return (
        results,
        total_retries,
        failures
    )


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------

if __name__ == "__main__":

    # Main pipeline using temperature 0

    results, retries, failures = run_pipeline(
        temperature=0
    )

    print()

    print(
        f"{'Title':<20} "
        f"{'Rating':<8} "
        f"{'Sentiment'}"
    )

    print("-" * 40)

    for r in results:

        print(
            f"{r['title']:<20} "
            f"{r['rating']:<8} "
            f"{r['sentiment']}"
        )


    # Count positive and negative reviews

    pos = sum(
        1
        for r in results
        if r["sentiment"] == "positive"
    )

    neg = sum(
        1
        for r in results
        if r["sentiment"] == "negative"
    )


    print()

    print(
        f"Positive: {pos}  "
        f"Negative: {neg}"
    )


    # --------------------------------------------------------
    # BONUS: temperature comparison
    # --------------------------------------------------------

    print("\n" + "=" * 40)

    print("BONUS: temperature comparison")

    print("=" * 40)


    # Temperature 0

    _, retries_0, fails_0 = run_pipeline(
        temperature=0
    )


    # Temperature 1.5

    _, retries_15, fails_15 = run_pipeline(
        temperature=1.5
    )


    print(
        f"temperature=0.0 -> "
        f"retries: {retries_0}, "
        f"failures: {fails_0}"
    )


    print(
        f"temperature=1.5 -> "
        f"retries: {retries_15}, "
        f"failures: {fails_15}"
    )