# app.py
from flask import Flask, render_template, jsonify
from config import Config
from services.news_fetcher import fetch_news

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# ── TEMPLATE HELPER FUNCTIONS ────────────────────────────────────────

def category_emoji(category):
    """Returns an emoji for each category"""
    emojis = {
        'Politics':    '🏛️',
        'Business':    '💼',
        'Technology':  '💻',
        'Sports':      '⚽',
        'Health':      '🏥',
        'Education':   '📚',
        'Environment': '🌿',
        'Crime':       '⚖️',
        'General':     '📰',
    }
    return emojis.get(category, '📰')


def category_color(category):
    """Returns a Bootstrap color for each category badge"""
    colors = {
        'Politics':    'danger',
        'Business':    'success',
        'Technology':  'info',
        'Sports':      'warning',
        'Health':      'danger',
        'Education':   'primary',
        'Environment': 'success',
        'Crime':       'dark',
        'General':     'secondary',
    }
    return colors.get(category, 'secondary')


# Register as Jinja2 template filters
app.jinja_env.globals['category_emoji'] = category_emoji
app.jinja_env.globals['category_color'] = category_color


# ── ROUTES ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Homepage - shows all continents"""
    continents = app.config['CONTINENTS']
    return render_template('index.html', continents=continents)


@app.route('/continent/<continent_name>')
def continent(continent_name):
    continents = app.config['CONTINENTS']

    if continent_name not in continents:
        return "Page not found", 404

    continent_data = continents[continent_name]
    return render_template('continent.html',
                           continent=continent_data,
                           continent_key=continent_name)


@app.route('/country/<continent_name>/<country_code>')
def country(continent_name, country_code):
    continents = app.config['CONTINENTS']

    if continent_name not in continents:
        return "Page not found", 404

    continent_data = continents[continent_name]

    if country_code not in continent_data['countries']:
        return "Page not found", 404

    # ← Updated: country is now a dict with name and flag
    country_info = continent_data['countries'][country_code]
    country_name = country_info['name']
    country_flag = country_info['flag']

    print(f"Fetching news for: {country_name} ({country_code})")
    articles = fetch_news(country_code, max_articles=10)

    return render_template('country.html',
                           country_name=country_name,
                           country_flag=country_flag,
                           country_code=country_code,
                           continent=continent_data,
                           continent_key=continent_name,
                           articles=articles)


# ── API ENDPOINT (for future use) ───────────────────────────────────
@app.route('/api/news/<country_code>')
def api_news(country_code):
    """Returns news as JSON - useful for future features"""
    articles = fetch_news(country_code)
    return jsonify(articles)


# ── RUN APP ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)