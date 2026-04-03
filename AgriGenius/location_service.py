import requests
import os
from dotenv import load_dotenv

load_dotenv()

# You can use OpenCage, Google Maps, or Nominatim (free)
# For this implementation, we'll use Nominatim (free, no API key needed)
# For production, consider OpenCage or Google Maps

def reverse_geocode_nominatim(latitude, longitude):
    """
    Reverse geocode using Nominatim (OpenStreetMap) - Free, no API key
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'AgriGenius/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            
            # Extract state and district - try multiple fields
            state = (address.get('state') or 
                    address.get('state_district') or 
                    address.get('region') or
                    address.get('ISO3166-2-lvl4', '').split('-')[-1] if address.get('ISO3166-2-lvl4') else None)
            
            district = (address.get('county') or 
                       address.get('state_district') or 
                       address.get('district') or
                       address.get('suburb'))
            
            city = (address.get('city') or 
                   address.get('town') or 
                   address.get('village') or
                   address.get('municipality') or
                   address.get('hamlet'))
            
            # If state is still None, try to extract from full address
            if not state and 'full_address' in data:
                parts = data.get('display_name', '').split(', ')
                # In India, state is usually second to last before country
                if len(parts) >= 2:
                    state = parts[-2] if parts[-1] == 'India' else None
            
            return {
                'success': True,
                'state': state,
                'district': district,
                'city': city,
                'country': address.get('country'),
                'full_address': data.get('display_name')
            }
        else:
            return {'success': False, 'error': 'Geocoding service unavailable'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def reverse_geocode_opencage(latitude, longitude):
    """
    Reverse geocode using OpenCage API (requires API key)
    Get free API key from: https://opencagedata.com/
    """
    api_key = os.getenv('OPENCAGE_API_KEY')
    
    if not api_key:
        return {'success': False, 'error': 'OpenCage API key not configured'}
    
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json"
        params = {
            'q': f"{latitude},{longitude}",
            'key': api_key,
            'language': 'en'
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                components = data['results'][0]['components']
                
                state = (components.get('state') or 
                        components.get('state_district'))
                
                district = (components.get('county') or 
                           components.get('state_district') or
                           components.get('district'))
                
                city = (components.get('city') or 
                       components.get('town') or 
                       components.get('village'))
                
                return {
                    'success': True,
                    'state': state,
                    'district': district,
                    'city': city,
                    'country': components.get('country'),
                    'full_address': data['results'][0]['formatted']
                }
        
        return {'success': False, 'error': 'Location not found'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_location_from_coordinates(latitude, longitude, service='nominatim'):
    """
    Main function to get location from coordinates
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        service: 'nominatim' (free) or 'opencage' (requires API key)
    
    Returns:
        Dictionary with location information
    """
    if service == 'opencage':
        return reverse_geocode_opencage(latitude, longitude)
    else:
        return reverse_geocode_nominatim(latitude, longitude)

# Indian state name normalization
INDIAN_STATES = {
    'andhra pradesh': 'Andhra Pradesh',
    'arunachal pradesh': 'Arunachal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chhattisgarh': 'Chhattisgarh',
    'goa': 'Goa',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'himachal pradesh': 'Himachal Pradesh',
    'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka',
    'kerala': 'Kerala',
    'madhya pradesh': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra',
    'manipur': 'Manipur',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'nagaland': 'Nagaland',
    'odisha': 'Odisha',
    'punjab': 'Punjab',
    'rajasthan': 'Rajasthan',
    'sikkim': 'Sikkim',
    'tamil nadu': 'Tamil Nadu',
    'telangana': 'Telangana',
    'tripura': 'Tripura',
    'uttar pradesh': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand',
    'west bengal': 'West Bengal',
    'andaman and nicobar islands': 'Andaman and Nicobar Islands',
    'chandigarh': 'Chandigarh',
    'dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'delhi': 'Delhi',
    'dl': 'Delhi',
    'jammu and kashmir': 'Jammu and Kashmir',
    'ladakh': 'Ladakh',
    'lakshadweep': 'Lakshadweep',
    'puducherry': 'Puducherry',
    # State codes
    'ap': 'Andhra Pradesh',
    'ar': 'Arunachal Pradesh',
    'as': 'Assam',
    'br': 'Bihar',
    'cg': 'Chhattisgarh',
    'ga': 'Goa',
    'gj': 'Gujarat',
    'hr': 'Haryana',
    'hp': 'Himachal Pradesh',
    'jh': 'Jharkhand',
    'ka': 'Karnataka',
    'kl': 'Kerala',
    'mp': 'Madhya Pradesh',
    'mh': 'Maharashtra',
    'mn': 'Manipur',
    'ml': 'Meghalaya',
    'mz': 'Mizoram',
    'nl': 'Nagaland',
    'or': 'Odisha',
    'pb': 'Punjab',
    'rj': 'Rajasthan',
    'sk': 'Sikkim',
    'tn': 'Tamil Nadu',
    'tg': 'Telangana',
    'tr': 'Tripura',
    'up': 'Uttar Pradesh',
    'uk': 'Uttarakhand',
    'wb': 'West Bengal'
}

def normalize_state_name(state):
    """Normalize state name to standard format"""
    if not state:
        return None
    state_lower = state.lower().strip()
    return INDIAN_STATES.get(state_lower, state)
