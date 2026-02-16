# 🌐 GlobalNews - Accessible Global News Platform

A web application that aggregates and simplifies news from around 
the world, with a strong focus on accessibility for visually 
impaired users.

## 🚀 Live Demo
Coming soon...

## ✨ Features
- 📰 Live news from trusted sources (BBC, NDTV, Al Jazeera, DW News)
- 🌍 Browse news by Continent → Country
- 🔍 Filter by category (Politics, Sports, Technology, Health etc.)
- 👁️ Full accessibility support with Text-to-Speech
- 🔊 Read Aloud feature for every article
- 🌐 Country flags for all supported countries
- ⚡ Fast loading with skeleton animations
- 📱 Fully responsive (mobile, tablet, desktop)
- 🌙 High contrast mode for visually impaired users
- 🔴 Live breaking news ticker

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **News Sources:** RSS Feeds (feedparser)
- **Accessibility:** Web Speech API, ARIA labels
- **Flags:** flagcdn.com

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/prajapati-anuj/news-website.git
cd news-website
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
```bash
# Create a .env file and add:
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run the application
```bash
python app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

## 📁 Project Structure
```
news-website/
├── app.py                  # Main Flask application
├── config.py               # Configuration + continent/country data
├── requirements.txt        # Python dependencies
│
├── services/
│   ├── news_fetcher.py     # RSS feed fetching + categorization
│   └── summarizer.py       # Article summarization
│
├── templates/
│   ├── base.html           # Base layout
│   ├── index.html          # Homepage
│   ├── continent.html      # Continent page
│   └── country.html        # Country news page
│
└── static/
    ├── css/style.css       # Custom styles + animations
    └── js/main.js          # Accessibility + loading spinner
```

## 🌍 Supported Countries
**Asia:** India, China, Japan, Pakistan, Bangladesh, Singapore  
**Europe:** UK, Germany, France, Italy, Spain  
**North America:** USA, Canada, Mexico  
**South America:** Brazil, Argentina, Colombia  
**Africa:** Nigeria, South Africa, Egypt, Kenya  
**Oceania:** Australia, New Zealand  

## ♿ Accessibility Features
- Screen reader support (ARIA labels)
- Text-to-Speech for every article
- Keyboard navigation
- High contrast mode
- Adjustable font size
- Skip to main content link

## 👨‍💻 Developer
Built by **Anuj** as part of learning full stack web development.

## 📄 License
MIT License - feel free to use and modify!