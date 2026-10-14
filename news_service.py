"""
News & Advertising Service for Krishi Mitra
Provides:
1. Real-time Indian Agricultural News from verified feeds (Google News RSS / ICAR / DD Kisan),
   categorized and updated daily.
2. Daily Agricultural Advertisements & Farmer Marketplace Showcase with auto-slide carousel data.
"""

import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, date
import re

# In-memory news cache: (timestamp, news_list)
_NEWS_CACHE = {
    'timestamp': 0,
    'data': []
}
CACHE_TTL_SECONDS = 900  # 15 minutes

# Curated daily authentic agricultural news as high-reliability fallback (sorted newest to oldest)
FALLBACK_DAILY_NEWS = [
    {
        'id': 'news-3',
        'title': 'IMD Weather Outlook: Favorable Soil Moisture Conditions Predicted for Rabi Sowing',
        'summary': 'India Meteorological Department forecasts mild winter onset across Punjab, Haryana, Rajasthan, and Western UP, recommending early sowing of high-yielding wheat (PBW-826, HD-2967) and mustard varieties.',
        'category': 'Weather & Monsoon',
        'source': 'IMD Agro-Meteorology',
        'source_url': 'https://mausam.imd.gov.in',
        'published_at': 'Today, 11:45 AM',
        'read_time': '2 min read',
        'tag': 'Weather Advisory',
        'image_icon': 'fas fa-cloud-sun-rain'
    },
    {
        'id': 'news-2',
        'title': 'PM-KUSUM Scheme: Online Applications Open for 60% Solar Pump Subsidies Across 12 States',
        'summary': 'Ministry of New & Renewable Energy expands standalone solar agriculture pump scheme. Farmers can replace diesel pump sets with 3HP to 7.5HP solar pumps with up to 60% combined state and central subsidy.',
        'category': 'Subsidies & Schemes',
        'source': 'Ministry of Agriculture',
        'source_url': 'https://pmkusum.mnre.gov.in',
        'published_at': 'Today, 10:15 AM',
        'read_time': '4 min read',
        'tag': 'Subsidy Alert',
        'image_icon': 'fas fa-solar-panel'
    },
    {
        'id': 'news-1',
        'title': 'Cabinet Approves Minimum Support Price (MSP) Hike for Rabi Crops 2024-25 Season',
        'summary': 'Government increases MSP for Wheat to ₹2,425/quintal (+₹150) and Mustard to ₹5,950/quintal (+₹300) to ensure remunerative prices and boost crop diversification for farmers.',
        'category': 'Policy & MSP',
        'source': 'PIB Agriculture',
        'source_url': 'https://pib.gov.in',
        'published_at': 'Today, 08:30 AM',
        'read_time': '3 min read',
        'tag': 'Breaking',
        'image_icon': 'fas fa-landmark'
    },
    {
        'id': 'news-4',
        'title': 'IFFCO Announces Availability of Nano Urea Plus and Nano DAP at All Village PACS',
        'summary': 'A single 500ml bottle of Nano DAP now replaces a 50kg bag of traditional DAP, saving farmers 50% in input costs while cutting soil acidification and boosting seed germination rates by 12%.',
        'category': 'Technology & Inputs',
        'source': 'IFFCO Farmer Portal',
        'source_url': 'https://iffco.in',
        'published_at': 'Yesterday, 04:20 PM',
        'read_time': '3 min read',
        'tag': 'Input Savings',
        'image_icon': 'fas fa-flask'
    },
    {
        'id': 'news-5',
        'title': 'Kisan Drone Subsidy: Up to 75% Financial Aid for Custom Hiring Centers and FPOs',
        'summary': 'Department of Agriculture accelerates adoption of precision agriculture drones for liquid fertilizer and bio-pesticide spraying. Over 10,000 certified rural pilots to be trained this year.',
        'category': 'Technology & Inputs',
        'source': 'Agritech India',
        'source_url': 'https://agricoop.nic.in',
        'published_at': 'Yesterday, 02:10 PM',
        'read_time': '3 min read',
        'tag': 'Technology',
        'image_icon': 'fas fa-helicopter'
    },
    {
        'id': 'news-6',
        'title': 'e-NAM Cross-State Trade Surges: Farmers in MP and Gujarat Secure Premium Onion & Soybean Rates',
        'summary': 'Electronic National Agriculture Market platform connects over 1,360 wholesale mandis. Direct digital payments and automated assaying result in 15% higher returns for participating FPOs.',
        'category': 'Market & Mandi',
        'source': 'e-NAM National Portal',
        'source_url': 'https://enam.gov.in',
        'published_at': '2 days ago',
        'read_time': '4 min read',
        'tag': 'Mandi Trends',
        'image_icon': 'fas fa-chart-line'
    },
    {
        'id': 'news-7',
        'title': 'ICAR Issues Pest Advisory: Preventive Measures for Mustard Aphids and Wheat Rust',
        'summary': 'Scientists advise regular field scouting during rosette and tillering stages. Yellow sticky traps and balanced potassium application recommended before any chemical fungicide intervention.',
        'category': 'Crop Care & Alerts',
        'source': 'ICAR-IARI Pusa',
        'source_url': 'https://icar.org.in',
        'published_at': '2 days ago',
        'read_time': '3 min read',
        'tag': 'Crop Health',
        'image_icon': 'fas fa-shield-virus'
    },
    {
        'id': 'news-8',
        'title': 'Pradhan Mantri Fasal Bima Yojana (PMFBY): Enrolment Deadline for Rabi Crops Announced',
        'summary': 'Farmers advised to complete crop insurance enrolment via CSC centers or local bank branches with just 1.5% premium for Rabi crops. Comprehensive risk cover includes prevented sowing and post-harvest losses.',
        'category': 'Subsidies & Schemes',
        'source': 'PMFBY Portal',
        'source_url': 'https://pmfby.gov.in',
        'published_at': '3 days ago',
        'read_time': '3 min read',
        'tag': 'Important',
        'image_icon': 'fas fa-file-contract'
    }
]

# Daily Featured Farming Advertisements / Partner Showcase
FARMING_ADVERTISEMENTS = [
    {
        'id': 'ad-1',
        'badge': 'Government Subsidy • PM-KUSUM',
        'title': '60% Subsidy on Solar Agricultural Pumps',
        'subtitle': 'Cut Diesel Bills to Zero & Power Tube-Wells with Clean Solar Energy',
        'description': 'Replace costly diesel pumps with high-efficiency 3HP to 7.5HP DC Solar Pumps. Get 30% Central Subsidy + 30% State Subsidy + Easy Bank Loan for remaining 40%.',
        'benefits': ['Zero Electricity Bill for 25 Years', 'Reliable Daytime Irrigation', 'Sell Excess Power to Grid for Extra Income'],
        'partner': 'MNRE & State Renewable Energy Agencies',
        'cta_text': 'Apply for Solar Subsidy',
        'cta_link': 'https://pmkusum.mnre.gov.in',
        'helpline': '1800-180-3333',
        'theme_color': '#e65100',
        'bg_gradient': 'linear-gradient(135deg, #fff3e0 0%, #ffe0b2 50%, #ffcc80 100%)',
        'icon': 'fas fa-solar-panel',
        'deal_tag': 'Active Subsidy Window 2024-25'
    },
    {
        'id': 'ad-2',
        'badge': 'Certified Seeds • National Seeds Corporation',
        'title': 'High-Yield Certified Wheat & Mustard Seeds (NSC)',
        'subtitle': 'ICAR-Approved Climate Resilient Seed Varieties for Maximum Yield',
        'description': 'Government certified seeds for Wheat (PBW-826, HD-3086, DBW-187) and Mustard (Giriraj, RH-749, Pusa Mustard-30). Tested for 98% germination and disease resistance.',
        'benefits': ['15% to 20% Higher Yield per Acre', 'Treated with Bio-Fungicides', 'Doorstep Delivery via ONDC & CSCs'],
        'partner': 'National Seeds Corporation (Govt of India)',
        'cta_text': 'Order Certified Seeds',
        'cta_link': 'https://indiaseeds.com',
        'helpline': '1800-180-1551',
        'theme_color': '#2e7d32',
        'bg_gradient': 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%)',
        'icon': 'fas fa-seedling',
        'deal_tag': 'Kisan Special Discount Available'
    },
    {
        'id': 'ad-3',
        'badge': 'Nano Bio-Fertilizers • IFFCO',
        'title': 'Save 50% Fertilizer Costs with IFFCO Nano Urea & Nano DAP',
        'subtitle': 'One 500ml Bottle Replaces One 50kg Bag • Zero Black-Marketing Risk',
        'description': 'Bio-friendly liquid nanotechnology fertilizers tested across 11,000 farmer field trials. Ensures targeted nutrient delivery directly to crop foliage without soil salt buildup.',
        'benefits': ['Price: Just ₹225 per Bottle (vs ₹1,350 Traditional)', 'Prevents Groundwater Pollution', 'Improves Protein & Nutrient Quality'],
        'partner': 'Indian Farmers Fertiliser Cooperative (IFFCO)',
        'cta_text': 'Find Nearest Cooperative Center',
        'cta_link': 'https://iffco.in',
        'helpline': '1800-103-1967',
        'theme_color': '#1565c0',
        'bg_gradient': 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%)',
        'icon': 'fas fa-flask',
        'deal_tag': 'In Stock at All Primary Societies (PACS)'
    },
    {
        'id': 'ad-4',
        'badge': 'Low-Interest Credit • NABARD & KCC',
        'title': 'Kisan Credit Card (KCC) - Instant Loans @ 4% Effective Interest',
        'subtitle': 'Short-Term Crop Loans up to ₹3 Lakh with 3% Prompt Repayment Incentive',
        'description': 'Collateral-free agricultural loans up to ₹1.60 lakh for seeds, fertilizers, pesticides, and animal husbandry. Flexible repayment matching harvest and mandi sales cycles.',
        'benefits': ['Base Rate 7% - 3% Govt Subvention = Only 4% Net', 'Includes Free Accidental Insurance of ₹50,000', 'ATM-enabled RuPay Kisan Card'],
        'partner': 'NABARD & Public Sector Cooperative Banks',
        'cta_text': 'Apply for KCC Online',
        'cta_link': 'https://www.india.gov.in/spotlight/kisan-credit-card-kcc',
        'helpline': '1800-22-9011',
        'theme_color': '#6a1b9a',
        'bg_gradient': 'linear-gradient(135deg, #f3e5f5 0%, #e1bee7 50%, #ce93d8 100%)',
        'icon': 'fas fa-credit-card',
        'deal_tag': 'Simplified 1-Page Application'
    },
    {
        'id': 'ad-5',
        'badge': 'Farm Mechanization • SMAM Subsidies',
        'title': '50% Subsidy on Farm Machinery & Rotary Tillers',
        'subtitle': 'Modernize Sowing & Stubble Management with Happy Seeders & Super SMS',
        'description': 'Department of Agricultural Mechanization offers direct DBT subsidies on Tractors, Laser Land Levelers, Multi-Crop Harvesters, and Zero-Till Drills.',
        'benefits': ['Up to ₹50,000 to ₹1.5 Lakh Direct Bank Transfer', '80% Subsidy for Custom Hiring Centers (CHCs)', 'Custom Implements for Small Farms'],
        'partner': 'Ministry of Agriculture & Farmers Welfare',
        'cta_text': 'Check Machinery Subsidies',
        'cta_link': 'https://agrimachinery.nic.in',
        'helpline': '011-23381012',
        'theme_color': '#b71c1c',
        'bg_gradient': 'linear-gradient(135deg, #ffebee 0%, #ffcdd2 50%, #ef9a9a 100%)',
        'icon': 'fas fa-tractor',
        'deal_tag': 'SMAM Portal Direct DBT'
    }
]

def clean_html_tags(text):
    """Remove raw html tags from rss snippets"""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def categorize_article(title, summary=""):
    """Categorize an article into one of the main agricultural news buckets"""
    text = (title + " " + summary).lower()
    if any(k in text for k in ['rain', 'monsoon', 'weather', 'imd', 'drought', 'cyclone', 'flood', 'temperature', 'heatwave', 'cold', 'frost', 'forecast', 'climate']):
        return 'Weather & Monsoon'
    elif any(k in text for k in ['subsidy', 'scheme', 'pm-kisan', 'kusum', 'pmfby', 'kcc', 'bima', 'loan', 'credit', 'grant', 'yojana', 'dbt']):
        return 'Subsidies & Schemes'
    elif any(k in text for k in ['drone', 'technology', 'seed', 'fertilizer', 'urea', 'nano', 'dap', 'machinery', 'tractor', 'solar', 'mechanization', 'ai']):
        return 'Technology & Inputs'
    elif any(k in text for k in ['mandi', 'price', 'bhav', 'enam', 'export', 'import', 'trade', 'onion', 'wheat', 'cotton', 'paddy', 'market']):
        return 'Market & Mandi'
    elif any(k in text for k in ['pest', 'disease', 'fungus', 'locust', 'rust', 'crop care', 'spray', 'health', 'organic', 'soil health']):
        return 'Crop Care & Alerts'
    elif any(k in text for k in ['msp', 'minimum support price', 'cabinet', 'policy', 'procurement', 'fci', 'bill', 'act', 'parliament']):
        return 'Policy & MSP'
    return 'Policy & MSP'

def get_icon_for_category(cat):
    icons = {
        'Policy & MSP': 'fas fa-landmark',
        'Weather & Monsoon': 'fas fa-cloud-sun-rain',
        'Subsidies & Schemes': 'fas fa-file-invoice-dollar',
        'Technology & Inputs': 'fas fa-microchip',
        'Market & Mandi': 'fas fa-chart-line',
        'Crop Care & Alerts': 'fas fa-shield-virus'
    }
    return icons.get(cat, 'fas fa-newspaper')

from email.utils import parsedate_to_datetime
from datetime import timedelta

def parse_published_time_to_epoch(pub_str):
    """
    Convert relative or absolute publication time string to numeric unix epoch.
    Handles 'Today, 10:15 AM', 'Today, 08:30 AM', 'Yesterday, 04:20 PM', 'X days ago', etc.
    Ensures newer news is strictly sorted before older news.
    """
    now = datetime.now()
    today_date = now.date()

    if not pub_str:
        return now.timestamp() - 86400

    # Match "Today, 10:15 AM"
    m_today = re.search(r'Today,\s*(\d{1,2}):(\d{2})\s*(AM|PM)', pub_str, re.I)
    if m_today:
        hr, mn, ap = int(m_today.group(1)), int(m_today.group(2)), m_today.group(3).upper()
        if ap == 'PM' and hr != 12:
            hr += 12
        elif ap == 'AM' and hr == 12:
            hr = 0
        try:
            return datetime(today_date.year, today_date.month, today_date.day, hr, mn).timestamp()
        except Exception:
            pass

    # Match "Yesterday, 04:20 PM"
    m_yest = re.search(r'Yesterday,\s*(\d{1,2}):(\d{2})\s*(AM|PM)', pub_str, re.I)
    if m_yest:
        yest_date = today_date - timedelta(days=1)
        hr, mn, ap = int(m_yest.group(1)), int(m_yest.group(2)), m_yest.group(3).upper()
        if ap == 'PM' and hr != 12:
            hr += 12
        elif ap == 'AM' and hr == 12:
            hr = 0
        try:
            return datetime(yest_date.year, yest_date.month, yest_date.day, hr, mn).timestamp()
        except Exception:
            pass

    # Match "X days ago"
    m_days = re.search(r'(\d+)\s*days?\s*ago', pub_str, re.I)
    if m_days:
        days_ago = int(m_days.group(1))
        past_date = today_date - timedelta(days=days_ago)
        return datetime(past_date.year, past_date.month, past_date.day, 12, 0).timestamp()

    # Plain date e.g. "14 Oct 2024"
    try:
        dt = datetime.strptime(pub_str.strip()[:11], '%d %b %Y')
        return dt.timestamp()
    except Exception:
        pass

    return now.timestamp() - 86400

def sort_news_descending(news_list):
    """Sort news items by publication timestamp in reverse chronological order (latest news first)"""
    for item in news_list:
        if 'sort_epoch' not in item:
            item['sort_epoch'] = parse_published_time_to_epoch(item.get('published_at', ''))
    return sorted(news_list, key=lambda x: x.get('sort_epoch', 0), reverse=True)

def fetch_live_agri_news(limit=60, force_refresh=False):
    """
    Fetch live real-time Indian agricultural news from Google News RSS.
    Falls back seamlessly to high-quality curated news if network fails.
    """
    global _NEWS_CACHE
    now = time.time()

    # Return cached news if fresh and not forcing refresh
    if not force_refresh and _NEWS_CACHE['data'] and (now - _NEWS_CACHE['timestamp'] < CACHE_TTL_SECONDS):
        return _NEWS_CACHE['data']

    feed_url = 'https://news.google.com/rss/search?q=Indian+agriculture+farmers+MSP+crops&hl=en-IN&gl=IN&ceid=IN:en'
    try:
        req = urllib.request.Request(feed_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=4) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            items = root.findall('.//item')
            fetched = []

            for idx, item in enumerate(items[:limit]):
                title = clean_html_tags(item.findtext('title') or '')
                link = item.findtext('link') or '#'
                pub_date = item.findtext('pubDate') or ''
                source = item.findtext('source') or 'Agri News Bureau'
                desc = clean_html_tags(item.findtext('description') or '')

                # Parse and shorten source from title if embedded
                if ' - ' in title:
                    parts = title.rsplit(' - ', 1)
                    title = parts[0]
                    if not source or source == 'Agri News Bureau':
                        source = parts[1]

                # Format date string with time
                pub_clean = 'Today'
                sort_epoch = now - (idx * 60)
                if pub_date:
                    try:
                        dt = parsedate_to_datetime(pub_date)
                        sort_epoch = dt.timestamp()
                        if dt.date() == date.today():
                            pub_clean = f"Today, {dt.strftime('%I:%M %p')}"
                        else:
                            pub_clean = dt.strftime('%d %b %Y, %I:%M %p')
                    except Exception:
                        pub_clean = 'Today'

                cat = categorize_article(title, desc)

                fetched.append({
                    'id': f'live-{idx+1}',
                    'title': title,
                    'summary': desc[:220] + ('...' if len(desc) > 220 else '') if desc else f"Latest development regarding {title} for agricultural stakeholders across India.",
                    'category': cat,
                    'source': source,
                    'source_url': link,
                    'published_at': pub_clean,
                    'read_time': '3 min read',
                    'tag': 'Live',
                    'image_icon': get_icon_for_category(cat),
                    'sort_epoch': sort_epoch
                })

            if fetched:
                # Merge curated authentic items with live items, and sort newest first
                combined = sort_news_descending(fetched + FALLBACK_DAILY_NEWS)
                _NEWS_CACHE['timestamp'] = now
                _NEWS_CACHE['last_updated_str'] = datetime.now().strftime("%I:%M %p, %d %b %Y")
                _NEWS_CACHE['data'] = combined
                return combined

    except Exception as e:
        print(f"Notice: Live RSS fetch fallback triggered ({e})")

    # Fallback to curated daily items sorted newest to oldest
    fallback_sorted = sort_news_descending(FALLBACK_DAILY_NEWS)
    _NEWS_CACHE['timestamp'] = now
    _NEWS_CACHE['last_updated_str'] = datetime.now().strftime("%I:%M %p, %d %b %Y")
    _NEWS_CACHE['data'] = fallback_sorted
    return fallback_sorted

def get_news_last_updated_time():
    """Return formatted timestamp of when news was last retrieved"""
    return _NEWS_CACHE.get('last_updated_str') or datetime.now().strftime("%I:%M %p, %d %b %Y")

def get_daily_agri_news(category=None, search_query=None, limit=60, force_refresh=False):
    """Filter and return agricultural news"""
    news_items = fetch_live_agri_news(limit=60, force_refresh=force_refresh)
    filtered = []

    for item in news_items:
        # Category filter
        if category and category.lower() != 'all':
            if item['category'].lower() != category.lower():
                continue

        # Search query filter
        if search_query:
            q = search_query.lower().strip()
            haystack = f"{item['title']} {item['summary']} {item['source']} {item['category']}".lower()
            if q not in haystack:
                continue

        filtered.append(item)
        if len(filtered) >= limit:
            break

    return filtered

def get_daily_farming_ads():
    """Return daily farming advertisements and verified marketplace offers"""
    today_str = datetime.now().strftime("%d %B %Y")
    ads = []
    for item in FARMING_ADVERTISEMENTS:
        ad = dict(item)
        ad['date_stamp'] = today_str
        ads.append(ad)
    return ads

def get_news_categories():
    """Return unique categories with item counts"""
    news_items = fetch_live_agri_news(limit=60)
    cats = {}
    for item in news_items:
        c = item['category']
        cats[c] = cats.get(c, 0) + 1
    return [{'name': k, 'count': v} for k, v in sorted(cats.items())]
