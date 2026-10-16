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
NEWS_RETENTION_DAYS = 7  # 7-day active lifecycle
NEWS_RETENTION_SECONDS = NEWS_RETENTION_DAYS * 86400  # 604,800 seconds

def prune_expired_news(days=NEWS_RETENTION_DAYS):
    """
    Purge any news records older than retention window (default 7 days) from the system database and memory cache.
    Ensures outdated agricultural news is automatically deleted and never stays in our system.
    """
    global _NEWS_CACHE
    try:
        from database import prune_expired_farmer_news
        deleted = prune_expired_farmer_news(days=days)
    except Exception as e:
        deleted = 0
        print(f"Notice: News auto-prune: {e}")

    # Also prune in-memory cache of any items older than retention window
    if _NEWS_CACHE.get('data'):
        now = time.time()
        cutoff = now - (days * 86400)
        fresh_cache = [item for item in _NEWS_CACHE['data'] if item.get('sort_epoch', now) >= cutoff]
        if len(fresh_cache) != len(_NEWS_CACHE['data']):
            _NEWS_CACHE['data'] = fresh_cache

    return deleted

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
    },
    {
        'id': 'ad-6',
        'badge': 'Micro-Irrigation • PMKSY',
        'title': '55% Subsidy on Drip & Sprinkler Micro-Irrigation Systems',
        'subtitle': 'Save 45% Irrigation Water, Boost Crop Yield by 35% with Direct DBT Grant',
        'description': 'Pradhan Mantri Krishi Sinchayee Yojana (Per Drop More Crop) provides 55% capital subsidy for small & marginal farmers and 45% for other farmers for inline drip and portable sprinkler setups.',
        'benefits': ['Cuts Electricity & Pumping Bills by 40%', 'Direct Fertigation to Roots Saves 30% Fertilizer', 'Government Approved On-Farm Installation'],
        'partner': 'Department of Agriculture & Farmers Welfare (DA&FW)',
        'cta_text': 'Apply on PMKSY Portal',
        'cta_link': 'https://pmksy.gov.in',
        'helpline': '1800-180-1551',
        'theme_color': '#0288d1',
        'bg_gradient': 'linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 50%, #81d4fa 100%)',
        'icon': 'fas fa-faucet-drip',
        'deal_tag': 'Active State Allocation Window'
    },
    {
        'id': 'ad-7',
        'badge': 'Organic Farming • PKVY',
        'title': '₹50,000/Hectare Financial Support for Natural & Organic Farming',
        'subtitle': 'Paramparagat Krishi Vikas Yojana (PKVY) Cluster Support & PGS Certification',
        'description': 'Direct financial assistance of ₹50,000 per hectare over 3 years. ₹31,000/ha transferred directly via DBT to farmers for certified organic seeds, bio-fertilizers, and botanical extracts.',
        'benefits': ['Free PGS-India Organic Certification', 'Premium Selling Price in Organic Mandis', '₹8,800/ha for Post-Harvest Processing & Packaging'],
        'partner': 'National Centre of Organic & Natural Farming (NCONF)',
        'cta_text': 'Join Organic Cluster (PKVY)',
        'cta_link': 'https://pgsindia-ncof.gov.in',
        'helpline': '0120-2764906',
        'theme_color': '#388e3c',
        'bg_gradient': 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%)',
        'icon': 'fas fa-leaf',
        'deal_tag': 'Cluster Enrolment Open'
    },
    {
        'id': 'ad-8',
        'badge': 'Crop Insurance • PMFBY',
        'title': 'Comprehensive Crop Insurance at Nominal 1.5% - 2% Premium',
        'subtitle': 'Pradhan Mantri Fasal Bima Yojana (PMFBY) Protection Against Drought & Flood',
        'description': 'Lowest crop insurance premium in India: just 2% for Kharif food crops, 1.5% for Rabi oilseeds/cereals, and 5% for horticultural crops. Covers prevented sowing, mid-season adversity, and localized hailstorms.',
        'benefits': ['Satellite & Drone Fast-Track Claim Assessment', 'Direct Claim Deposit to Bank Account via DBT', '72-Hour Grievance Redressal Mechanism'],
        'partner': 'Ministry of Agriculture (Govt of India)',
        'cta_text': 'Insure Crop on PMFBY',
        'cta_link': 'https://pmfby.gov.in',
        'helpline': '14447',
        'theme_color': '#7b1fa2',
        'bg_gradient': 'linear-gradient(135deg, #f3e5f5 0%, #e1bee7 50%, #ce93d8 100%)',
        'icon': 'fas fa-shield-alt',
        'deal_tag': 'Rabi 2026-27 Enrollment Live'
    },
    {
        'id': 'ad-9',
        'badge': 'Soil Diagnostics • Govt Labs',
        'title': 'Free 12-Nutrient Soil Health Testing & Customized Fertilizer Dose',
        'subtitle': 'Stop Over-Spending on DAP & Urea with Scientific Soil Health Card Recommendations',
        'description': 'National Soil Health Card initiative provides free laboratory testing of pH, Electrical Conductivity, Nitrogen, Phosphorus, Potassium, Zinc, and Sulfur. Get dosage guidelines tailored to your soil.',
        'benefits': ['Saves ₹2,000 - ₹3,500 per Acre in Excess Fertilizer', 'Free Sample Testing at Nearest Block KVK Lab', 'Valid for 3 Years with Mobile Downloadable Card'],
        'partner': 'Soil Health Management Division (DAC&FW)',
        'cta_text': 'Track Soil Health Card',
        'cta_link': 'https://soilhealth.dac.gov.in',
        'helpline': '1800-180-1551',
        'theme_color': '#5d4037',
        'bg_gradient': 'linear-gradient(135deg, #efebe9 0%, #d7ccc8 50%, #bcaaa4 100%)',
        'icon': 'fas fa-flask-vial',
        'deal_tag': 'Free Testing at Block Labs'
    },
    {
        'id': 'ad-10',
        'badge': 'National e-Market • e-NAM',
        'title': 'Sell Produce Online Across 1,400+ Mandis Pan-India via e-NAM',
        'subtitle': 'Transparent Digital Auctions, Zero Middleman Cuts & Direct Bank Payment',
        'description': 'National Agriculture Market (e-NAM) connects 1.7 crore+ farmers directly with licensed bulk commodity buyers across 23 States and 4 UTs. Free quality assaying and transparent electronic weighing.',
        'benefits': ['Direct Bidding from Out-of-State Buyers for Higher Rates', 'Same-Day RTGS/NEFT Payment to Bank Account', 'Free Warehouse Receipt (e-NWR) Trade Support'],
        'partner': 'Small Farmers Agribusiness Consortium (SFAC)',
        'cta_text': 'Register on e-NAM Portal',
        'cta_link': 'https://enam.gov.in',
        'helpline': '1800-270-0224',
        'theme_color': '#f57f17',
        'bg_gradient': 'linear-gradient(135deg, #fffde7 0%, #fff9c4 50%, #fff59d 100%)',
        'icon': 'fas fa-building-columns',
        'deal_tag': '1,400+ Mandis Live'
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

def format_relative_time(epoch_time):
    """Convert timestamp to clean user-friendly relative time (e.g. '15 mins ago', 'Today, 02:30 PM')"""
    if not epoch_time:
        return "Recently"
    now_ts = time.time()
    diff = now_ts - epoch_time
    if diff < 0:
        return "Just now"
    if diff < 60:
        return f"{max(1, int(diff))}s ago"
    elif diff < 3600:
        mins = int(diff // 60)
        return f"{mins} min{'s' if mins > 1 else ''} ago"
    elif diff < 86400:
        hours = int(diff // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff < 172800:
        dt = datetime.fromtimestamp(epoch_time)
        return f"Yesterday, {dt.strftime('%I:%M %p')}"
    elif diff < 604800:
        days = int(diff // 86400)
        return f"{days} days ago"
    else:
        dt = datetime.fromtimestamp(epoch_time)
        return dt.strftime('%d %b %Y')

def parse_published_time_to_epoch(pub_str):
    """
    Convert relative or absolute publication time string to numeric unix epoch.
    Ensures newer news is strictly sorted before older news.
    """
    now = datetime.now()
    today_date = now.date()

    if not pub_str:
        return now.timestamp() - 86400

    # Match "X mins ago"
    m_mins = re.search(r'(\d+)\s*mins?\s*ago', pub_str, re.I)
    if m_mins:
        return time.time() - (int(m_mins.group(1)) * 60)

    # Match "X hours ago"
    m_hrs = re.search(r'(\d+)\s*hours?\s*ago', pub_str, re.I)
    if m_hrs:
        return time.time() - (int(m_hrs.group(1)) * 3600)

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
    """Sort news items strictly by publication timestamp in reverse chronological order (latest news first)"""
    for item in news_list:
        if 'sort_epoch' not in item or not item['sort_epoch']:
            item['sort_epoch'] = parse_published_time_to_epoch(item.get('published_at', ''))
    return sorted(news_list, key=lambda x: x.get('sort_epoch', 0), reverse=True)

def get_farmer_community_news_items():
    """Retrieve verified community-submitted farmer news items from SQLite database (strictly within 7 days)"""
    try:
        from database import get_all_farmer_news
        records = get_all_farmer_news(limit=60, max_age_days=NEWS_RETENTION_DAYS)
        items = []
        now_ts = time.time()
        for r in records:
            created_str = r.get('created_at', '')
            epoch = now_ts
            if created_str:
                try:
                    dt = datetime.strptime(created_str, '%Y-%m-%d %H:%M:%S')
                    epoch = dt.timestamp()
                except Exception:
                    pass

            # Skip any news older than 7 days
            if (now_ts - epoch) > NEWS_RETENTION_SECONDS:
                continue

            loc_parts = [p for p in [r.get('village_district'), r.get('state')] if p]
            location_str = ", ".join(loc_parts) if loc_parts else "Rural India"
            
            cat = r.get('category') or 'Crop Care & Alerts'
            items.append({
                'id': f"farmer-{r['id']}",
                'farmer_db_id': r['id'],
                'title': r['title'],
                'summary': r['summary'],
                'category': cat,
                'source': f"🌾 {r['author_name']} ({location_str})",
                'source_url': r.get('source_url') or '#',
                'published_at': format_relative_time(epoch),
                'read_time': '1 min read',
                'tag': 'Farmer Report',
                'badge_color': '#2e7d32',
                'image_icon': 'fas fa-bullhorn',
                'is_farmer_news': True,
                'author_name': r['author_name'],
                'location': location_str,
                'contact': r.get('contact', ''),
                'upvotes': r.get('upvotes', 0),
                'sort_epoch': epoch
            })
        return items
    except Exception as e:
        print(f"Notice: Farmer community news fetch: {e}")
        return []

def add_farmer_report(title, summary, category, author_name, village_district=None, state=None, contact=None, source_url=None):
    """Add a new community farmer report and invalidate cache immediately"""
    global _NEWS_CACHE
    from database import create_farmer_news
    news_id = create_farmer_news(
        title=title,
        summary=summary,
        category=category,
        author_name=author_name,
        village_district=village_district,
        state=state,
        contact=contact,
        source_url=source_url
    )
    # Invalidate cache so fresh report appears immediately
    _NEWS_CACHE['timestamp'] = 0
    _NEWS_CACHE['data'] = []
    return news_id

def fetch_live_agri_news(limit=100, force_refresh=False):
    """
    Fetch live real-time Indian agricultural news from multiple verified RSS feeds (Google News, PIB Agri, IMD).
    Seamlessly merges with farmer-submitted field advisories and orders newest items first.
    Enforces automatic 7-day retention: news older than 7 days is automatically pruned and deleted.
    """
    global _NEWS_CACHE
    now = time.time()

    # Automatically prune expired news records from DB and memory
    prune_expired_news(days=NEWS_RETENTION_DAYS)

    # Return cached news if fresh and not forcing refresh
    if not force_refresh and _NEWS_CACHE['data'] and (now - _NEWS_CACHE['timestamp'] < CACHE_TTL_SECONDS):
        return _NEWS_CACHE['data']

    # Multi-topic agricultural RSS feeds
    feed_urls = [
        'https://news.google.com/rss/search?q=farmers+agriculture+MSP+india&hl=en-IN&gl=IN&ceid=IN:en',
        'https://news.google.com/rss/search?q=kisan+mandi+bhav+crops+india&hl=en-IN&gl=IN&ceid=IN:en',
        'https://news.google.com/rss/search?q=imd+weather+agriculture+rainfall+india&hl=en-IN&gl=IN&ceid=IN:en',
        'https://news.google.com/rss/search?q=agritech+fertilizer+seeds+subsidy+india&hl=en-IN&gl=IN&ceid=IN:en'
    ]

    fetched = []
    seen_titles = set()

    for feed_url in feed_urls:
        try:
            req = urllib.request.Request(feed_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                items = root.findall('.//item')

                for item in items[:30]:
                    raw_title = clean_html_tags(item.findtext('title') or '')
                    if not raw_title:
                        continue
                    
                    # Normalize title for deduplication
                    norm_key = re.sub(r'[^a-z0-9]', '', raw_title.lower())[:50]
                    if norm_key in seen_titles:
                        continue
                    seen_titles.add(norm_key)

                    link = item.findtext('link') or '#'
                    pub_date = item.findtext('pubDate') or ''
                    source = item.findtext('source') or 'Agri News Bureau'
                    desc = clean_html_tags(item.findtext('description') or '')

                    title = raw_title
                    if ' - ' in title:
                        parts = title.rsplit(' - ', 1)
                        title = parts[0]
                        if not source or source == 'Agri News Bureau':
                            source = parts[1]

                    sort_epoch = now - (len(fetched) * 180)
                    pub_clean = "Recently"
                    if pub_date:
                        try:
                            dt = parsedate_to_datetime(pub_date)
                            sort_epoch = dt.timestamp()
                            pub_clean = format_relative_time(sort_epoch)
                        except Exception:
                            pub_clean = "Recently"

                    # 7-day cutoff filter: skip if older than 7 days
                    if (now - sort_epoch) > NEWS_RETENTION_SECONDS:
                        continue

                    cat = categorize_article(title, desc)

                    fetched.append({
                        'id': f'live-{len(fetched)+1}',
                        'title': title,
                        'summary': desc[:230] + ('...' if len(desc) > 230 else '') if desc else f"Latest development regarding {title} for agricultural stakeholders across India.",
                        'category': cat,
                        'source': source,
                        'source_url': link,
                        'published_at': pub_clean,
                        'read_time': '3 min read',
                        'tag': 'Live Feed',
                        'image_icon': get_icon_for_category(cat),
                        'is_farmer_news': False,
                        'sort_epoch': sort_epoch
                    })

        except Exception as e:
            print(f"Notice: Live RSS query failed for {feed_url[:45]}... ({e})")

    # Fetch farmer community reports (strictly within 7 days)
    farmer_reports = get_farmer_community_news_items()

    # Combine farmer items + live RSS news and strictly enforce 7-day retention
    all_news = [
        item for item in (farmer_reports + fetched)
        if (now - item.get('sort_epoch', now)) <= NEWS_RETENTION_SECONDS
    ]

    # If fewer than 8 total items retrieved (network outage), backfill with curated fallback items
    if len(all_news) < 8:
        for idx, fb in enumerate(FALLBACK_DAILY_NEWS):
            fb_copy = dict(fb)
            fb_epoch = now - (86400 * (idx + 1))
            fb_copy['sort_epoch'] = fb_epoch
            fb_copy['published_at'] = format_relative_time(fb_epoch)
            fb_copy['is_farmer_news'] = False
            all_news.append(fb_copy)

    # Sort strictly descending (newest articles first)
    combined = sort_news_descending(all_news)

    _NEWS_CACHE['timestamp'] = now
    _NEWS_CACHE['last_updated_str'] = datetime.now().strftime("%I:%M %p, %d %b %Y")
    _NEWS_CACHE['data'] = combined
    return combined

def get_news_last_updated_time():
    """Return formatted timestamp of when news was last retrieved"""
    return _NEWS_CACHE.get('last_updated_str') or datetime.now().strftime("%I:%M %p, %d %b %Y")

def get_daily_agri_news(category=None, search_query=None, limit=100, force_refresh=False):
    """Filter and return agricultural news"""
    news_items = fetch_live_agri_news(limit=100, force_refresh=force_refresh)
    filtered = []

    for item in news_items:
        # Category filter
        if category and category.lower() != 'all':
            cat_lower = category.lower().strip()
            if cat_lower in ['farmer', 'farmer community reports', 'farmer reports']:
                if not item.get('is_farmer_news'):
                    continue
            elif item['category'].lower() != cat_lower:
                continue

        # Search query filter
        if search_query:
            q = search_query.lower().strip()
            haystack = f"{item['title']} {item['summary']} {item['source']} {item['category']} {item.get('author_name', '')} {item.get('location', '')}".lower()
            if q not in haystack:
                continue

        filtered.append(item)
        if len(filtered) >= limit:
            break

    return filtered

def add_farmer_deal(title, category, description, price_terms="", seller_name="Farmer", contact_number="", location="", state="", image_url=None):
    """Add a farmer deal / verified agricultural offer to the database"""
    from database import create_farmer_deal
    return create_farmer_deal(
        title=title,
        category=category,
        description=description,
        price_terms=price_terms,
        seller_name=seller_name,
        contact_number=contact_number,
        location=location,
        state=state,
        image_url=image_url
    )

def get_daily_farming_ads(category=None, region=None):
    """Return daily farming advertisements and verified marketplace offers combining community deals and partner ads with region tagging"""
    today_str = datetime.now().strftime("%d %B %Y")
    ads = []

    try:
        from mandi_service import get_region_for_state
    except Exception:
        def get_region_for_state(st):
            return 'North'

    # 1. Fetch community & local farmer deals from database
    try:
        from database import get_all_farmer_deals
        farmer_deals = get_all_farmer_deals(limit=25)
        for deal in farmer_deals:
            cat = deal.get('category') or 'General Farming'
            theme_colors = {
                'Seeds & Plant Material': '#2e7d32',
                'Machinery & Equipment Rental': '#b71c1c',
                'Fertilizers & Organic Inputs': '#2e7d32',
                'Drone & Tech Services': '#1565c0',
                'Irrigation & Solar': '#e65100',
                'Crop Output & Harvest Sale': '#f57f17'
            }
            theme_color = theme_colors.get(cat, '#2e7d32')

            bg_gradient = "linear-gradient(135deg, #f1f8e9 0%, #dcedc8 50%, #c5e1a5 100%)"
            if 'Machinery' in cat:
                bg_gradient = "linear-gradient(135deg, #ffebee 0%, #ffcdd2 50%, #ef9a9a 100%)"
            elif 'Drone' in cat or 'Tech' in cat:
                bg_gradient = "linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%)"
            elif 'Solar' in cat or 'Irrigation' in cat:
                bg_gradient = "linear-gradient(135deg, #fff3e0 0%, #ffe0b2 50%, #ffcc80 100%)"
            elif 'Output' in cat:
                bg_gradient = "linear-gradient(135deg, #fffde7 0%, #fff9c4 50%, #fff59d 100%)"

            icons = {
                'Seeds & Plant Material': 'fas fa-seedling',
                'Machinery & Equipment Rental': 'fas fa-tractor',
                'Fertilizers & Organic Inputs': 'fas fa-leaf',
                'Drone & Tech Services': 'fas fa-drone',
                'Irrigation & Solar': 'fas fa-solar-panel',
                'Crop Output & Harvest Sale': 'fas fa-boxes-stacked'
            }
            icon = icons.get(cat, 'fas fa-handshake')

            badge_text = deal.get('badge') or f"Farmer Deal • {cat}"

            benefits = []
            if deal.get('price_terms'):
                benefits.append(f"Rate / Terms: {deal.get('price_terms')}")
            if deal.get('location'):
                benefits.append(f"Location: {deal.get('location')}, {deal.get('state', '')}")
            if deal.get('is_verified'):
                benefits.append("Verified Community Listing")
            else:
                benefits.append("Direct Farmer-to-Farmer Deal")

            # Resolve crop image if relevant
            crop_img = deal.get('image_url')
            if not crop_img:
                from crop_images import get_crop_image_url
                crop_img = get_crop_image_url(deal.get('title', ''))

            deal_region = get_region_for_state(deal.get('state'))

            ads.append({
                'id': f"deal-{deal['id']}",
                'deal_id': deal['id'],
                'is_farmer_deal': True,
                'badge': badge_text,
                'title': deal['title'],
                'subtitle': f"Offered by {deal.get('seller_name', 'Local Farmer')} ({deal.get('location', 'India')})",
                'description': deal.get('description', ''),
                'benefits': benefits,
                'partner': f"{deal.get('seller_name', 'Community Farmer')} ({deal.get('location', '')})",
                'cta_text': "Call / Contact Seller",
                'cta_link': f"tel:{deal.get('contact_number')}" if deal.get('contact_number') else '#',
                'helpline': deal.get('contact_number') or 'Community Listing',
                'theme_color': theme_color,
                'bg_gradient': bg_gradient,
                'icon': icon,
                'deal_tag': f"₹ {deal.get('price_terms')}" if deal.get('price_terms') else "Verified Deal",
                'date_stamp': today_str,
                'upvotes': deal.get('upvotes', 0),
                'location': deal.get('location'),
                'state': deal.get('state'),
                'region': deal_region,
                'seller_name': deal.get('seller_name'),
                'contact_number': deal.get('contact_number'),
                'image_url': crop_img
            })
    except Exception as e:
        print(f"Error loading farmer deals: {e}")

    # 2. Partner & Institutional Ads
    for item in FARMING_ADVERTISEMENTS:
        ad = dict(item)
        ad['date_stamp'] = today_str
        ad['is_farmer_deal'] = False
        ad['upvotes'] = 15
        ad['region'] = get_region_for_state(ad.get('state') or 'Punjab')
        ads.append(ad)

    # Optional region filtering
    if region and region.lower() not in ['all', '']:
        ads = [a for a in ads if a.get('region', '').lower() == region.lower() or region.lower() in a.get('region', '').lower()]

    # Optional category filtering
    if category and category.lower() not in ['all', '']:
        ads = [a for a in ads if category.lower() in a.get('category', '').lower() or category.lower() in a.get('badge', '').lower()]

    # Strict Deduplication: Ensure each offer or subsidy appears only once (no repeating titles)
    seen_titles = set()
    unique_ads = []
    for a in ads:
        t_key = a.get('title', '').strip().lower()
        if not t_key or t_key in seen_titles:
            continue
        seen_titles.add(t_key)
        unique_ads.append(a)

    return unique_ads

def get_news_categories():
    """Return unique categories with item counts including Farmer Community Reports"""
    news_items = fetch_live_agri_news(limit=100)
    cats = {}
    farmer_count = 0
    for item in news_items:
        if item.get('is_farmer_news'):
            farmer_count += 1
        c = item['category']
        cats[c] = cats.get(c, 0) + 1
    
    cat_list = [{'name': k, 'count': v} for k, v in sorted(cats.items())]
    if farmer_count > 0:
        cat_list.insert(0, {'name': 'Farmer Community Reports', 'count': farmer_count, 'is_farmer': True})
    return cat_list
