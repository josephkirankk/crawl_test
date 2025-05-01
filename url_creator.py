import urllib.parse

def build_shopping_url(query, num=100, start=0, hl='en', gl='us'):
    """
    Build a Google Shopping search URL for a given query.

    Parameters:
    - query (str): Your search terms.
    - num (int): Number of results to return (max 100).
    - start (int): Result offset for pagination.
    - hl (str): Interface language (ISO 639-1 code).
    - gl (str): Geolocation country code (ISO 3166-1 alpha-2).

    Returns:
    - str: A fully-formed Google Shopping URL.
    """
    base = 'https://www.google.com/search'
    # Encode the query, turning spaces into '+' per HTML form encoding
    q_encoded = urllib.parse.quote_plus(query)
    return (
        f"{base}?tbm=shop"
        f"&q={q_encoded}"
        f"&num={num}"
        f"&start={start}"
        f"&hl={hl}"
        f"&gl={gl}"
    )

# Example usage:
if __name__ == "__main__":
    print(build_shopping_url("low budget smartphone"))
    # => https://www.google.com/search?tbm=shop&q=low+budget+smartphone&num=100&start=0&hl=en&gl=us
