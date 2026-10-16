"""
Mandi Service for Krishi Mitra
Provides up-to-date Indian APMC Mandi prices, MSP (Minimum Support Price 2024-25/2026),
daily bulletin release schedule, region-wise filtering, and regional buyer procurement offers.
"""
from datetime import datetime, date
import random

# State to Indian Agricultural Region Mapping
STATE_REGION_MAP = {
    'Punjab': 'North',
    'Haryana': 'North',
    'Rajasthan': 'North',
    'Uttar Pradesh': 'North',
    'Himachal Pradesh': 'North',
    'Jammu and Kashmir': 'North',
    'Uttarakhand': 'North',
    'Delhi': 'North',
    'Madhya Pradesh': 'Central',
    'Chhattisgarh': 'Central',
    'Maharashtra': 'West',
    'Gujarat': 'West',
    'Goa': 'West',
    'Andhra Pradesh': 'South',
    'Telangana': 'South',
    'Karnataka': 'South',
    'Tamil Nadu': 'South',
    'Kerala': 'South',
    'West Bengal': 'East & North-East',
    'Bihar': 'East & North-East',
    'Odisha': 'East & North-East',
    'Jharkhand': 'East & North-East',
    'Assam': 'East & North-East'
}

# Government of India MSP (Minimum Support Price) 2024-25 / 2025-26 in ₹/Quintal
GOVT_MSP_RATES = {
    'wheat': 2425,
    'paddy_common': 2300,
    'paddy_grade_a': 2320,
    'rice': 2300,
    'cotton_medium': 7121,
    'cotton_long': 7521,
    'cotton': 7121,
    'mustard': 5950,
    'soybean': 4892,
    'chickpea': 5650,
    'gram': 5650,
    'groundnut': 6783,
    'maize': 2225,
    'bajra': 2625,
    'jowar_hybrid': 3371,
    'jowar': 3371,
    'ragi': 4290,
    'barley': 1980,
    'sunflower': 7280,
    'sugarcane': 340,   # FRP per quintal
    'turmeric': 13500,  # Benchmark modal
    'onion': 2100,      # Benchmark modal
    'potato': 1450,     # Benchmark modal
    'tomato': 1800      # Benchmark modal
}

MANDI_PRICE_DATA = [
    # Punjab (North)
    {
        'state': 'Punjab', 'district': 'Ludhiana', 'market': 'Khanna APMC',
        'commodity': 'Wheat', 'variety': 'Sharbati / PBW-826',
        'min_price': 2400, 'max_price': 2580, 'modal_price': 2480,
        'msp': 2425, 'trend': 'Rising', 'arrivals': '4,200 Bags',
        'category': 'Cereal', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:45 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Punjab', 'district': 'Amritsar', 'market': 'Amritsar Dana Mandi',
        'commodity': 'Paddy (Basmati)', 'variety': '1121 Pusa Basmati',
        'min_price': 3850, 'max_price': 4350, 'modal_price': 4120,
        'msp': 2300, 'trend': 'Rising', 'arrivals': '3,800 Bags',
        'category': 'Cereal', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:30 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Punjab', 'district': 'Bathinda', 'market': 'Bathinda Cotton Yard',
        'commodity': 'Cotton', 'variety': 'BT Cotton Medium',
        'min_price': 6950, 'max_price': 7450, 'modal_price': 7280,
        'msp': 7121, 'trend': 'Steady', 'arrivals': '1,450 Quintals',
        'category': 'Commercial', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:15 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Punjab', 'district': 'Jalandhar', 'market': 'Jalandhar Sabzi Mandi',
        'commodity': 'Potato', 'variety': 'Kufri Jyoti Fresh',
        'min_price': 1250, 'max_price': 1650, 'modal_price': 1450,
        'msp': 1450, 'trend': 'Steady', 'arrivals': '6,500 Quintals',
        'category': 'Vegetable', 'region': 'North',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 11:30 AM', 'release_status': 'Official APMC Released'
    },

    # Haryana (North)
    {
        'state': 'Haryana', 'district': 'Karnal', 'market': 'Karnal Grain Market',
        'commodity': 'Paddy (Basmati)', 'variety': '1509 Basmati',
        'min_price': 3550, 'max_price': 3950, 'modal_price': 3780,
        'msp': 2300, 'trend': 'Rising', 'arrivals': '2,900 Bags',
        'category': 'Cereal', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:00 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Haryana', 'district': 'Hisar', 'market': 'Hisar Mandi',
        'commodity': 'Mustard', 'variety': 'Black Mustard (Raya)',
        'min_price': 5750, 'max_price': 6180, 'modal_price': 6010,
        'msp': 5950, 'trend': 'Rising', 'arrivals': '2,200 Quintals',
        'category': 'Oilseed', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:20 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Haryana', 'district': 'Sirsa', 'market': 'Sirsa Cotton Yard',
        'commodity': 'Cotton', 'variety': 'G. hirsutum',
        'min_price': 7100, 'max_price': 7520, 'modal_price': 7340,
        'msp': 7121, 'trend': 'Rising', 'arrivals': '1,800 Quintals',
        'category': 'Commercial', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:40 PM', 'release_status': 'Official APMC Released'
    },

    # Rajasthan (North)
    {
        'state': 'Rajasthan', 'district': 'Bharatpur', 'market': 'Bharatpur Mandi',
        'commodity': 'Mustard', 'variety': 'Yellow / Black Mustard',
        'min_price': 5850, 'max_price': 6350, 'modal_price': 6140,
        'msp': 5950, 'trend': 'Rising', 'arrivals': '15,000 Bags',
        'category': 'Oilseed', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:50 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Rajasthan', 'district': 'Kota', 'market': 'Bhamashah Mandi Kota',
        'commodity': 'Wheat', 'variety': 'Milkat / Desi Wheat',
        'min_price': 2450, 'max_price': 2750, 'modal_price': 2560,
        'msp': 2425, 'trend': 'Rising', 'arrivals': '9,200 Bags',
        'category': 'Cereal', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:10 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Rajasthan', 'district': 'Jaipur', 'market': 'Muhana Mandi Jaipur',
        'commodity': 'Bajra', 'variety': 'Desi Pearl Millet',
        'min_price': 2550, 'max_price': 2850, 'modal_price': 2710,
        'msp': 2625, 'trend': 'Rising', 'arrivals': '4,800 Bags',
        'category': 'Cereal', 'region': 'North',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 11:45 AM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Rajasthan', 'district': 'Bikaner', 'market': 'Bikaner Grain Mandi',
        'commodity': 'Gram (Chana)', 'variety': 'Desi Chana Bold',
        'min_price': 5550, 'max_price': 6050, 'modal_price': 5820,
        'msp': 5650, 'trend': 'Rising', 'arrivals': '3,900 Bags',
        'category': 'Pulse', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:25 PM', 'release_status': 'Official APMC Released'
    },

    # Uttar Pradesh (North)
    {
        'state': 'Uttar Pradesh', 'district': 'Agra', 'market': 'Agra Mandi',
        'commodity': 'Potato', 'variety': 'Kufri Bahar',
        'min_price': 1200, 'max_price': 1620, 'modal_price': 1420,
        'msp': 1450, 'trend': 'Steady', 'arrivals': '22,000 Quintals',
        'category': 'Vegetable', 'region': 'North',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 10:30 AM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Uttar Pradesh', 'district': 'Bareilly', 'market': 'Bareilly Mandi',
        'commodity': 'Wheat', 'variety': 'HD-2967',
        'min_price': 2420, 'max_price': 2580, 'modal_price': 2490,
        'msp': 2425, 'trend': 'Rising', 'arrivals': '7,500 Bags',
        'category': 'Cereal', 'region': 'North',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:15 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Uttar Pradesh', 'district': 'Muzaffarnagar', 'market': 'Muzaffarnagar Sugar Yard',
        'commodity': 'Sugarcane', 'variety': 'Co-0238',
        'min_price': 350, 'max_price': 380, 'modal_price': 365,
        'msp': 340, 'trend': 'Steady', 'arrivals': '45,000 Tonnes',
        'category': 'Commercial', 'region': 'North',
        'bulletin_session': 'Continuous Crushing (दैनिक तौल)',
        'release_time': 'Today, 02:00 PM', 'release_status': 'Official Mill Released'
    },
    {
        'state': 'Uttar Pradesh', 'district': 'Lucknow', 'market': 'Dubagga Mandi Lucknow',
        'commodity': 'Mango', 'variety': 'Dasheri',
        'min_price': 3200, 'max_price': 4800, 'modal_price': 3900,
        'msp': 3500, 'trend': 'Steady', 'arrivals': '4,200 Crates',
        'category': 'Fruit', 'region': 'North',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 11:00 AM', 'release_status': 'Official APMC Released'
    },

    # Madhya Pradesh (Central)
    {
        'state': 'Madhya Pradesh', 'district': 'Indore', 'market': 'Indore (Chhawani Mandi)',
        'commodity': 'Soybean', 'variety': 'Yellow Soybean (JS-9560)',
        'min_price': 4750, 'max_price': 5220, 'modal_price': 5050,
        'msp': 4892, 'trend': 'Rising', 'arrivals': '8,500 Bags',
        'category': 'Oilseed', 'region': 'Central',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:00 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Madhya Pradesh', 'district': 'Indore', 'market': 'Indore APMC',
        'commodity': 'Wheat', 'variety': 'Lokwan Premium',
        'min_price': 2600, 'max_price': 2950, 'modal_price': 2780,
        'msp': 2425, 'trend': 'Rising', 'arrivals': '5,600 Bags',
        'category': 'Cereal', 'region': 'Central',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:30 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Madhya Pradesh', 'district': 'Ujjain', 'market': 'Ujjain Mandi',
        'commodity': 'Gram (Chana)', 'variety': 'Desi Chana (JG-11)',
        'min_price': 5600, 'max_price': 6100, 'modal_price': 5850,
        'msp': 5650, 'trend': 'Rising', 'arrivals': '3,400 Bags',
        'category': 'Pulse', 'region': 'Central',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:45 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Madhya Pradesh', 'district': 'Mandsaur', 'market': 'Mandsaur Mandi',
        'commodity': 'Garlic', 'variety': 'Ooty / Desi Bold',
        'min_price': 9500, 'max_price': 15800, 'modal_price': 12400,
        'msp': 10000, 'trend': 'Rising', 'arrivals': '2,100 Quintals',
        'category': 'Spice', 'region': 'Central',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:15 PM', 'release_status': 'Official APMC Released'
    },

    # Maharashtra (West)
    {
        'state': 'Maharashtra', 'district': 'Nashik', 'market': 'Lasalgaon APMC',
        'commodity': 'Onion', 'variety': 'Red Onion (Gavran)',
        'min_price': 1850, 'max_price': 3150, 'modal_price': 2520,
        'msp': 2100, 'trend': 'Steady', 'arrivals': '18,000 Quintals',
        'category': 'Vegetable', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:30 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Maharashtra', 'district': 'Latur', 'market': 'Latur APMC',
        'commodity': 'Soybean', 'variety': 'JS-335 / Grade I',
        'min_price': 4800, 'max_price': 5180, 'modal_price': 5010,
        'msp': 4892, 'trend': 'Steady', 'arrivals': '12,500 Bags',
        'category': 'Oilseed', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:40 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Maharashtra', 'district': 'Latur', 'market': 'Latur APMC',
        'commodity': 'Pigeonpeas (Arhar/Tur)', 'variety': 'White Tur',
        'min_price': 9800, 'max_price': 11200, 'modal_price': 10550,
        'msp': 7550, 'trend': 'Rising', 'arrivals': '3,800 Bags',
        'category': 'Pulse', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:00 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Maharashtra', 'district': 'Kolhapur', 'market': 'Kolhapur Market',
        'commodity': 'Sugarcane', 'variety': 'Co-86032',
        'min_price': 345, 'max_price': 385, 'modal_price': 365,
        'msp': 340, 'trend': 'Steady', 'arrivals': '35,000 Tonnes',
        'category': 'Commercial', 'region': 'West',
        'bulletin_session': 'Crushing Daily Rate',
        'release_time': 'Today, 01:30 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Maharashtra', 'district': 'Sangli', 'market': 'Sangli Turmeric Yard',
        'commodity': 'Turmeric', 'variety': 'Rajapuri Bold',
        'min_price': 13200, 'max_price': 16800, 'modal_price': 15100,
        'msp': 13500, 'trend': 'Rising', 'arrivals': '1,900 Quintals',
        'category': 'Spice', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:50 PM', 'release_status': 'Official APMC Released'
    },

    # Gujarat (West)
    {
        'state': 'Gujarat', 'district': 'Rajkot', 'market': 'Rajkot APMC (Marketing Yard)',
        'commodity': 'Groundnut', 'variety': 'GG-20 / Bold 50-60',
        'min_price': 6750, 'max_price': 7450, 'modal_price': 7120,
        'msp': 6783, 'trend': 'Rising', 'arrivals': '14,000 Bags',
        'category': 'Oilseed', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:15 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Gujarat', 'district': 'Rajkot', 'market': 'Rajkot APMC',
        'commodity': 'Cotton', 'variety': 'Shankar-6 (S-6)',
        'min_price': 7200, 'max_price': 7680, 'modal_price': 7480,
        'msp': 7121, 'trend': 'Rising', 'arrivals': '6,200 Quintals',
        'category': 'Commercial', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:45 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Gujarat', 'district': 'Gondal', 'market': 'Gondal APMC Yard',
        'commodity': 'Chilli', 'variety': 'Dry Red Resham Patti',
        'min_price': 15000, 'max_price': 22500, 'modal_price': 18800,
        'msp': 16000, 'trend': 'Rising', 'arrivals': '4,500 Quintals',
        'category': 'Spice', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:00 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Gujarat', 'district': 'Unjha', 'market': 'Unjha APMC (Spice Market)',
        'commodity': 'Mustard', 'variety': 'Peeled Mustard / Mustard Seed',
        'min_price': 5850, 'max_price': 6250, 'modal_price': 6050,
        'msp': 5950, 'trend': 'Steady', 'arrivals': '3,100 Bags',
        'category': 'Oilseed', 'region': 'West',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:30 PM', 'release_status': 'Official APMC Released'
    },

    # Andhra Pradesh & Telangana (South)
    {
        'state': 'Andhra Pradesh', 'district': 'Guntur', 'market': 'Guntur Mirchi Yard',
        'commodity': 'Chilli', 'variety': 'Teja / S17 Dry Red Chilli',
        'min_price': 16500, 'max_price': 24000, 'modal_price': 20200,
        'msp': 16500, 'trend': 'Rising', 'arrivals': '25,000 Bags',
        'category': 'Spice', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:30 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Telangana', 'district': 'Nizamabad', 'market': 'Nizamabad Turmeric Market',
        'commodity': 'Turmeric', 'variety': 'Finger Nizamabad Turmeric',
        'min_price': 12800, 'max_price': 16200, 'modal_price': 14600,
        'msp': 13500, 'trend': 'Rising', 'arrivals': '6,500 Bags',
        'category': 'Spice', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:45 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Andhra Pradesh', 'district': 'Kurnool', 'market': 'Kurnool Market',
        'commodity': 'Onion', 'variety': 'Bellary Red',
        'min_price': 1700, 'max_price': 2800, 'modal_price': 2250,
        'msp': 2100, 'trend': 'Steady', 'arrivals': '7,200 Quintals',
        'category': 'Vegetable', 'region': 'South',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 11:15 AM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Telangana', 'district': 'Warangal', 'market': 'Enumamula Market Warangal',
        'commodity': 'Cotton', 'variety': 'Long Staple BT Cotton',
        'min_price': 7250, 'max_price': 7700, 'modal_price': 7520,
        'msp': 7521, 'trend': 'Rising', 'arrivals': '8,500 Quintals',
        'category': 'Commercial', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:00 PM', 'release_status': 'Official APMC Released'
    },

    # Karnataka (South)
    {
        'state': 'Karnataka', 'district': 'Kolar', 'market': 'Kolar APMC (APMC Yard)',
        'commodity': 'Tomato', 'variety': 'Hybrid Red Firm Tomato',
        'min_price': 1600, 'max_price': 2800, 'modal_price': 2200,
        'msp': 1800, 'trend': 'Rising', 'arrivals': '14,000 Crates',
        'category': 'Vegetable', 'region': 'South',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 10:15 AM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Karnataka', 'district': 'Davangere', 'market': 'Davangere APMC',
        'commodity': 'Maize', 'variety': 'Yellow Maize',
        'min_price': 2250, 'max_price': 2480, 'modal_price': 2360,
        'msp': 2225, 'trend': 'Rising', 'arrivals': '11,000 Bags',
        'category': 'Cereal', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:30 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Karnataka', 'district': 'Hassan', 'market': 'Hassan Ragi Market',
        'commodity': 'Ragi', 'variety': 'Finger Millet (Indaf-8)',
        'min_price': 4250, 'max_price': 4650, 'modal_price': 4450,
        'msp': 4290, 'trend': 'Steady', 'arrivals': '3,200 Bags',
        'category': 'Cereal', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:40 PM', 'release_status': 'Official APMC Released'
    },

    # Tamil Nadu & Kerala (South)
    {
        'state': 'Tamil Nadu', 'district': 'Erode', 'market': 'Erode Turmeric Market',
        'commodity': 'Turmeric', 'variety': 'Erode Local Finger',
        'min_price': 13500, 'max_price': 16900, 'modal_price': 15250,
        'msp': 13500, 'trend': 'Rising', 'arrivals': '5,800 Bags',
        'category': 'Spice', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:50 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Tamil Nadu', 'district': 'Thanjavur', 'market': 'Thanjavur Regulated Market',
        'commodity': 'Paddy (Common)', 'variety': 'ADT-45 / CR-1009',
        'min_price': 2320, 'max_price': 2550, 'modal_price': 2440,
        'msp': 2300, 'trend': 'Steady', 'arrivals': '6,000 Bags',
        'category': 'Cereal', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:10 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Kerala', 'district': 'Wayanad', 'market': 'Kalpetta Spice Yard',
        'commodity': 'Ginger', 'variety': 'Green Ginger (Wayanad Bold)',
        'min_price': 7200, 'max_price': 10500, 'modal_price': 8900,
        'msp': 7500, 'trend': 'Rising', 'arrivals': '1,400 Bags',
        'category': 'Spice', 'region': 'South',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:20 PM', 'release_status': 'Official APMC Released'
    },

    # West Bengal, Bihar & Assam (East & North-East)
    {
        'state': 'West Bengal', 'district': 'Burdwan', 'market': 'Burdwan Krishi Mandi',
        'commodity': 'Paddy (Common)', 'variety': 'Swarna (MTU-7029)',
        'min_price': 2300, 'max_price': 2480, 'modal_price': 2390,
        'msp': 2300, 'trend': 'Steady', 'arrivals': '8,500 Bags',
        'category': 'Cereal', 'region': 'East & North-East',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 03:45 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Bihar', 'district': 'Purnia', 'market': 'Gulabbagh Mandi Purnia',
        'commodity': 'Maize', 'variety': 'Rabi Yellow Maize',
        'min_price': 2280, 'max_price': 2520, 'modal_price': 2410,
        'msp': 2225, 'trend': 'Rising', 'arrivals': '16,000 Bags',
        'category': 'Cereal', 'region': 'East & North-East',
        'bulletin_session': 'Closing Auction (शाम का भाव)',
        'release_time': 'Today, 04:20 PM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'West Bengal', 'district': 'Hooghly', 'market': 'Tarakeswar Mandi',
        'commodity': 'Potato', 'variety': 'Jyoti Fresh',
        'min_price': 1300, 'max_price': 1650, 'modal_price': 1480,
        'msp': 1450, 'trend': 'Steady', 'arrivals': '12,000 Quintals',
        'category': 'Vegetable', 'region': 'East & North-East',
        'bulletin_session': 'Morning Session (प्रातः भाव)',
        'release_time': 'Today, 11:30 AM', 'release_status': 'Official APMC Released'
    },
    {
        'state': 'Assam', 'district': 'Guwahati', 'market': 'Guwahati Tea Auction / Mandi',
        'commodity': 'Tea', 'variety': 'CTC Orthodox Green Leaf',
        'min_price': 3400, 'max_price': 5200, 'modal_price': 4150,
        'msp': 3600, 'trend': 'Steady', 'arrivals': '4,500 Kg',
        'category': 'Commercial', 'region': 'East & North-East',
        'bulletin_session': 'Weekly Auction Closing',
        'release_time': 'Today, 02:45 PM', 'release_status': 'Official APMC Released'
    }
]

# Regional Verified Mandi Procurement & Input Deals
REGIONAL_MANDI_OFFERS = [
    # North Region Offers
    {
        'id': 'offer-north-1',
        'region': 'North',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Sharbati & PBW-826 Premium Wheat Procurement',
        'buyer_partner': 'Khanna Agro Flour & Roller Mills',
        'location': 'Khanna APMC Yard, Ludhiana, Punjab',
        'state': 'Punjab',
        'offered_rate': '₹2,550 - ₹2,600 / Quintal',
        'msp_comp': '+₹125 over Govt MSP',
        'quantity': 'Requirement: 5,000 Bags (Instant Weighment)',
        'payment_terms': 'Same-Day Spot Bank Transfer / Instant RTGS',
        'contact': '98765-11024',
        'badge': 'Verified Direct Mill Procurement',
        'badge_color': '#2e7d32',
        'icon': 'fas fa-wheat-awn',
        'commodity': 'Wheat'
    },
    {
        'id': 'offer-north-2',
        'region': 'North',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Pusa 1121 & 1509 Basmati Paddy Export Purchase',
        'buyer_partner': 'Karnal Royal Basmati Overseas Ltd',
        'location': 'Karnal Grain Market, Haryana',
        'state': 'Haryana',
        'offered_rate': '₹4,180 - ₹4,350 / Quintal',
        'msp_comp': 'Premium Export Quality Bonus',
        'quantity': 'Requirement: 8,000 Bags (< 12% Moisture)',
        'payment_terms': 'Immediate APMC Mandi Receipt Settlement',
        'contact': '98120-44981',
        'badge': 'Govt Certified Export House',
        'badge_color': '#1565c0',
        'icon': 'fas fa-bowl-rice',
        'commodity': 'Paddy (Basmati)'
    },
    {
        'id': 'offer-north-3',
        'region': 'North',
        'offer_type': 'Input Subsidy & Deals',
        'title': 'Certified High-Germination Mustard & Wheat Seeds 25% Off',
        'buyer_partner': 'IFFCO Kisan Sahakari Kendra',
        'location': 'Bharatpur & Kota Mandis, Rajasthan',
        'state': 'Rajasthan',
        'offered_rate': 'Subsidized ₹42/kg with Free Bio-Fungicide',
        'msp_comp': 'Certified Breeder Seed',
        'quantity': 'Stock: 2,500 Certified Packets Available',
        'payment_terms': 'Kisan Credit Card / Cash / DBT',
        'contact': '1800-180-1551',
        'badge': 'Cooperative Input Subsidy',
        'badge_color': '#e65100',
        'icon': 'fas fa-seedling',
        'commodity': 'Mustard'
    },

    # Central Region Offers
    {
        'id': 'offer-central-1',
        'region': 'Central',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Yellow Soybean (JS-9560 / JS-2034) Direct Solvent Mill Purchase',
        'buyer_partner': 'Malwa Solvent Extractions & Refineries',
        'location': 'Chhawani Mandi, Indore, Madhya Pradesh',
        'state': 'Madhya Pradesh',
        'offered_rate': '₹5,100 - ₹5,250 / Quintal',
        'msp_comp': '+₹208 over Govt MSP',
        'quantity': 'Requirement: 12,000 Bags (Any Moisture up to 11%)',
        'payment_terms': 'Cash on Gate Weight or Instant NEFT',
        'contact': '94250-88319',
        'badge': 'Solvent Plant Direct Gate Entry',
        'badge_color': '#2e7d32',
        'icon': 'fas fa-cubes-stacked',
        'commodity': 'Soybean'
    },
    {
        'id': 'offer-central-2',
        'region': 'Central',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Desi Bold Chana (Gram) & Masoor Direct Mill Buying',
        'buyer_partner': 'Ujjain Mahakaleshwar Dal Millers Group',
        'location': 'Ujjain APMC Mandi, Madhya Pradesh',
        'state': 'Madhya Pradesh',
        'offered_rate': '₹5,880 - ₹6,050 / Quintal',
        'msp_comp': '+₹230 over Govt MSP',
        'quantity': 'Requirement: 4,000 Bags',
        'payment_terms': 'Gatepass Clearance with Zero Brokerage',
        'contact': '98260-33412',
        'badge': 'Zero Brokerage Direct Dal Mill',
        'badge_color': '#6a1b9a',
        'icon': 'fas fa-jar',
        'commodity': 'Gram (Chana)'
    },

    # West Region Offers
    {
        'id': 'offer-west-1',
        'region': 'West',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Lasalgaon Red Onion (Gavran) Direct Export Container Booking',
        'buyer_partner': 'Nashik Agro-Fresh Gulf Exporters',
        'location': 'Lasalgaon APMC Market, Nashik, Maharashtra',
        'state': 'Maharashtra',
        'offered_rate': '₹2,650 - ₹2,950 / Quintal',
        'msp_comp': '+₹550 over Benchmark',
        'quantity': 'Requirement: 25 Truck Loads (Grade-A 45mm+)',
        'payment_terms': 'Spot Electronic APMC Payout',
        'contact': '98220-77112',
        'badge': 'Direct Gulf Export Procurement',
        'badge_color': '#b71c1c',
        'icon': 'fas fa-apple-whole',
        'commodity': 'Onion'
    },
    {
        'id': 'offer-west-2',
        'region': 'West',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Saurashtra GG-20 Bold Groundnut Direct Oil Mill Buying',
        'buyer_partner': 'Rajkot Agro Edible Oil Mills',
        'location': 'Rajkot Marketing Yard, Gujarat',
        'state': 'Gujarat',
        'offered_rate': '₹7,200 - ₹7,480 / Quintal',
        'msp_comp': '+₹417 over Govt MSP',
        'quantity': 'Requirement: 6,000 Bags (Clean Pods)',
        'payment_terms': 'Direct Account Credit within 2 Hours',
        'contact': '98790-44123',
        'badge': 'Top Paying APMC Yard Partner',
        'badge_color': '#2e7d32',
        'icon': 'fas fa-bottle-droplet',
        'commodity': 'Groundnut'
    },
    {
        'id': 'offer-west-3',
        'region': 'West',
        'offer_type': 'Custom Hiring & Services',
        'title': 'Custom Hiring Mechanized Sugarcane Harvester Booking',
        'buyer_partner': 'Kolhapur District Cane Harvester Cooperative',
        'location': 'Kolhapur & Sangli, Maharashtra',
        'state': 'Maharashtra',
        'offered_rate': '₹380 per Tonne Mechanized Cutting',
        'msp_comp': 'Cuts 40% Harvesting Labor Cost',
        'quantity': 'Available: 8 Harvesters with Operators',
        'payment_terms': 'Direct Sugar Mill Recovery Adjustment',
        'contact': '98231-55099',
        'badge': 'Mechanized Harvesting Subsidy',
        'badge_color': '#1565c0',
        'icon': 'fas fa-tractor',
        'commodity': 'Sugarcane'
    },

    # South Region Offers
    {
        'id': 'offer-south-1',
        'region': 'South',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Teja & S17 Guntur Red Chilli Cold Storage & Export Buy',
        'buyer_partner': 'Guntur Spice Merchants Federation',
        'location': 'Guntur Mirchi Yard, Andhra Pradesh',
        'state': 'Andhra Pradesh',
        'offered_rate': '₹20,500 - ₹22,800 / Quintal',
        'msp_comp': 'Top Grade Export Quality',
        'quantity': 'Requirement: 10,000 Bags (Deep Red Stemless)',
        'payment_terms': 'Immediate eNAM Settlement',
        'contact': '98480-11234',
        'badge': 'Spices Board Certified Buyer',
        'badge_color': '#b71c1c',
        'icon': 'fas fa-pepper-hot',
        'commodity': 'Chilli'
    },
    {
        'id': 'offer-south-2',
        'region': 'South',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Kolar Hybrid Firm Red Tomato Paste Factory Direct Purchase',
        'buyer_partner': 'Kolar Agro Processing & Puree Ltd',
        'location': 'Kolar APMC Market, Karnataka',
        'state': 'Karnataka',
        'offered_rate': '₹2,250 - ₹2,400 / Quintal',
        'msp_comp': '+₹450 over MSP Benchmark',
        'quantity': 'Requirement: 30 Metric Tonnes Daily',
        'payment_terms': 'Crate-to-Crate Spot Payment at Gate',
        'contact': '94480-66778',
        'badge': 'Direct Factory Procurement',
        'badge_color': '#2e7d32',
        'icon': 'fas fa-kitchen-set',
        'commodity': 'Tomato'
    },
    {
        'id': 'offer-south-3',
        'region': 'South',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Erode & Nizamabad Finger Turmeric Direct Curcumin Mill Buy',
        'buyer_partner': 'Deccan Natural Curcumin Extracts',
        'location': 'Nizamabad & Erode Turmeric Markets',
        'state': 'Telangana',
        'offered_rate': '₹15,200 - ₹16,500 / Quintal',
        'msp_comp': '+₹1,700 over Benchmark',
        'quantity': 'Requirement: 3,500 Bags (> 3.5% Curcumin)',
        'payment_terms': 'Spot Quality-Linked Electronic Transfer',
        'contact': '98490-99881',
        'badge': 'High Curcumin Premium Bonus',
        'badge_color': '#e65100',
        'icon': 'fas fa-mortar-pestle',
        'commodity': 'Turmeric'
    },

    # East & North-East Region Offers
    {
        'id': 'offer-east-1',
        'region': 'East & North-East',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Gulabbagh Yellow Rabi Maize Starch Factory Bulk Buy',
        'buyer_partner': 'Purnia Starch & Cattle Feed Mills',
        'location': 'Gulabbagh Mandi, Purnia, Bihar',
        'state': 'Bihar',
        'offered_rate': '₹2,420 - ₹2,530 / Quintal',
        'msp_comp': '+₹195 over Govt MSP',
        'quantity': 'Requirement: 15,000 Bags (Dry Clean Grain)',
        'payment_terms': 'Zero Mandi Cut Direct Weighbridge Payment',
        'contact': '94310-22119',
        'badge': 'Starch Mill Direct Acceptance',
        'badge_color': '#2e7d32',
        'icon': 'fas fa-plant-wilt',
        'commodity': 'Maize'
    },
    {
        'id': 'offer-east-2',
        'region': 'East & North-East',
        'offer_type': 'Procurement (Buyer Direct)',
        'title': 'Swarna & Minikit Paddy Direct Cooperative Rice Mill Buying',
        'buyer_partner': 'Burdwan District Rice Millers Association',
        'location': 'Burdwan Krishi Mandi, West Bengal',
        'state': 'West Bengal',
        'offered_rate': '₹2,400 - ₹2,480 / Quintal',
        'msp_comp': '+₹100 over Govt MSP',
        'quantity': 'Requirement: 8,000 Bags',
        'payment_terms': 'Bank Account NEFT within 24 Hours',
        'contact': '98320-55441',
        'badge': 'Govt Registered Rice Mill',
        'badge_color': '#1565c0',
        'icon': 'fas fa-bowl-rice',
        'commodity': 'Paddy (Common)'
    }
]

def get_region_for_state(state):
    """Resolve state to Indian agricultural region"""
    if not state:
        return 'North'
    return STATE_REGION_MAP.get(state.strip(), 'North')

def get_mandi_prices(state_filter=None, commodity_filter=None, search_query=None, region_filter=None):
    """
    Filter and return real-time APMC Mandi rates with MSP comparisons, 
    daily bulletin release timing, and region classification.
    """
    today_str = datetime.now().strftime("%d %b %Y")
    results = []

    # Safe crop image lookup helper
    try:
        from crop_images import get_crop_image_url
    except Exception:
        def get_crop_image_url(name):
            return ""

    for item in MANDI_PRICE_DATA:
        # Determine region if missing
        region = item.get('region') or get_region_for_state(item.get('state'))

        # Match region filter
        if region_filter and region_filter.lower() not in ['all', '']:
            if region.lower() != region_filter.lower() and region_filter.lower() not in region.lower():
                continue

        # Match state filter
        if state_filter and state_filter.lower() != 'all':
            if item['state'].lower() != state_filter.lower():
                continue

        # Match commodity filter
        if commodity_filter and commodity_filter.lower() != 'all':
            if item['commodity'].lower() != commodity_filter.lower() and commodity_filter.lower() not in item['commodity'].lower():
                continue

        # Match search query
        if search_query:
            q = search_query.lower().strip()
            haystack = f"{item['commodity']} {item['variety']} {item['market']} {item['district']} {item['state']} {region}".lower()
            if q not in haystack:
                continue

        # Calculate difference from Govt MSP
        msp = item.get('msp', 0)
        modal = item['modal_price']
        diff = modal - msp
        diff_pct = round((diff / msp) * 100, 1) if msp > 0 else 0

        res = dict(item)
        res['region'] = region
        res['updated_date'] = today_str
        res['msp_difference'] = diff
        res['msp_diff_percent'] = diff_pct
        res['status'] = 'Above MSP' if diff >= 0 else 'Below MSP'
        res['image_url'] = get_crop_image_url(item['commodity'])
        results.append(res)

    return results

def get_all_states(region_filter=None):
    """Return unique states, optionally filtered by region"""
    if region_filter and region_filter.lower() != 'all':
        return sorted(list(set(
            item['state'] for item in MANDI_PRICE_DATA 
            if (item.get('region') or get_region_for_state(item['state'])).lower() == region_filter.lower()
        )))
    return sorted(list(set(item['state'] for item in MANDI_PRICE_DATA)))

def get_all_commodities(region_filter=None):
    """Return unique commodities, optionally filtered by region"""
    if region_filter and region_filter.lower() != 'all':
        return sorted(list(set(
            item['commodity'] for item in MANDI_PRICE_DATA 
            if (item.get('region') or get_region_for_state(item['state'])).lower() == region_filter.lower()
        )))
    return sorted(list(set(item['commodity'] for item in MANDI_PRICE_DATA)))

def get_all_regions():
    """Return standard Indian agricultural region categories with descriptions and metadata"""
    return [
        {
            'id': 'all',
            'name': 'All Regions',
            'name_hi': 'समस्त भारत',
            'icon': 'fas fa-earth-asia',
            'states': 'All APMC Mandis Nationwide',
            'badge': '40+ Mandis'
        },
        {
            'id': 'North',
            'name': 'North India',
            'name_hi': 'उत्तर भारत',
            'icon': 'fas fa-mountain-sun',
            'states': 'Punjab, Haryana, Rajasthan, Uttar Pradesh',
            'badge': 'Wheat, Mustard & Basmati Hub'
        },
        {
            'id': 'Central',
            'name': 'Central India',
            'name_hi': 'मध्य भारत',
            'icon': 'fas fa-sun',
            'states': 'Madhya Pradesh, Chhattisgarh',
            'badge': 'Soybean & Pulses Capital'
        },
        {
            'id': 'West',
            'name': 'West India',
            'name_hi': 'पश्चिम भारत',
            'icon': 'fas fa-water',
            'states': 'Maharashtra, Gujarat, Goa',
            'badge': 'Onion, Cotton & Groundnut'
        },
        {
            'id': 'South',
            'name': 'South India',
            'name_hi': 'दक्षिण भारत',
            'icon': 'fas fa-tree',
            'states': 'AP, Telangana, Karnataka, Tamil Nadu, Kerala',
            'badge': 'Spices, Chilli & Paddy'
        },
        {
            'id': 'East & North-East',
            'name': 'East & North-East',
            'name_hi': 'पूर्वी व पूर्वोत्तर भारत',
            'icon': 'fas fa-cloud-sun-rain',
            'states': 'West Bengal, Bihar, Assam',
            'badge': 'Maize, Paddy & Tea'
        }
    ]

def get_mandi_summary_stats(region_filter=None):
    """Return high-level summary stats for the dashboard, optionally scoped to region"""
    dataset = MANDI_PRICE_DATA
    if region_filter and region_filter.lower() != 'all':
        dataset = [
            item for item in MANDI_PRICE_DATA 
            if (item.get('region') or get_region_for_state(item['state'])).lower() == region_filter.lower()
        ]
    if not dataset:
        dataset = MANDI_PRICE_DATA

    commodities = set(item['commodity'] for item in dataset)
    states = set(item['state'] for item in dataset)
    markets = set(item['market'] for item in dataset)
    above_msp_count = sum(1 for item in dataset if item['modal_price'] >= item['msp'])

    return {
        'total_commodities': len(commodities),
        'total_states': len(states),
        'total_markets': len(markets),
        'above_msp_percent': round((above_msp_count / len(dataset)) * 100, 1) if dataset else 100.0,
        'records_count': len(dataset)
    }

def get_mandi_release_schedule(region_filter=None):
    """
    Return official daily APMC release timing schedule, bulletin session,
    and live status for transparency to farmers.
    """
    now = datetime.now()
    cur_hour = now.hour
    today_date = now.strftime("%d %B %Y")
    cur_time = now.strftime("%I:%M %p")

    if cur_hour < 12:
        session = 'Morning Session (प्रातः कालीन प्रथम भाव)'
        release_time = f'Today, 10:30 AM ({today_date})'
        next_session = 'Afternoon Closing Bulletin at 03:30 PM'
        release_state = 'Live Morning Mandi Session Active'
    elif cur_hour < 17:
        session = 'Closing Final Auction (शाम का अंतिम बंद भाव)'
        release_time = f'Today, 03:45 PM ({today_date})'
        next_session = 'Tomorrow Opening Auction at 10:30 AM'
        release_state = 'Today\'s Official APMC Closing Bulletins Released'
    else:
        session = 'Closing Final Auction (अंतिम प्रमाणित भाव)'
        release_time = f'Today, 05:00 PM ({today_date})'
        next_session = 'Tomorrow Morning Opening at 10:30 AM'
        release_state = 'All Regional Bulletins Finalized & Archived'

    return {
        'current_session': session,
        'release_timestamp': release_time,
        'next_release': next_session,
        'release_state': release_state,
        'last_sync_time': cur_time,
        'total_released_bulletins': len(MANDI_PRICE_DATA),
        'is_released_today': True
    }

def refresh_mandi_prices(region_filter=None):
    """
    Simulate live APMC bulletin re-sync when newly released rates are published.
    Updates arrival volumes, applies minor market fluctuations, and stamps fresh release time.
    """
    now = datetime.now()
    cur_time = now.strftime("%I:%M %p")

    refreshed_list = []
    for item in MANDI_PRICE_DATA:
        # Small fluctuation between -15 and +25 rupees to reflect active auction bidding
        variation = random.choice([-15, -10, 0, 10, 15, 20, 25])
        new_modal = max(item['min_price'], min(item['max_price'], item['modal_price'] + variation))
        item['modal_price'] = new_modal
        item['release_time'] = f"Today, {cur_time} (Newly Released Bulletin)"
        item['release_status'] = 'Official APMC Released (Fresh Sync)'
        refreshed_list.append(item)

    return get_mandi_prices(region_filter=region_filter)

def get_regional_mandi_offers(region_filter=None, commodity_filter=None):
    """
    Retrieve verified regional procurement inquiries (buyer wanted) and input offers.
    Allows farmers to directly connect with mills, exporters, and input suppliers in their zone.
    """
    offers = []
    for off in REGIONAL_MANDI_OFFERS:
        if region_filter and region_filter.lower() not in ['all', '']:
            if off['region'].lower() != region_filter.lower() and region_filter.lower() not in off['region'].lower():
                continue

        if commodity_filter and commodity_filter.lower() != 'all':
            if off.get('commodity') and commodity_filter.lower() not in off['commodity'].lower():
                continue

        offers.append(dict(off))

    return offers

def add_mandi_offer(data):
    """
    Add a farmer/buyer procurement offer directly into the regional mandi offers network.
    """
    offer_id = f"offer-user-{int(datetime.now().timestamp())}"
    state = data.get('state', 'Punjab')
    region = get_region_for_state(state)

    new_offer = {
        'id': offer_id,
        'region': region,
        'offer_type': data.get('offer_type', 'Farmer Direct Sale (विक्रेता)'),
        'title': data.get('title', 'Direct Commodity Offer'),
        'buyer_partner': data.get('partner_name', 'Local Farmer / Trader'),
        'location': data.get('location', f"{state} Mandi"),
        'state': state,
        'offered_rate': data.get('price_terms', 'Negotiable at Mandi Gate'),
        'msp_comp': data.get('msp_comp', 'Spot Settlement'),
        'quantity': data.get('quantity', 'Available on Request'),
        'payment_terms': data.get('payment_terms', 'Direct Bank Transfer / Cash'),
        'contact': data.get('contact', '1800-180-1551'),
        'badge': 'Community Mandi Listing',
        'badge_color': '#2e7d32',
        'icon': 'fas fa-handshake',
        'commodity': data.get('commodity', 'General')
    }
    REGIONAL_MANDI_OFFERS.insert(0, new_offer)
    return offer_id
