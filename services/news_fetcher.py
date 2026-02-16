# services/news_fetcher.py
import feedparser
import re
from datetime import datetime
from bs4 import BeautifulSoup


# ── RSS FEEDS FOR EACH COUNTRY ──────────────────────────────────────

COUNTRY_FEEDS = {
    # ── ASIA ──
    'in': {
        'name': 'India',
        'feeds': [
            'https://feeds.feedburner.com/ndtvnews-top-stories',
            'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
        ]
    },
    'cn': {
        'name': 'China',
        'feeds': [
            'http://www.chinadaily.com.cn/rss/china_rss.xml',
        ]
    },
    'jp': {
        'name': 'Japan',
        'feeds': [
            'https://www3.nhk.or.jp/rss/news/cat0.xml',
        ]
    },
    'pk': {
        'name': 'Pakistan',
        'feeds': [
            'https://www.dawn.com/feed',
        ]
    },
    'sg': {
        'name': 'Singapore',
        'feeds': [
            'https://www.straitstimes.com/news/singapore/rss.xml',
        ]
    },

    # ── EUROPE ──
    'gb': {
        'name': 'United Kingdom',
        'feeds': [
            'https://feeds.bbci.co.uk/news/uk/rss.xml',
        ]
    },
    'de': {
        'name': 'Germany',
        'feeds': [
            'https://rss.dw.com/rdf/rss-en-ger',
        ]
    },
    'fr': {
        'name': 'France',
        'feeds': [
            'https://www.france24.com/en/rss',
        ]
    },

    # ── NORTH AMERICA ──
    'us': {
        'name': 'United States',
        'feeds': [
            'https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
        ]
    },
    'ca': {
        'name': 'Canada',
        'feeds': [
            'https://www.cbc.ca/cmlink/rss-topstories',
        ]
    },

    # ── SOUTH AMERICA ──
    'br': {
        'name': 'Brazil',
        'feeds': [
            'https://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
        ]
    },

    # ── AFRICA ──
    'ng': {
        'name': 'Nigeria',
        'feeds': [
            'https://www.aljazeera.com/xml/rss/all.xml',
        ]
    },
    'za': {
        'name': 'South Africa',
        'feeds': [
            'https://www.aljazeera.com/xml/rss/all.xml',
        ]
    },

    # ── OCEANIA ──
    'au': {
        'name': 'Australia',
        'feeds': [
            'https://www.abc.net.au/news/feed/51120/rss.xml',
        ]
    },
    'nz': {
        'name': 'New Zealand',
        'feeds': [
            'https://www.rnz.co.nz/rss/national.xml',
        ]
    },
}


# ── HELPER: CLEAN HTML TAGS FROM TEXT ───────────────────────────────
def clean_text(text):
    """Remove HTML tags and clean up text"""
    if not text:
        return ''
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    clean = soup.get_text()
    # Remove extra whitespace
    clean = ' '.join(clean.split())
    return clean.strip()


# ── HELPER: SAFE TEXT FOR JAVASCRIPT ────────────────────────────────
def safe_for_js(text):
    """
    Make text safe to use inside JavaScript strings.
    Removes characters that would break JS like quotes and newlines.
    """
    if not text:
        return ''
    # Replace single quotes, double quotes, backticks, newlines
    text = text.replace("'", " ")
    text = text.replace('"', " ")
    text = text.replace('`', " ")
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\\', ' ')
    return text.strip()


# ── HELPER: EXTRACT BEST SUMMARY ────────────────────────────────────
def extract_summary(entry):
    """
    Try multiple fields to get the best summary.
    RSS feeds store summaries in different fields.
    """
    # Try these fields in order
    possible_fields = [
        entry.get('summary', ''),
        entry.get('description', ''),
        entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '',
        entry.get('subtitle', ''),
    ]

    for text in possible_fields:
        cleaned = clean_text(text)
        # Only use if it has meaningful content (more than 20 characters)
        if cleaned and len(cleaned) > 20:
            # Limit to 250 characters so it stays short and readable
            if len(cleaned) > 250:
                # Cut at last complete word within 250 chars
                cleaned = cleaned[:250].rsplit(' ', 1)[0] + '...'
            return cleaned

    # If nothing found, create a summary from the title
    title = clean_text(entry.get('title', ''))
    if title:
        return f"Read the full story about: {title}"

    return "Summary not available for this article. Click Full Article to read more."


# ── HELPER: FORMAT TIME ──────────────────────────────────────────────
def format_time(entry):
    """Get and format published time from RSS entry"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            return dt.strftime('%B %d, %Y %I:%M %p')
    except:
        pass
    return 'Recently published'

# ── HELPER: DETECT ARTICLE CATEGORY ─────────────────────────────────
def detect_category(title, summary):
    """
    Automatically detect category based on keywords
    in the article title and summary.
    """

    # Combine title and summary for better detection
    text = (title + ' ' + summary).lower()

    # Define keywords for each category
    categories = {
        'Politics': [
            'government', 'election', 'president', 'minister', 'parliament',
            'political', 'party', 'vote', 'democracy', 'policy', 'senate',
            'congress', 'prime minister', 'cabinet', 'diplomat', 'treaty',
            'legislation', 'opposition', 'ruling', 'constitution', 'coup'
        ],
        'Business': [
            'economy', 'market', 'stock', 'trade', 'business', 'company',
            'bank', 'finance', 'investment', 'gdp', 'inflation', 'startup',
            'revenue', 'profit', 'loss', 'industry', 'export', 'import',
            'currency', 'oil', 'price', 'fund', 'billion', 'million'
        ],
        'Technology': [
            'technology', 'tech', 'ai', 'artificial intelligence', 'software',
            'internet', 'cyber', 'digital', 'app', 'smartphone', 'computer',
            'robot', 'data', 'hack', 'social media', 'startup', 'innovation',
            'satellite', 'space', 'electric', 'ev', 'tesla', 'google', 'apple'
        ],
        'Sports': [
            'cricket', 'football', 'soccer', 'tennis', 'basketball', 'sport',
            'olympic', 'tournament', 'championship', 'match', 'player', 'team',
            'fifa', 'ipl', 'league', 'coach', 'athlete', 'medal', 'race',
            'hockey', 'baseball', 'rugby', 'golf', 'swimming', 'boxing'
        ],
        'Health': [
            'health', 'hospital', 'doctor', 'medicine', 'disease', 'virus',
            'vaccine', 'covid', 'cancer', 'mental health', 'drug', 'treatment',
            'pandemic', 'epidemic', 'patient', 'surgery', 'medical', 'who',
            'diabetes', 'nutrition', 'fitness', 'wellness', 'pharmacy'
        ],
        'Education': [
            'education', 'school', 'university', 'student', 'teacher',
            'college', 'learning', 'exam', 'degree', 'scholarship', 'course',
            'academic', 'research', 'study', 'campus', 'graduate', 'literacy',
            'curriculum', 'tuition', 'admission', 'professor', 'faculty'
        ],
        'Environment': [
            'climate', 'environment', 'pollution', 'global warming', 'flood',
            'earthquake', 'storm', 'weather', 'forest', 'wildlife', 'ocean',
            'carbon', 'emission', 'renewable', 'solar', 'drought', 'fire',
            'plastic', 'recycling', 'green', 'sustainability', 'nature'
        ],
        'Crime': [
            'crime', 'police', 'arrest', 'murder', 'theft', 'fraud',
            'corruption', 'court', 'judge', 'prison', 'sentence', 'terror',
            'attack', 'violence', 'protest', 'riot', 'shooting', 'robbery',
            'investigation', 'drug trafficking', 'smuggling', 'accused'
        ],
    }

    # Check each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category

    # Default category if nothing matched
    return 'General'

# ── MAIN FUNCTION: FETCH NEWS FOR A COUNTRY ─────────────────────────
def fetch_news(country_code, max_articles=10):
    """
    Fetch news articles for a given country code.
    Returns a list of article dictionaries.
    """

    # Check if we have feeds for this country
    if country_code not in COUNTRY_FEEDS:
        return []

    country_data = COUNTRY_FEEDS[country_code]
    all_articles = []

    # Loop through each RSS feed for this country
    for feed_url in country_data['feeds']:
        try:
            print(f"  → Fetching: {feed_url}")

            # Parse the RSS feed
            feed = feedparser.parse(feed_url)

            # Check if feed was fetched successfully
            if feed.bozo and not feed.entries:
                print(f"  ✗ Failed to fetch: {feed_url}")
                continue

            print(f"  ✓ Got {len(feed.entries)} articles")

            # Loop through each news entry
            for entry in feed.entries[:6]:

                # Get and clean title
                title = clean_text(entry.get('title', 'No title available'))

                # Get best available summary
                summary = extract_summary(entry)

                # Get article URL
                url = entry.get('link', '#')

                # Get published time
                published = format_time(entry)

                # Get source name
                source = feed.feed.get('title', 'Unknown Source')

                # Make text safe for JavaScript (fixes Read Aloud bug)
                safe_title = safe_for_js(title)
                safe_summary = safe_for_js(summary)

                # Detect category automatically
                category = detect_category(title, summary)

                # Build article dictionary
                article = {
                    'title': title,           # Original title for display
                    'summary': summary,        # Original summary for display
                    'safe_title': safe_title,  # Safe title for JavaScript
                    'safe_summary': safe_summary, # Safe summary for JavaScript
                    'url': url,
                    'published': published,
                    'source': source,
                    'category': category, 
                    'country': country_data['name'],
                    'country_code': country_code,
                }

                all_articles.append(article)

        except Exception as e:
            print(f"  ✗ Error fetching {feed_url}: {e}")
            continue

    print(f"Total articles fetched: {len(all_articles)}")
    return all_articles[:max_articles]