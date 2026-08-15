# 🔍 TrustRadius Reviews API: find the software alternatives buyers actually compared

> Every B2B review is an evaluation someone already ran. This API hands you the result: which software alternatives the buyer weighed, what they scored feature by feature, and what the purchase returned.

**Actor page:** [apify.com/johnvc/trustradius-reviews-api](https://apify.com/johnvc/trustradius-reviews-api?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/trustradius-reviews-api/input-schema](https://apify.com/johnvc/trustradius-reviews-api/input-schema?fpr=9n7kx3)

Most review data gives you a star and a paragraph. This one gives you the comparison. Point it at a product's review page and you get one clean JSON row per review, carrying `alternativesConsidered` (the software alternatives that buyer shortlisted, in their own words), `featureRatings` (per-feature numeric scores rather than a single average), `returnOnInvestment`, structured `pros` and `cons`, `likelihoodToRecommend`, and the reviewer's role, company size and industry so you can weight who is talking. That mix is what turns B2B software reviews into competitive intelligence instead of sentiment.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

Start with a product review page, for example `https://www.trustradius.com/products/gtm-workspace/reviews`, set `mode` to `product`, and cap `maxReviewsPerProduct` while you are experimenting. The run returns one row per review. Read `alternativesConsidered` first: that is where the software alternatives live, written by someone who ran the evaluation, and it names real rivals rather than the ones a marketing page chose to list. Then read `featureRatings`, an array of `{feature, rating}` pairs, which lets you line two products up dimension by dimension instead of comparing one overall score to another. `returnOnInvestment` and `likelihoodToRecommend` explain what the purchase actually did for that team, and `authorPosition`, `authorCompanySize` and `authorCompanyIndustry` let you separate an enterprise opinion from an SMB one. A concrete use: pass three products from a shortlist in a single run, pull `alternativesConsidered` from each, and you have a vendor comparison assembled from buyers instead of vendors. When you already hold individual review URLs, switch `mode` to `review` and pass them in `reviewUrls` to re-collect the same reviews on a schedule.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-TrustRadius-Reviews-API.git
   cd Apify-TrustRadius-Reviews-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python trustradius-reviews-api-example.py
   ```

### The three recipes in this repo

| Command | What it does |
|---|---|
| `uv run python trustradius-reviews-api-example.py` | Cheapest start: one product review page, one review, one page. |
| `uv run python trustradius-reviews-api-example.py --example alternatives` | Three products in one run, so you can read the software alternatives and feature scores side by side. |
| `uv run python trustradius-reviews-api-example.py --example review-urls` | Review mode: collect specific review URLs, one review each. Add `--url <review-url>` to point it somewhere else. |

Every recipe sets `maxReviewsPerProduct` to 1 on purpose. Billing is per review returned, so that field is your cost dial; raise it once you know your budget.

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python trustradius-reviews-api-example.py
```

## Why Use This TrustRadius Reviews API?

**It answers the software alternatives question directly.** Buyers looking for alternatives to their current software normally get a listicle. `alternativesConsidered` is different: it is a written head-to-head from someone who shortlisted the same products and had to pick one. In a live run against GTM Workspace, that field came back as a paragraph naming a rival by name and explaining exactly which pricing and feature gaps decided it.

**Feature-level comparison, not star-level.** `featureRatings` returns an array of feature names with numeric scores from that reviewer, typically a dozen or more per review. Two products compared on twelve dimensions is a real evaluation. Two products compared on one average is a coin flip.

**Reviewer context so you can weight the opinion.** `authorPosition`, `authorCompanySize`, `authorCompanyIndustry` and `authorExperienceYears` tell you whether the reviewer is an admin at a fifty-person shop or an engineer at an enterprise. `authorIncentivized` tells you whether they were given something for writing it, which matters when you are aggregating.

**Business outcomes in plain language.** `returnOnInvestment`, `efficienciesGained` and `likelihoodToRenew` describe what the tool changed for that team. That is the material a business case is built from, and it is usually stuck in prose that nobody has time to read at volume.

**Built for agents.** Every review row carries a one-line `summary`, so a model can read a record without post-processing, and the Actor is MCP-ready for Claude, Cursor and ChatGPT (install sections below).

## Features

### Core Capabilities
- Two modes: `product` discovers reviews from a product's review page, `review` collects individual review URLs
- Up to 50 product URLs per run, or up to 500 review URLs per run
- `maxReviewsPerProduct` (1 to 2000) and `pages` (1 to 25) control depth and cost
- One flat JSON row per review, exportable as JSON, CSV or Excel
- Two ready-made dataset views in the Apify Console: **Reviews overview** and **Competitive comparisons**

### Data Quality
- Ratings are on the source's 1 to 10 scale, and the `summary` line says so to avoid confusion with a 5 star scale
- `pros` and `cons` come back as discrete arrays, not one blob
- An input that returns nothing produces a row with `result_type: "error"` and a plain-language `error_message`, so a failure never looks like an empty success
- Billing is per review returned, so an input that yields nothing costs nothing

## Usage Examples

### Basic Example
```json
{
  "mode": "product",
  "productUrls": ["https://www.trustradius.com/products/gtm-workspace/reviews"],
  "maxReviewsPerProduct": 1,
  "pages": 1
}
```

### Advanced Example
```json
{
  "mode": "product",
  "productUrls": [
    "https://www.trustradius.com/products/asana/reviews",
    "https://www.trustradius.com/products/hubspot-crm/reviews",
    "https://www.trustradius.com/products/gtm-workspace/reviews"
  ],
  "maxReviewsPerProduct": 25,
  "pages": 3
}
```

### Review mode
```json
{
  "mode": "review",
  "reviewUrls": [
    "https://www.trustradius.com/reviews/zoominfo-sales-2026-04-10-06-11-40"
  ]
}
```

**Schedule tip:** save any of these inputs as a Task in the Apify Console and [schedule it](https://apify.com/johnvc/trustradius-reviews-api?fpr=9n7kx3) to run weekly over a fixed product list. Each new review adds a fresh `alternativesConsidered` paragraph and a fresh `featureRatings` array, so the week over week diff is a real competitive signal rather than a website changelog.

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `mode` | `str` | YES | `review` | `product` discovers all reviews for a product. `review` collects specific review URLs, one review each. |
| `productUrls` | `list[str]` | in `product` mode | - | Product review pages or bare product slugs. Up to 50 per run. The full `.../products/<slug>/reviews` form is the most reliable. |
| `reviewUrls` | `list[str]` | in `review` mode | - | Individual review URLs. Up to 500 per run. URLs that return nothing are not charged. |
| `maxReviewsPerProduct` | `int` | no | `50` | Reviews to return per product in `product` mode. Range 1 to 2000. This is your cost control. |
| `pages` | `int` | no | - | How many pages of a product's review list to walk in `product` mode. Range 1 to 25. Higher values reach older reviews. |

## Output Format

One row per review. Real fields from a live run on 2026.08.08, with the long prose fields trimmed here for readability:

```json
{
  "result_type": "review",
  "reviewId": "zoominfo-sales-2026-04-10-06-11-40",
  "productId": "gtm-workspace",
  "productName": "GTM Workspace Powered by ZoomInfo",
  "productUrl": "https://www.trustradius.com/products/gtm-workspace/reviews",
  "reviewUrl": "https://www.trustradius.com/reviews/zoominfo-sales-2026-04-10-06-11-40",
  "reviewTitle": "Zoom Info Pros and Cons from 2 Year User.",
  "reviewRating": 8,
  "reviewDate": "2026-07-13T12:38:49.917Z",
  "alternativesConsidered": "When I talk about ZoomInfo stacking up against the software that I have selected above, I'll say that ZoomInfo lacks a lot of features when it comes to the comparison of price and features...",
  "productsReplaced": false,
  "featureRatings": [
    { "feature": "Advanced search", "rating": 8 },
    { "feature": "Identification of new leads", "rating": 8 },
    { "feature": "List quality", "rating": 7 },
    { "feature": "Ideal customer targeting", "rating": 8 }
  ],
  "ratings": { "usability": 7 },
  "returnOnInvestment": "Now, the positive impact that ZoomInfo has made on our sales pipeline...",
  "pros": ["The very first example of what ZoomInfo sales does particularly well is providing the correct scope and intent for current initiatives in an organization."],
  "cons": ["The areas for ZoomInfo that require improvement are, first, the Chrome extension. It lags a lot."],
  "likelihoodToRecommend": "A scenario wherein ZoomInfo Sales is well-suited, as I said, is good for giving you the details, the intent, and scope for a specific person...",
  "reviewAuthor": "Karan Rajput",
  "authorPosition": "Growth Specialist",
  "authorCompanyName": "Aress Software & Education Technologies",
  "authorCompanyIndustry": "Information Technology & Services",
  "authorCompanySize": "501-1000 employees",
  "authorExperienceYears": 2,
  "authorLabels": ["Vetted Review", "Verified User"],
  "authorIncentivized": true,
  "summary": "8-out-of-10 review of GTM Workspace Powered by ZoomInfo from Growth Specialist: \"Zoom Info Pros and Cons from 2 Year User.\"",
  "fetched_at": "2026-08-09T00:57:47.988695+00:00"
}
```

Rows also carry `prosAndCons`, `useCasesAndScope`, `efficienciesGained`, `startDate` and `updatedDate`. Several further fields in the schema, including `keyDifferentiators`, `otherSoftwareUsed`, `businessProcessesSupported`, `likelihoodToRenew`, `usabilityPros`, `usabilityCons`, `supportPros`, `supportCons`, `implementationPartner` and `implementationIssues`, appear only when that reviewer filled in that part of the form, so treat them as a bonus rather than a guarantee. Full field list: [the Actor's Store page](https://apify.com/johnvc/trustradius-reviews-api?fpr=9n7kx3).

## People also search for

### What are good alternatives to our current software?

Collect reviews for the product you use today and read `alternativesConsidered` on each row. Every populated entry is a buyer naming what else they evaluated and saying why they went the way they went, which is a shortlist built from evaluations rather than from a listicle.

### How do I compare B2B software vendors on real user reviews?

Pass the shortlist as `productUrls` in one `product` mode run, then compare `featureRatings` feature by feature and `ratings` for usability, support and implementation. The `alternatives` recipe in this repo does exactly that for three products: `uv run python trustradius-reviews-api-example.py --example alternatives`.

### Which products do buyers replace most often?

`productsReplaced` is a boolean on every row, so you can filter for reviews describing a switch and then read `alternativesConsidered` on those rows to see what got displaced. Collect a decent volume before drawing conclusions; on small samples the flag is often false across the board.

### How do I get per feature ratings for software products?

`featureRatings` is an array of `{feature, rating}` objects taken from the reviewer's own scoring, usually a dozen or more entries per review. Group it by `feature` across many reviews and you have a per-feature average that no single overall score can give you.

### Is there a TrustRadius API I can call from Python?

The official route sits behind a vendor account. This Actor is a self-serve alternative: any public product review page works as input, you call it with the Apify Python client shown in Quick Start, and you pay per review returned with no start fee.

### Can I use this with MCP or Claude?

Yes. Use the install sections below to add the Actor as an MCP tool in [Claude Code](https://claude.ai/referral/uIlpa7nPLg) (free trial), [Claude Cowork](https://claude.ai/referral/uIlpa7nPLg) (free trial), Claude.ai, Cursor or ChatGPT, then ask your agent what these buyers compared the product against.

### Why did a product return an error row instead of reviews?

Product pages are not uniformly readable, and a few products fail even when others work. When that happens you get a row with `result_type: "error"` and a plain-language `error_message` rather than a silent empty result, and you are not charged for it. Try the full `.../products/<slug>/reviews` URL rather than a bare slug, and fall back to `review` mode with individual review URLs.

---

<!-- The five install sections below embed hosted screenshots from ApifyPublicData/assets/guides. -->

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the TrustRadius Reviews API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the TrustRadius Reviews API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the TrustRadius Reviews API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/trustradius-reviews-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api`, using OAuth when prompted.
5. Ask Claude to run the TrustRadius Reviews API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the TrustRadius Reviews API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/trustradius-reviews-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

## Related APIs

- [G2 Reviews API](https://apify.com/johnvc/g2-reviews-api?fpr=9n7kx3) for the other major B2B software review source
- [Trustpilot Reviews API](https://apify.com/johnvc/trustpilot-reviews-api?fpr=9n7kx3) for consumer-facing business reviews
- [Glassdoor Reviews API](https://apify.com/johnvc/glassdoor-reviews-api?fpr=9n7kx3) for employer reviews
- [Owler Company Intelligence API](https://apify.com/johnvc/owler-company-api?fpr=9n7kx3) for the vendor's own competitor set

---

## 🌐 About Alpha OSINT

This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.
For support or requests for this actor, please start a ticket [directly on our support page](https://apify.com/johnvc/trustradius-reviews-api/issues/open?fpr=9n7kx3).

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the TrustRadius Reviews API to turn B2B software reviews into a comparison you can act on.*

Last Updated: 2026.08.15
