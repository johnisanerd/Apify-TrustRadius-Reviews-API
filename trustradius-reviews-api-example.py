"""TrustRadius Reviews API: a quick start example.

See more at: https://apify.com/johnvc/trustradius-reviews-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/trustradius-reviews-api/input-schema?fpr=9n7kx3

This script calls the TrustRadius Reviews API on Apify from Python and reads its
structured JSON output. Every run returns one row per review, and the row that
matters most is `alternativesConsidered`: the software alternatives the buyer
weighed the product against, written by the buyer. Alongside it you get
`featureRatings` (per-feature numeric scores), `returnOnInvestment`, `pros`,
`cons`, `likelihoodToRecommend`, and the reviewer's role, company size and
industry.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python trustradius-reviews-api-example.py
  uv run python trustradius-reviews-api-example.py --example alternatives
  uv run python trustradius-reviews-api-example.py --example review-urls
  uv run python trustradius-reviews-api-example.py --example review-urls --url https://www.trustradius.com/reviews/<review-slug>
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/trustradius-reviews-api"

# Product review pages are the easiest way in: you almost never have individual
# review URLs on hand, but you always know which products you care about.
# Pass the full ".../products/<slug>/reviews" form; a bare slug is less reliable.
PRODUCT_URL = "https://www.trustradius.com/products/gtm-workspace/reviews"
SHORTLIST_URLS = [
    "https://www.trustradius.com/products/asana/reviews",
    "https://www.trustradius.com/products/hubspot-crm/reviews",
    "https://www.trustradius.com/products/gtm-workspace/reviews",
]
# Review mode takes individual review URLs. You normally harvest these from the
# `reviewUrl` field of a product-mode run, then pin them for repeat collection.
SAMPLE_REVIEW_URL = "https://www.trustradius.com/reviews/zoominfo-sales-2026-04-10-06-11-40"


def _short(value: Any, limit: int = 220) -> str:
    """Trim a value to one readable line.

    Args:
        value: Any field value from a dataset row.
        limit: Maximum characters to keep.

    Returns:
        A single-line string, truncated with an ellipsis when long.
    """
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a readable summary of the review rows a run returned.

    Args:
        items: Rows from the Actor's default dataset. Each row carries a
            `result_type` of "review" or "error".
    """
    reviews = [row for row in items if row.get("result_type") == "review"]
    errors = [row for row in items if row.get("result_type") == "error"]
    print(f"Returned {len(items)} row(s): {len(reviews)} review(s), {len(errors)} error row(s).\n")

    for row in reviews:
        print("=" * 72)
        print(f"Product        : {row.get('productName')}")
        print(f"Review         : {row.get('reviewTitle')}")
        print(f"Rating         : {row.get('reviewRating')} out of 10")
        print(f"Reviewer       : {row.get('authorPosition')} at a {row.get('authorCompanySize')} company")
        print(f"Industry       : {row.get('authorCompanyIndustry')}")
        print(f"Incentivized   : {row.get('authorIncentivized')}")
        print(f"Replaced a tool: {row.get('productsReplaced')}")

        # The headline field: which software alternatives this buyer compared,
        # and why they landed where they did.
        alternatives = row.get("alternativesConsidered")
        if alternatives:
            print(f"Alternatives   : {_short(alternatives)}")

        # Per-feature numeric scores, as an array of {feature, rating}.
        feature_ratings = row.get("featureRatings") or []
        if feature_ratings:
            scored = ", ".join(
                f"{entry.get('feature')} {entry.get('rating')}" for entry in feature_ratings[:5]
            )
            print(f"Feature scores : {scored}")

        # Usability, support and implementation scores, gathered into one object.
        ratings = row.get("ratings") or {}
        if ratings:
            print(f"Scored aspects : {ratings}")

        roi = row.get("returnOnInvestment")
        if roi:
            print(f"ROI notes      : {_short(roi)}")

        pros = row.get("pros") or []
        cons = row.get("cons") or []
        if pros:
            print(f"Pros           : {_short(' | '.join(str(p) for p in pros))}")
        if cons:
            print(f"Cons           : {_short(' | '.join(str(c) for c in cons))}")

        recommend = row.get("likelihoodToRecommend")
        if recommend:
            print(f"Would recommend: {_short(recommend)}")

        print(f"Review URL     : {row.get('reviewUrl')}")
        print()

    for row in errors:
        print(f"[error] {row.get('sourceUrl')}: {row.get('error_message')}")


def _run(client: ApifyClient, run_input: dict[str, Any]) -> None:
    """Call the Actor and print what came back.

    Args:
        client: An authenticated Apify client.
        run_input: The Actor input, matching the published input schema.
    """
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")

    # apify-client 3.x returns a typed Run object, so read the attribute.
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_default(client: ApifyClient) -> None:
    """Cheapest starting point: one product, one review, one page."""
    # Billing is per review returned, so maxReviewsPerProduct is the cost dial.
    # It is set to 1 here to keep this first run inexpensive. Raise it once you
    # have your own API key and know your budget.
    run_input: dict[str, Any] = {
        "mode": "product",
        "productUrls": [PRODUCT_URL],
        "maxReviewsPerProduct": 1,
        "pages": 1,
    }
    _run(client, run_input)


def run_alternatives(client: ApifyClient) -> None:
    """Put a shortlist side by side and read the software alternatives buyers named.

    Three product review pages in one request. Each row carries
    `alternativesConsidered` and `featureRatings`, which is the raw material for
    a vendor comparison built from real evaluations rather than marketing pages.
    """
    # Still one review per product to keep the demo cheap. Product mode accepts
    # up to 50 product URLs and up to 2000 reviews per product.
    run_input: dict[str, Any] = {
        "mode": "product",
        "productUrls": SHORTLIST_URLS,
        "maxReviewsPerProduct": 1,
        "pages": 1,
    }
    _run(client, run_input)


def run_review_urls(client: ApifyClient, url: str | None = None) -> None:
    """Collect specific review URLs, one review each.

    Use this when you already hold review URLs, for example after harvesting the
    `reviewUrl` field from a product-mode run, and you want to re-collect the
    same reviews on a schedule. Review mode accepts up to 500 URLs per run.
    """
    run_input: dict[str, Any] = {
        "mode": "review",
        "reviewUrls": [url or SAMPLE_REVIEW_URL],
    }
    _run(client, run_input)


def main() -> None:
    """Dispatch one of the example recipes."""
    parser = argparse.ArgumentParser(description="TrustRadius Reviews API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=["default", "alternatives", "review-urls"],
        help="Which recipe to run. See the README for what each one returns.",
    )
    parser.add_argument(
        "--url",
        default=None,
        help="Override the review URL used by the review-urls recipe.",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit(
            "Set APIFY_API_TOKEN in .env or the environment. "
            "Get a free key at https://apify.com?fpr=9n7kx3"
        )

    client = ApifyClient(token)

    if args.example == "default":
        run_default(client)
    elif args.example == "alternatives":
        run_alternatives(client)
    else:
        run_review_urls(client, args.url)


if __name__ == "__main__":
    main()
