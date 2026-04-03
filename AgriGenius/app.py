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
    log_prediction, get_user_predictions
)
from location_service import get_location_from_coordinates, normalize_state_name
from auth import login_required, admin_required
from crop_recommendation import (
    predict_crops, get_district_averages, get_crop_guide, 
    get_crop_finance, get_government_schemes, get_soil_labs, load_model
)

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

WEATHER_API_KEY = "fca22fd77b165be8f104eac5dbd4f4c4"

# Initialize database
init_db()

# Load crop recommendation model
try:
    load_model()
except Exception as e:
    print(f"Warning: Could not load crop model: {e}")

# Initialize knowledge base
print("Loading knowledge base...")
import os

# Check if vector store already exists
VECTOR_STORE_PATH = "chroma_db"

if os.path.exists(VECTOR_STORE_PATH):
    # Load existing vector store (fast)
    print("Loading cached vector store...")
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
    from langchain_community.vectorstores import Chroma
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embedding_function)
    print("Vector store loaded from cache!")
else:
    # Build vector store from scratch (slow, first time only)
    print("Building vector store (this will take a few minutes on first run)...")
    urls = ["https://mospi.gov.in/4-agricultural-statistics"]
    pdf_files = ["Data/Farming Schemes.pdf", "Data/farmerbook.pdf"]
    
    website_contents = [fetch_website_content(url) for url in urls]
    pdf_texts = [extract_pdf_text(pdf_file) for pdf_file in pdf_files]
    all_contents = website_contents + pdf_texts
    
    from chat1 import initialize_vector_store_persistent
    db = initialize_vector_store_persistent(all_contents, VECTOR_STORE_PATH)
    print("Vector store built and cached!")

chat_chain = setup_retrieval_qa(db)
sustainability_chain = setup_sustainability_qa(db)

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
    return render_template('index.html')

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
            
            update_last_login(user['id'])
            log_activity(user['id'], 'login', 'User logged in')
            
            flash('Login successful!', 'success')
            
            if user['is_admin']:
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

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

@app.route('/crop-guide')
@login_required
def crop_guide():
    import pandas as pd
    guides_df = pd.read_csv('train/dataset/crop_guides.csv')
    crops = sorted(guides_df['crop'].unique())
    return render_template('crop_guide.html', crops=crops)

@app.route('/krishi-seva')
@login_required
def krishi_seva():
    schemes = get_government_schemes()
    labs = get_soil_labs()
    return render_template('krishi_seva.html', schemes=schemes, labs=labs)

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
    data = request.get_json()
    city = data.get('city', '')
    crop_type = data.get('crop_type', 'general')
    
    # Log analytics
    user_id = session.get('user_id')
    if user_id:
        log_analytics(user_id, 'weather', json.dumps({'city': city, 'crop': crop_type}))
    
    if not city:
        return jsonify({"error": "Please provide a city name."})
    
    if not WEATHER_API_KEY or WEATHER_API_KEY == "yo    ur_openweathermap_api_key_here":
        return jsonify({"error": "Weather API key not configured. Please add your OpenWeatherMap API key to .env file."})
    
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_response.status_code != 200:
            error_msg = weather_data.get('message', 'Unknown error')
            return jsonify({"error": f"Could not fetch weather for {city}: {error_msg}"})
        
        advice = get_farming_advice(weather_data, crop_type)
        
        return jsonify({
            "weather": {
                "city": weather_data.get('name'),
                "temp": weather_data.get('main', {}).get('temp'),
                "humidity": weather_data.get('main', {}).get('humidity'),
                "description": weather_data.get('weather', [{}])[0].get('description'),
                "wind_speed": weather_data.get('wind', {}).get('speed'),
                "icon": weather_data.get('weather', [{}])[0].get('icon')
            },
            "advice": advice
        })
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})

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
@login_required
def api_get_crop_guide(crop):
    guide = get_crop_guide(crop)
    if guide:
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
    app.run(debug=True)
