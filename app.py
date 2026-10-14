import os
import base64
import requests
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from chat1 import fetch_website_content, extract_pdf_text, initialize_vector_store
from chat2 import (
    analyze_image_with_text, 
    analyze_crop_disease,
    get_farming_advice,
    calculate_resources,
    setup_retrieval_qa,
    setup_sustainability_qa
)
from database import (
    init_db, create_user, verify_user, update_user_location, 
    update_last_login, get_user_by_id, get_all_users, delete_user,
    create_contact_submission, get_all_contacts, update_contact_status,
    log_activity, log_analytics, get_analytics_summary,
    log_prediction, get_user_predictions,
    update_user_language, get_user_language
)
from location_service import get_location_from_coordinates, normalize_state_name, get_open_meteo_weather
from mandi_service import get_mandi_prices, get_all_states, get_all_commodities, get_mandi_summary_stats
from news_service import get_daily_agri_news, get_daily_farming_ads, get_news_categories, get_news_last_updated_time
from auth import login_required, admin_required
from crop_recommendation import (
    predict_crops, get_district_averages, get_crop_guide, 
    get_crop_finance, get_government_schemes, get_soil_labs, load_model
)
from multimodal_remote_sensing import (
    predict_multimodal_disease_and_yield,
    get_preset_scenario,
    create_synthetic_preset_image
)

load_dotenv()

SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'native': 'English', 'region': 'Universal'},
    'hi': {'name': 'Hindi', 'native': 'हिन्दी', 'region': 'North & Central'},
    'pa': {'name': 'Punjabi', 'native': 'ਪੰਜਾਬੀ', 'region': 'Punjab'},
    'bn': {'name': 'Bengali', 'native': 'বাংলা', 'region': 'East India'},
    'mr': {'name': 'Marathi', 'native': 'मराठी', 'region': 'Maharashtra'},
    'gu': {'name': 'Gujarati', 'native': 'ગુજરાતી', 'region': 'Gujarat'},
    'te': {'name': 'Telugu', 'native': 'తెలుగు', 'region': 'Andhra & Telangana'},
    'ta': {'name': 'Tamil', 'native': 'தமிழ்', 'region': 'Tamil Nadu'},
    'kn': {'name': 'Kannada', 'native': 'ಕನ್ನಡ', 'region': 'Karnataka'},
    'ml': {'name': 'Malayalam', 'native': 'മലയാളം', 'region': 'Kerala'}
}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

@app.context_processor
def inject_language_context():
    lang = session.get('language') or request.cookies.get('krishi_lang', 'en')
    return {
        'current_lang': lang,
        'SUPPORTED_LANGUAGES': SUPPORTED_LANGUAGES
    }

WEATHER_API_KEY = "fca22fd77b165be8f104eac5dbd4f4c4"

# Initialize database
init_db()

# Load crop recommendation model
try:
    load_model()
except Exception as e:
    print(f"Warning: Could not load crop model: {e}")

# Initialize agricultural knowledge base
print("Loading agricultural knowledge base...")
db = initialize_vector_store()
chat_chain = setup_retrieval_qa(db)
sustainability_chain = setup_sustainability_qa(db)
print("[OK] Knowledge base and RAG chains initialized successfully!")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mime_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    mime_types = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'gif': 'image/gif', 'webp': 'image/webp'}
    return mime_types.get(ext, 'image/jpeg')

# Routes
@app.route('/')
def index():
    ads = get_daily_farming_ads()
    latest_news = get_daily_agri_news(limit=6)
    return render_template('index.html', ads=ads, latest_news=latest_news)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = verify_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            
            # Load user's default language
            saved_lang = user.get('preferred_language')
            has_chosen_lang = bool(saved_lang and saved_lang in SUPPORTED_LANGUAGES)
            if has_chosen_lang:
                session['language'] = saved_lang
            else:
                session['language'] = 'en'
            
            update_last_login(user['id'])
            log_activity(user['id'], 'login', 'User logged in')
            
            flash('Login successful!', 'success')
            
            # Post-login language selection if user hasn't set default yet
            if not has_chosen_lang and not user['is_admin']:
                return redirect(url_for('select_language'))
                
            if user['is_admin']:
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/select-language', methods=['GET', 'POST'])
def select_language():
    if request.method == 'POST':
        lang = request.form.get('language', 'en').lower()
        if lang in SUPPORTED_LANGUAGES:
            session['language'] = lang
            user_id = session.get('user_id')
            if user_id:
                update_user_language(user_id, lang)
                log_activity(user_id, 'language_changed', f'Default language set to {lang}')
            flash(f"Default language set to {SUPPORTED_LANGUAGES[lang]['native']} ({SUPPORTED_LANGUAGES[lang]['name']})", 'success')
            
            next_url = request.args.get('next') or url_for('index')
            resp = redirect(next_url)
            resp.set_cookie('krishi_lang', lang, max_age=30*24*3600)
            return resp

    current_lang = session.get('language') or request.cookies.get('krishi_lang', 'en')
    return render_template('select_language.html', 
                           languages=SUPPORTED_LANGUAGES, 
                           current_lang=current_lang)

@app.route('/api/set-language', methods=['POST'])
def api_set_language():
    data = request.get_json() or {}
    lang = data.get('language', 'en').lower()
    if lang in SUPPORTED_LANGUAGES:
        session['language'] = lang
        user_id = session.get('user_id')
        if user_id:
            update_user_language(user_id, lang)
            log_activity(user_id, 'language_changed', f'Language changed to {lang}')
        resp = jsonify({
            'success': True, 
            'language': lang, 
            'native': SUPPORTED_LANGUAGES[lang]['native'],
            'name': SUPPORTED_LANGUAGES[lang]['name']
        })
        resp.set_cookie('krishi_lang', lang, max_age=30*24*3600)
        return resp
    return jsonify({'success': False, 'error': 'Unsupported language'}), 400


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        result = create_user(username, email, password, full_name, phone)
        
        if result['success']:
            user_id = result['user_id']
            
            # If location provided, update it
            if latitude and longitude:
                try:
                    lat = float(latitude)
                    lon = float(longitude)
                    
                    # Get location details
                    location_data = get_location_from_coordinates(lat, lon)
                    if location_data['success']:
                        state = normalize_state_name(location_data.get('state'))
                        district = location_data.get('district')
                        update_user_location(user_id, lat, lon, state, district)
                        log_activity(user_id, 'location_updated', f'Location: {district}, {state}')
                except Exception as e:
                    print(f"Location error: {e}")
            
            log_activity(user_id, 'signup', 'New user registered')
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['error'], 'danger')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], 'logout', 'User logged out')
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

# User Profile
@app.route('/profile')
@login_required
def profile():
    user = get_user_by_id(session['user_id'])
    predictions = get_user_predictions(session['user_id'], limit=20)
    return render_template('profile.html', user=user, predictions=predictions)

# About and Contact routes
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        result = create_contact_submission(name, email, subject, message)
        if result['success']:
            flash('Thank you for contacting us! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Error submitting form. Please try again.', 'danger')
    
    return render_template('contact.html')

# Admin routes
@app.route('/admin')
@admin_required
def admin():
    users = get_all_users()
    contacts = get_all_contacts()
    analytics = get_analytics_summary()
    
    return render_template('admin.html', users=users, contacts=contacts, analytics=analytics)

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    try:
        delete_user(user_id)
        log_activity(session['user_id'], 'admin_action', f'Deleted user ID: {user_id}')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/update-contact/<int:contact_id>', methods=['POST'])
@admin_required
def admin_update_contact(contact_id):
    try:
        data = request.get_json()
        status = data.get('status')
        update_contact_status(contact_id, status)
        log_activity(session['user_id'], 'admin_action', f'Updated contact ID: {contact_id} to {status}')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/disease')
def disease():
    return render_template('disease.html')

@app.route('/remote-sensing')
def remote_sensing():
    return render_template('remote_sensing.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/sustainability')
@login_required
def sustainability():
    return render_template('sustainability.html')

# New Feature Routes
@app.route('/crop-recommendation')
@login_required
def crop_recommendation():
    return render_template('crop_recommendation.html')

@app.route('/mandi-prices')
def mandi_prices():
    prices = get_mandi_prices()
    states = get_all_states()
    commodities = get_all_commodities()
    stats = get_mandi_summary_stats()
    return render_template('mandi_prices.html', prices=prices, states=states, commodities=commodities, stats=stats)

@app.route('/api/mandi-prices', methods=['GET', 'POST'])
def api_mandi_prices():
    if request.method == 'POST':
        data = request.get_json() or {}
        state = data.get('state')
        commodity = data.get('commodity')
        query = data.get('query')
    else:
        state = request.args.get('state')
        commodity = request.args.get('commodity')
        query = request.args.get('query')
    
    results = get_mandi_prices(state_filter=state, commodity_filter=commodity, search_query=query)
    return jsonify({
        'success': True,
        'count': len(results),
        'prices': results
    })

@app.route('/crop-guide')
def crop_guide():
    import pandas as pd
    guides_df = pd.read_csv('train/dataset/crop_guides.csv')
    general_crops = guides_df[guides_df['category'] == 'general'].to_dict('records')
    fruit_crops = guides_df[guides_df['category'] == 'fruit'].to_dict('records')
    all_crops = guides_df.to_dict('records')
    crops = sorted(guides_df['crop'].unique())
    return render_template('crop_guide.html', 
                           crops=crops, 
                           general_crops=general_crops, 
                           fruit_crops=fruit_crops,
                           all_crops=all_crops)

@app.route('/krishi-seva')
def krishi_seva():
    schemes = get_government_schemes()
    labs = get_soil_labs()
    states = sorted(list(set(l['state'] for l in labs if l.get('state'))))
    categories = sorted(list(set(s['category'] for s in schemes if s.get('category'))))
    return render_template('krishi_seva.html', schemes=schemes, labs=labs, states=states, categories=categories)

@app.route('/api/soil-labs', methods=['GET', 'POST'])
def api_soil_labs():
    if request.method == 'POST':
        data = request.get_json() or {}
        state = data.get('state')
        district = data.get('district')
        search = data.get('search')
    else:
        state = request.args.get('state')
        district = request.args.get('district')
        search = request.args.get('search')
    
    labs = get_soil_labs(state=state, district=district)
    if search:
        s_lower = search.lower().strip()
        labs = [
            l for l in labs
            if s_lower in str(l.get('lab_name', '')).lower()
            or s_lower in str(l.get('district', '')).lower()
            or s_lower in str(l.get('state', '')).lower()
            or s_lower in str(l.get('services', '')).lower()
            or s_lower in str(l.get('address', '')).lower()
        ]
    return jsonify({'success': True, 'count': len(labs), 'labs': labs})

@app.route('/api/schemes', methods=['GET'])
def api_schemes():
    category = request.args.get('category')
    search = request.args.get('search')
    schemes = get_government_schemes()
    if category and category.lower() != 'all':
        schemes = [s for s in schemes if str(s.get('category', '')).lower() == category.lower()]
    if search:
        q = search.lower().strip()
        schemes = [
            s for s in schemes
            if q in str(s.get('scheme_name', '')).lower()
            or q in str(s.get('full_name', '')).lower()
            or q in str(s.get('description', '')).lower()
            or q in str(s.get('benefits', '')).lower()
            or q in str(s.get('eligibility', '')).lower()
        ]
    return jsonify({'success': True, 'count': len(schemes), 'schemes': schemes})

# Daily Agricultural News & Advertisements Portal
@app.route('/news')
def news_portal():
    category = request.args.get('category')
    search = request.args.get('q')
    force_refresh = request.args.get('refresh') in ['1', 'true', 'True']
    news_items = get_daily_agri_news(category=category, search_query=search, limit=60, force_refresh=force_refresh)
    categories = get_news_categories()
    ads = get_daily_farming_ads()
    last_updated = get_news_last_updated_time()
    return render_template('news.html', 
                           news_items=news_items, 
                           categories=categories, 
                           ads=ads,
                           selected_category=category or 'all',
                           search_query=search or '',
                           last_updated=last_updated)

@app.route('/api/news', methods=['GET', 'POST'])
def api_news():
    force_refresh = False
    if request.method == 'POST':
        data = request.get_json() or {}
        category = data.get('category')
        search = data.get('query')
        force_refresh = bool(data.get('refresh'))
    else:
        category = request.args.get('category')
        search = request.args.get('query') or request.args.get('q')
        force_refresh = request.args.get('refresh') in ['1', 'true', 'True']
    
    items = get_daily_agri_news(category=category, search_query=search, limit=60, force_refresh=force_refresh)
    last_updated = get_news_last_updated_time()
    return jsonify({
        'success': True,
        'count': len(items),
        'last_updated': last_updated,
        'news': items
    })

@app.route('/api/farming-ads', methods=['GET'])
def api_farming_ads():
    ads = get_daily_farming_ads()
    return jsonify({
        'success': True,
        'count': len(ads),
        'ads': ads
    })

# API Endpoints
@app.route('/api/chat', methods=['POST'])
def api_chat():
    query = request.form.get('messageText', '').strip()
    language = request.form.get('language', 'en')
    image_file = request.files.get('image')
    
    # Language names mapping
    language_names = {
        'en': 'English',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'te': 'Telugu',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'or': 'Odia',
        'as': 'Assamese'
    }
    
    language_name = language_names.get(language, 'English')
    
    # Log analytics
    user_id = session.get('user_id')
    if user_id:
        log_analytics(user_id, 'chat', query)
    
    if image_file and image_file.filename and allowed_file(image_file.filename):
        try:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            mime_type = get_mime_type(image_file.filename)
            
            if not query:
                query = "Analyze this agricultural image and provide insights."
            
            # Add language instruction for image analysis
            if language != 'en':
                query = f"{query}\n\nIMPORTANT: Please respond in {language_name} language."
            
            answer = analyze_image_with_text(image_base64, query, mime_type)
            
            # Log prediction
            if user_id:
                log_prediction(user_id, 'chat', f"Image + Query: {query}", answer[:500])
            
            return jsonify({"answer": answer})
        except Exception as e:
            return jsonify({"error": f"Error processing image: {str(e)}"})
    
    if not query:
        return jsonify({"error": "Please provide a message or image."})
    
    # Add language instruction to the query
    if language != 'en':
        enhanced_query = f"{query}\n\nIMPORTANT: Please respond in {language_name} language only. Do not use English."
    else:
        enhanced_query = query
    
    response = chat_chain.invoke(enhanced_query)
    
    # Log prediction
    if user_id:
        log_prediction(user_id, 'chat', query, response[:500])
    
    return jsonify({"answer": response})

@app.route('/api/weather', methods=['POST'])
def api_weather():
    data = request.get_json() or {}
    city = data.get('city', '').strip()
    crop_type = data.get('crop_type', 'general')
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    # Log analytics
    user_id = session.get('user_id')
    if user_id:
        log_analytics(user_id, 'weather', json.dumps({'city': city, 'crop': crop_type}))
    
    if not city and (lat is None or lon is None):
        return jsonify({"error": "Please provide a city name or coordinates."})
    
    # Fetch live precision agro-meteorological weather via Open-Meteo
    weather_info = get_open_meteo_weather(city_name=city or 'Ludhiana', lat=lat, lon=lon)
    
    # Adapter for farming advice engine
    weather_data_for_advice = {
        'name': weather_info.get('city', city.title()),
        'main': {
            'temp': weather_info.get('temp', 26.5),
            'humidity': weather_info.get('humidity', 62)
        },
        'weather': [{
            'description': weather_info.get('description', 'Partly cloudy'),
            'icon': weather_info.get('icon', '02d')
        }],
        'wind': {'speed': weather_info.get('wind_speed', 3.5)}
    }

    advice = get_farming_advice(weather_data_for_advice, crop_type)

    return jsonify({
        "weather": {
            "city": weather_info.get('city'),
            "state": weather_info.get('state'),
            "temp": weather_info.get('temp'),
            "feels_like": weather_info.get('feels_like'),
            "humidity": weather_info.get('humidity'),
            "description": weather_info.get('description'),
            "detailed_desc": weather_info.get('detailed_desc'),
            "wind_speed": weather_info.get('wind_speed'),
            "precipitation": weather_info.get('precipitation'),
            "icon": weather_info.get('icon'),
            "forecast": weather_info.get('forecast', [])
        },
        "advice": advice
    })

@app.route('/api/disease', methods=['POST'])
def api_disease():
    image_file = request.files.get('image')
    
    # Log analytics
    user_id = session.get('user_id')
    if user_id:
        log_analytics(user_id, 'disease_detection', 'Image uploaded')
    
    if not image_file or not image_file.filename:
        return jsonify({"error": "Please upload an image of the crop."})
    
    if not allowed_file(image_file.filename):
        return jsonify({"error": "Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP."})
    
    try:
        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        mime_type = get_mime_type(image_file.filename)
        
        diagnosis = analyze_crop_disease(image_base64, mime_type)
        
        # Log prediction
        if user_id:
            log_prediction(user_id, 'disease', 'Crop image uploaded', diagnosis[:500])
        
        return jsonify({"diagnosis": diagnosis})
    except Exception as e:
        return jsonify({"error": f"Error analyzing image: {str(e)}"})

@app.route('/api/multimodal-predict', methods=['POST'])
def api_multimodal_predict():
    """
    Multimodal Remote Sensing & Micro-Climate Telemetry Prediction API
    Executes Gated Cross-Attention Fusion -> Grad-CAM Heatmap + Disease Risk + Yield Forecast
    """
    try:
        # 1. Extract image bytes (multipart file OR base64 payload)
        image_bytes = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_bytes = file.read()
        
        if not image_bytes:
            b64_img = None
            if request.is_json:
                json_data = request.get_json() or {}
                b64_img = json_data.get('image_base64', '')
            elif 'image_base64' in request.form:
                b64_img = request.form.get('image_base64', '')
            
            if b64_img:
                if ',' in b64_img:
                    b64_img = b64_img.split(',', 1)[1]
                image_bytes = base64.b64decode(b64_img)

        # 2. Extract telemetry features (form or json)
        form_data = request.form if request.form else (request.get_json() or {})
        crop_name = form_data.get('crop_name', 'wheat')
        temperature = float(form_data.get('temperature', 26.5))
        humidity = float(form_data.get('humidity', 75.0))
        rainfall_7d = float(form_data.get('rainfall_7d', 25.0))
        soil_moisture = float(form_data.get('soil_moisture', 60.0))
        vpd = float(form_data.get('vpd', 1.2))
        canopy_source = form_data.get('canopy_source', 'Sentinel-2 Multispectral')

        # Fallback to synthetic preset if no image provided
        if not image_bytes:
            image_bytes = create_synthetic_preset_image('punjab_wheat_rust')

        results = predict_multimodal_disease_and_yield(
            image_bytes=image_bytes,
            crop_name=crop_name,
            temperature=temperature,
            humidity=humidity,
            rainfall_7d=rainfall_7d,
            soil_moisture=soil_moisture,
            vpd=vpd,
            canopy_source=canopy_source
        )

        user_id = session.get('user_id')
        if user_id:
            log_prediction(
                user_id,
                'multimodal_remote_sensing',
                f"{crop_name}, T={temperature}C, RH={humidity}%",
                f"{results['diagnosis']['name']} | Yield: {results['yield_forecast']['estimated_yield_q_ha']} q/ha"
            )

        return jsonify(results)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/sample-remote-sensing/<scenario_id>', methods=['GET'])
def api_sample_remote_sensing(scenario_id):
    """Returns preset scenario parameters and synthetic multispectral canopy imagery"""
    try:
        scenario = get_preset_scenario(scenario_id)
        img_bytes = create_synthetic_preset_image(scenario_id)
        b64_img = base64.b64encode(img_bytes).decode('utf-8')
        return jsonify({
            "success": True,
            "scenario": scenario,
            "image_data_url": f"data:image/jpeg;base64,{b64_img}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    
    crop_type = data.get('crop_type', '')
    area = data.get('area', '')
    area_unit = data.get('area_unit', 'acres')
    soil_type = data.get('soil_type', 'loamy')
    growth_stage = data.get('growth_stage', 'vegetative')
    
    # Log analytics
    user_id = session.get('user_id')
    if user_id:
        log_analytics(user_id, 'calculator', json.dumps({'crop': crop_type, 'area': area}))
    
    if not crop_type or not area:
        return jsonify({"error": "Please provide crop type and area."})
    
    try:
        result = calculate_resources(crop_type, area, area_unit, soil_type, growth_stage)
        
        # Log prediction
        if user_id:
            input_str = f"{crop_type}, {area} {area_unit}, {soil_type}, {growth_stage}"
            log_prediction(user_id, 'calculator', input_str, result[:500])
        
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": f"Error calculating: {str(e)}"})

@app.route('/api/calculate-profit', methods=['POST'])
@login_required
def api_calculate_profit():
    data = request.get_json()
    
    crop_type = data.get('crop_type', '')
    area = float(data.get('area', 0))
    area_unit = data.get('area_unit', 'acres')
    area_hectares = float(data.get('area_hectares', 0))
    soil_type = data.get('soil_type', 'loamy')
    growth_stage = data.get('growth_stage', 'vegetative')
    
    if not crop_type or not area:
        return jsonify({"error": "Please provide crop type and area."})
    
    try:
        # Get crop finance data
        import pandas as pd
        finance_df = pd.read_csv('train/dataset/india_crop_production.csv')
        crop_data = finance_df[finance_df['Crop'].str.lower() == crop_type.lower()]
        
        if not crop_data.empty:
            crop_info = crop_data.iloc[0]
            cost_per_hectare = float(crop_info['Cost of Cultivation (`/Hectare) C2'])
            yield_per_hectare = float(crop_info['Yield (Quintal/ Hectare) '])
            cost_per_quintal = float(crop_info['Cost of Production (`/Quintal) C2'])
            
            # Calculate based on actual data
            total_cost = cost_per_hectare * area_hectares
            expected_yield = yield_per_hectare * area_hectares
            price_per_quintal = cost_per_quintal * 1.3  # Assume 30% markup for selling price
            total_revenue = expected_yield * price_per_quintal
            net_profit = total_revenue - total_cost
            profit_margin = ((net_profit / total_revenue) * 100) if total_revenue > 0 else 0
            roi = ((net_profit / total_cost) * 100) if total_cost > 0 else 0
            
            profit_analysis = {
                'cost_per_hectare': round(cost_per_hectare, 2),
                'yield_per_hectare': round(yield_per_hectare, 2),
                'price_per_quintal': round(price_per_quintal, 2),
                'total_cost': round(total_cost, 2),
                'expected_yield': round(expected_yield, 2),
                'total_revenue': round(total_revenue, 2),
                'net_profit': round(net_profit, 2),
                'profit_margin': round(profit_margin, 2),
                'roi': round(roi, 2)
            }
        else:
            # Use estimates if crop not in database
            cost_per_hectare = 50000
            yield_per_hectare = 30
            price_per_quintal = 2000
            
            total_cost = cost_per_hectare * area_hectares
            expected_yield = yield_per_hectare * area_hectares
            total_revenue = expected_yield * price_per_quintal
            net_profit = total_revenue - total_cost
            profit_margin = ((net_profit / total_revenue) * 100) if total_revenue > 0 else 0
            roi = ((net_profit / total_cost) * 100) if total_cost > 0 else 0
            
            profit_analysis = {
                'cost_per_hectare': cost_per_hectare,
                'yield_per_hectare': yield_per_hectare,
                'price_per_quintal': price_per_quintal,
                'total_cost': round(total_cost, 2),
                'expected_yield': round(expected_yield, 2),
                'total_revenue': round(total_revenue, 2),
                'net_profit': round(net_profit, 2),
                'profit_margin': round(profit_margin, 2),
                'roi': round(roi, 2)
            }
        
        # Get resource requirements from AI
        resources = calculate_resources(crop_type, str(area), area_unit, soil_type, growth_stage)
        
        # Log prediction
        user_id = session.get('user_id')
        if user_id:
            input_str = f"{crop_type}, {area} {area_unit}"
            output_str = f"Profit: ₹{net_profit:.2f}"
            log_prediction(user_id, 'profit_calculator', input_str, output_str)
        
        return jsonify({
            'profit_analysis': profit_analysis,
            'resources': resources
        })
        
    except Exception as e:
        return jsonify({"error": f"Error calculating: {str(e)}"}), 400

@app.route('/api/sustainability', methods=['POST'])
def api_sustainability():
    data = request.get_json()
    query = data.get('query', '').strip()
    
    # Log analytics
    user_id = session.get('user_id')
    if user_id:
        log_analytics(user_id, 'sustainability', query)
    
    if not query:
        return jsonify({"error": "Please provide a question about sustainable farming."})
    
    response = sustainability_chain.invoke(query)
    return jsonify({"answer": response})

# New API Endpoints
@app.route('/api/predict-crop', methods=['POST'])
@login_required
def api_predict_crop():
    data = request.get_json()
    
    try:
        result = predict_crops(
            N=data['N'],
            P=data['P'],
            K=data['K'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            ph=data['ph'],
            rainfall=data['rainfall']
        )
        
        # Log prediction
        user_id = session.get('user_id')
        if user_id:
            input_str = f"N:{data['N']}, P:{data['P']}, K:{data['K']}"
            output_str = f"Top: {result['top_crops'][0]['crop']}"
            log_prediction(user_id, 'crop_recommendation', input_str, output_str, 
                         result['top_crops'][0]['probability']/100)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/get-district-averages', methods=['POST'])
@login_required
def api_get_district_averages():
    data = request.get_json()
    state = data.get('state')
    district = data.get('district')
    
    averages = get_district_averages(state, district)
    return jsonify(averages)

@app.route('/api/get-crop-guide/<crop>', methods=['GET'])
def api_get_crop_guide(crop):
    guide = get_crop_guide(crop)
    if guide:
        user_id = session.get('user_id')
        if user_id:
            log_analytics(user_id, 'crop_guide', crop)
        return jsonify(guide)
    return jsonify({"error": "Crop guide not found"}), 404

@app.route('/api/get-location', methods=['POST'])
@login_required
def api_get_location():
    """Get location details from coordinates"""
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude required"}), 400
    
    try:
        location_data = get_location_from_coordinates(float(latitude), float(longitude))
        
        if location_data['success']:
            state = normalize_state_name(location_data.get('state'))
            district = location_data.get('district')
            city = location_data.get('city')
            
            # Update user location
            user_id = session.get('user_id')
            if user_id:
                update_user_location(user_id, float(latitude), float(longitude), state, district)
            
            return jsonify({
                'success': True,
                'state': state,
                'district': district,
                'city': city,
                'full_address': location_data.get('full_address')
            })
        else:
            return jsonify({"error": location_data.get('error', 'Location not found')}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n" + "="*65)
    print("  [OK] Krishi Mitra: AI-Powered Smart Farming Assistant")
    print("  [OK] Running directly at: http://127.0.0.1:5000")
    print("  [OK] Default Admin: admin / admin123")
    print("="*65 + "\n")
    app.run(debug=True, host="127.0.0.1", port=5000)

