# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    ARTICLES_PER_PAGE = 10

    CONTINENTS = {
        'asia': {
            'name': 'Asia',
            'emoji': '🌏',
            'description': 'News from the largest and most populous continent',
            'color': 'success',
            'countries': {
                'in': {'name': 'India',        'flag': '🇮🇳'},
                'cn': {'name': 'China',         'flag': '🇨🇳'},
                'jp': {'name': 'Japan',         'flag': '🇯🇵'},
                'pk': {'name': 'Pakistan',      'flag': '🇵🇰'},
                'bd': {'name': 'Bangladesh',    'flag': '🇧🇩'},
                'sg': {'name': 'Singapore',     'flag': '🇸🇬'},
            }
        },
        'europe': {
            'name': 'Europe',
            'emoji': '🌍',
            'description': 'News from across the European continent',
            'color': 'primary',
            'countries': {
                'gb': {'name': 'United Kingdom', 'flag': '🇬🇧'},
                'de': {'name': 'Germany',         'flag': '🇩🇪'},
                'fr': {'name': 'France',          'flag': '🇫🇷'},
                'it': {'name': 'Italy',           'flag': '🇮🇹'},
                'es': {'name': 'Spain',           'flag': '🇪🇸'},
            }
        },
        'north_america': {
            'name': 'North America',
            'emoji': '🌎',
            'description': 'News from North American nations',
            'color': 'danger',
            'countries': {
                'us': {'name': 'United States', 'flag': '🇺🇸'},
                'ca': {'name': 'Canada',         'flag': '🇨🇦'},
                'mx': {'name': 'Mexico',         'flag': '🇲🇽'},
            }
        },
        'south_america': {
            'name': 'South America',
            'emoji': '🌎',
            'description': 'News from South American nations',
            'color': 'warning',
            'countries': {
                'br': {'name': 'Brazil',    'flag': '🇧🇷'},
                'ar': {'name': 'Argentina', 'flag': '🇦🇷'},
                'co': {'name': 'Colombia',  'flag': '🇨🇴'},
            }
        },
        'africa': {
            'name': 'Africa',
            'emoji': '🌍',
            'description': 'News from the African continent',
            'color': 'info',
            'countries': {
                'ng': {'name': 'Nigeria',       'flag': '🇳🇬'},
                'za': {'name': 'South Africa',  'flag': '🇿🇦'},
                'eg': {'name': 'Egypt',         'flag': '🇪🇬'},
                'ke': {'name': 'Kenya',         'flag': '🇰🇪'},
            }
        },
        'oceania': {
            'name': 'Oceania',
            'emoji': '🌏',
            'description': 'News from Australia, New Zealand and Pacific islands',
            'color': 'secondary',
            'countries': {
                'au': {'name': 'Australia',  'flag': '🇦🇺'},
                'nz': {'name': 'New Zealand', 'flag': '🇳🇿'},
            }
        }
    }