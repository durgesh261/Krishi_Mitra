import unittest
import json
import base64
import io
import sys
from PIL import Image
from app import app

# Ensure utf-8 output if possible
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class TestKrishiMitraApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def login_admin(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['is_admin'] = True

    def test_01_public_pages(self):
        # Home
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Krishi Mitra', res.data)

        # About
        res = self.client.get('/about')
        self.assertEqual(res.status_code, 200)

        # Contact
        res = self.client.get('/contact')
        self.assertEqual(res.status_code, 200)

        # Login
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)

    def test_02_crop_prediction_api(self):
        self.login_admin()
        payload = {
            'N': 90,
            'P': 42,
            'K': 43,
            'temperature': 20.8,
            'humidity': 82.0,
            'ph': 6.5,
            'rainfall': 202.9
        }
        res = self.client.post('/api/predict-crop', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('top_crops', data)
        self.assertIn('confidence', data)
        self.assertIn('entropy', data)
        self.assertEqual(data['top_crops'][0]['crop'], 'Rice')
        print(f"  [PASS] Crop Prediction: Top is {data['top_crops'][0]['crop']} with {data['confidence']} confidence")

    def test_03_crop_guide_and_district_averages(self):
        self.login_admin()
        # Crop guide page
        res = self.client.get('/crop-guide')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'tabGeneralCrops', res.data)
        self.assertIn(b'tabFruitCrops', res.data)

        # General Crop guide (rice)
        res = self.client.get('/api/get-crop-guide/rice')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['crop'].lower(), 'rice')
        self.assertEqual(data['category'], 'general')
        print(f"  [PASS] General Crop Guide: {data['crop']} (Category: {data['category']}) loaded")

        # Fruit Crop guide (mango)
        res = self.client.get('/api/get-crop-guide/mango')
        self.assertEqual(res.status_code, 200)
        data_fruit = res.get_json()
        self.assertEqual(data_fruit['crop'].lower(), 'mango')
        self.assertEqual(data_fruit['category'], 'fruit')
        print(f"  [PASS] Fruit Crop Guide: {data_fruit['crop']} (Category: {data_fruit['category']}) loaded")

        # Crop alias resolution (chana -> chickpea)
        res = self.client.get('/api/get-crop-guide/chana')
        self.assertEqual(res.status_code, 200)
        data_alias = res.get_json()
        self.assertEqual(data_alias['crop'].lower(), 'chickpea')
        print(f"  [PASS] Crop Alias: chana resolved to {data_alias['crop']}")

        # District averages
        res = self.client.post('/api/get-district-averages', 
                               data=json.dumps({'state': 'Punjab', 'district': 'Ludhiana'}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)
        avg = res.get_json()
        self.assertIn('N', avg)
        print(f"  [PASS] District Averages for Ludhiana: N={avg['N']}, rainfall={avg['rainfall']}")

    def test_04_profit_calculator(self):
        self.login_admin()
        payload = {
            'crop_type': 'rice',
            'area': 2.5,
            'area_unit': 'acres',
            'area_hectares': 1.011,
            'soil_type': 'loamy',
            'growth_stage': 'vegetative'
        }
        res = self.client.post('/api/calculate-profit', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('profit_analysis', data)
        self.assertIn('resources', data)
        print(f"  [PASS] Profit Calculator: Total Cost = {data['profit_analysis']['total_cost']}, Net Profit = {data['profit_analysis']['net_profit']}")

    def test_05_weather_advisory(self):
        payload = {'city': 'Ludhiana', 'crop_type': 'wheat'}
        res = self.client.post('/api/weather', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('weather', data)
        self.assertIn('advice', data)
        print(f"  [PASS] Weather Advisory for {data['weather']['city']}: {data['weather']['temp']} C")

    def test_06_rag_chat_and_sustainability(self):
        # Chat
        res = self.client.post('/api/chat', data={'messageText': 'What is PM-KISAN scheme and benefits?', 'language': 'en'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('answer', data)
        self.assertTrue(len(data['answer']) > 20)
        print("  [PASS] RAG Chat response successfully received")

        # Hindi Chat
        res_hi = self.client.post('/api/chat', data={'messageText': 'फसल में जैविक खाद कैसे डालें?', 'language': 'hi'})
        self.assertEqual(res_hi.status_code, 200)
        data_hi = res_hi.get_json()
        self.assertIn('answer', data_hi)
        print("  [PASS] Hindi Chat response successfully received")

        # Non-agricultural rejection test (e.g. 'nbvc')
        res_non_agri = self.client.post('/api/chat', data={'messageText': 'nbvc', 'language': 'en'})
        self.assertEqual(res_non_agri.status_code, 200)
        data_non_agri = res_non_agri.get_json()
        self.assertIn('Krishi Mitra is dedicated exclusively', data_non_agri['answer'])
        print("  [PASS] Non-agricultural query 'nbvc' successfully rejected with guardrail message")

        # Sustainability
        res_sust = self.client.post('/api/sustainability', data=json.dumps({'query': 'Best water conservation techniques'}), content_type='application/json')
        self.assertEqual(res_sust.status_code, 200)
        data_sust = res_sust.get_json()
        self.assertIn('answer', data_sust)
        print("  [PASS] Sustainability advice successfully received")

    def test_07_disease_detection(self):
        img = Image.new('RGB', (100, 100), color=(34, 139, 34))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        buf.seek(0)

        data = {
            'image': (buf, 'leaf.jpg')
        }
        res = self.client.post('/api/disease', data=data, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)
        diag = res.get_json()
        self.assertIn('diagnosis', diag)
        print("  [PASS] Disease Detection diagnosis generated successfully")

    def test_08_location_service(self):
        self.login_admin()
        payload = {'latitude': 30.9, 'longitude': 75.8}
        res = self.client.post('/api/get-location', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        loc = res.get_json()
        self.assertTrue(loc.get('success'))
        self.assertEqual(loc.get('state'), 'Punjab')
        print(f"  [PASS] Location Geocoding: State = {loc.get('state')}, District = {loc.get('district')}")

    def test_09_admin_dashboard(self):
        self.login_admin()
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Admin Dashboard', res.data)
        print("  [PASS] Admin Dashboard rendered without errors")

    def test_10_regional_languages(self):
        self.login_admin()
        # 1. GET /select-language
        res = self.client.get('/select-language')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Choose Your Language', res.data)
        print("  [PASS] GET /select-language rendered correctly")

        # 2. POST /select-language (e.g. Hindi)
        res_post = self.client.post('/select-language', data={'language': 'hi'}, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        print("  [PASS] POST /select-language successfully set Hindi as default")

        # 3. POST /api/set-language (e.g. Punjabi)
        res_api = self.client.post('/api/set-language', 
                                   data=json.dumps({'language': 'pa'}),
                                   content_type='application/json')
        self.assertEqual(res_api.status_code, 200)
        data = res_api.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('language'), 'pa')
        print("  [PASS] POST /api/set-language switched language to Punjabi (pa)")

        # 4. Check invalid language rejection
        res_invalid = self.client.post('/api/set-language', 
                                       data=json.dumps({'language': 'xx'}),
                                       content_type='application/json')
        self.assertEqual(res_invalid.status_code, 400)
        print("  [PASS] /api/set-language rejected unsupported language code")

    def test_11_mandi_prices(self):
        # 1. GET /mandi-prices
        res = self.client.get('/mandi-prices')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Mandi Bhav', res.data)
        print("  [PASS] GET /mandi-prices rendered successfully")

        # 2. GET /api/mandi-prices
        res_api = self.client.get('/api/mandi-prices?state=Punjab')
        self.assertEqual(res_api.status_code, 200)
        data = res_api.get_json()
        self.assertTrue(data.get('success'))
        self.assertGreater(data.get('count'), 0)
        print(f"  [PASS] GET /api/mandi-prices filtered by state: {data.get('count')} records found")

    def test_12_indian_crops_prediction(self):
        self.login_admin()
        # Test Wheat prediction with realistic wheat soil & climate
        payload_wheat = {
            'N': 115, 'P': 48, 'K': 46,
            'temperature': 19.0, 'humidity': 60.0, 'ph': 6.8, 'rainfall': 65.0
        }
        res = self.client.post('/api/predict-crop', data=json.dumps(payload_wheat), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        top_crop = data['top_crops'][0]['crop']
        print(f"  [PASS] Indian Wheat prediction: Top recommended crop = {top_crop} (Confidence = {data['confidence']})")

    def test_13_krishi_seva_hub(self):
        # 1. GET /krishi-seva
        res = self.client.get('/krishi-seva')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Krishi Seva Hub', res.data)
        self.assertIn(b'PM-KISAN', res.data)
        self.assertIn(b'PM-KUSUM', res.data)
        print("  [PASS] GET /krishi-seva rendered successfully with schemes and labs")

        # 2. GET /api/soil-labs?state=Punjab
        res_labs = self.client.get('/api/soil-labs?state=Punjab')
        self.assertEqual(res_labs.status_code, 200)
        data_labs = res_labs.get_json()
        self.assertTrue(data_labs.get('success'))
        self.assertGreater(data_labs.get('count'), 0)
        print(f"  [PASS] GET /api/soil-labs filtered by state: {data_labs.get('count')} labs found")

        # 3. GET /api/schemes?category=Solar+%26+Energy
        res_schemes = self.client.get('/api/schemes?search=KUSUM')
        self.assertEqual(res_schemes.status_code, 200)
        data_schemes = res_schemes.get_json()
        self.assertTrue(data_schemes.get('success'))
        self.assertGreater(data_schemes.get('count'), 0)
        print(f"  [PASS] GET /api/schemes filtered by search: found {data_schemes['schemes'][0]['scheme_name']}")

    def test_14_farming_ads_and_daily_news(self):
        # 1. GET / - homepage contains ad carousel and news spotlight
        res_home = self.client.get('/')
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b'ad-carousel-section', res_home.data)
        self.assertIn(b'home-news-section', res_home.data)
        print("  [PASS] GET / renders with sliding ad carousel and daily news spotlight")

        # 2. GET /news - dedicated news portal
        res_news = self.client.get('/news')
        self.assertEqual(res_news.status_code, 200)
        self.assertIn(b'Daily Krishi Samachar', res_news.data)
        self.assertIn(b'news-sidebar', res_news.data)
        print("  [PASS] GET /news rendered successfully with news feed and partner ads sidebar")

        # 3. GET /api/news - news feed API
        res_api_news = self.client.get('/api/news')
        self.assertEqual(res_api_news.status_code, 200)
        data_news = res_api_news.get_json()
        self.assertTrue(data_news.get('success'))
        self.assertGreaterEqual(len(data_news.get('news', [])), 5)
        first_item = data_news['news'][0]
        self.assertIn('title', first_item)
        self.assertIn('category', first_item)
        self.assertIn('source_url', first_item)
        print(f"  [PASS] GET /api/news returned {len(data_news['news'])} stories (Latest: {first_item['title'][:40]}...)")

        # 4. GET /api/news?category=Subsidies & Schemes
        res_cat = self.client.get('/api/news?category=Subsidies+%26+Schemes')
        self.assertEqual(res_cat.status_code, 200)
        data_cat = res_cat.get_json()
        self.assertTrue(data_cat.get('success'))
        print(f"  [PASS] GET /api/news filtered by category: {len(data_cat['news'])} subsidy news items")

        # 5. GET /api/farming-ads - verified deals & subsidies API
        res_ads = self.client.get('/api/farming-ads')
        self.assertEqual(res_ads.status_code, 200)
        data_ads = res_ads.get_json()
        self.assertTrue(data_ads.get('success'))
        self.assertGreaterEqual(len(data_ads.get('ads', [])), 4)
        first_ad = data_ads['ads'][0]
        self.assertIn('title', first_ad)
        self.assertIn('badge', first_ad)
        self.assertIn('helpline', first_ad)
        print(f"  [PASS] GET /api/farming-ads returned {len(data_ads['ads'])} ads (First: {first_ad['title']})")

    def test_15_multimodal_remote_sensing(self):
        # 1. GET /remote-sensing
        res = self.client.get('/remote-sensing')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Multi-Spectral Remote Sensing', res.data)
        print("  [PASS] GET /remote-sensing rendered successfully")

        # 2. GET /api/sample-remote-sensing/punjab_wheat_rust & kashmir_apple_scab
        res_sample = self.client.get('/api/sample-remote-sensing/punjab_wheat_rust')
        self.assertEqual(res_sample.status_code, 200)
        sample_data = res_sample.get_json()
        self.assertTrue(sample_data.get('success'))
        self.assertIn('image_data_url', sample_data)

        res_apple = self.client.get('/api/sample-remote-sensing/kashmir_apple_scab')
        self.assertEqual(res_apple.status_code, 200)
        apple_data = res_apple.get_json()
        self.assertTrue(apple_data.get('success'))
        self.assertEqual(apple_data['scenario']['crop'], 'apple')
        print("  [PASS] GET /api/sample-remote-sensing loaded Punjab Wheat & Kashmir Apple presets")

        # 3. POST /api/multimodal-predict for Cereal (Wheat)
        payload = {
            'crop_name': 'wheat',
            'temperature': 21.5,
            'humidity': 84.0,
            'rainfall_7d': 42.0,
            'soil_moisture': 72.0,
            'vpd': 0.8,
            'canopy_source': 'Sentinel-2 Multispectral'
        }
        res_pred = self.client.post('/api/multimodal-predict', data=payload)
        self.assertEqual(res_pred.status_code, 200)
        pred_data = res_pred.get_json()
        self.assertTrue(pred_data.get('success'))
        self.assertIn('diagnosis', pred_data)
        self.assertIn('yield_forecast', pred_data)
        self.assertIn('spectral_indices', pred_data)
        self.assertIn('gradcam_image', pred_data)
        self.assertTrue(len(pred_data['diagnosis']['crop_specific_advisory']) > 0)
        diag_name = pred_data['diagnosis']['name']
        ndvi_val = pred_data['spectral_indices']['ndvi']
        yield_val = pred_data['yield_forecast']['estimated_yield_q_ha']
        print(f"  [PASS] Wheat Multimodal: Diagnosis = {diag_name}, NDVI = {ndvi_val}, Yield = {yield_val} q/ha")

        # 4. Multimodal test across Fruit (Apple), Commercial (Sugarcane), and Pulse (Chickpea)
        for crop_test, temp_t, rh_t in [('apple', 16.0, 85.0), ('sugarcane', 30.0, 85.0), ('chickpea', 22.0, 55.0)]:
            p = {
                'crop_name': crop_test,
                'temperature': temp_t,
                'humidity': rh_t,
                'rainfall_7d': 25.0,
                'soil_moisture': 65.0,
                'vpd': 1.0,
                'canopy_source': 'Drone Multispectral'
            }
            r = self.client.post('/api/multimodal-predict', data=p)
            self.assertEqual(r.status_code, 200)
            d = r.get_json()
            self.assertTrue(d.get('success'))
            base_q = d['yield_forecast']['district_baseline_q_ha']
            est_q = d['yield_forecast']['estimated_yield_q_ha']
            self.assertTrue(base_q > 0)
            self.assertTrue(est_q > 0)
            self.assertTrue(len(d['diagnosis']['crop_specific_advisory']) > 0)
            print(f"  [PASS] {crop_test.capitalize()} Multimodal ({d['crop_category']}/{d['crop_sub_category']}): Baseline={base_q} q/ha, Est={est_q} q/ha")

    def test_16_news_and_farmer_community_reports(self):
        # 1. News HTML portal
        res = self.client.get('/news')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Daily Krishi Samachar', res.data)
        self.assertIn(b'Post Farmer News', res.data)
        self.assertIn(b'submitNewsModal', res.data)
        print("  [PASS] News HTML portal: Loaded successfully with Farmer News modal and actions")

        # 2. News API JSON endpoint
        res_api = self.client.get('/api/news')
        self.assertEqual(res_api.status_code, 200)
        api_data = res_api.get_json()
        self.assertTrue(api_data['success'])
        self.assertTrue(api_data['count'] > 0)
        self.assertTrue(len(api_data['news']) > 0)
        print(f"  [PASS] News API: Retrieved {api_data['count']} active agricultural headlines")

        # 3. Submit a new farmer community news advisory
        farmer_payload = {
            'title': 'Test Mandi Alert: Fresh Sharbati Wheat arrival touched 3200 per quintal in Sehore',
            'summary': 'High protein quality grain is receiving strong bidding from flour millers. Clean dry grain brings spot cash payments.',
            'category': 'Market & Mandi',
            'author_name': 'Kisan Bhai Rajesh',
            'village_district': 'Sehore Mandi',
            'state': 'Madhya Pradesh',
            'contact': '9876543210'
        }
        res_submit = self.client.post('/api/news/submit',
                                      data=json.dumps(farmer_payload),
                                      content_type='application/json')
        self.assertEqual(res_submit.status_code, 200)
        sub_data = res_submit.get_json()
        self.assertTrue(sub_data['success'])
        self.assertIn('news_id', sub_data)
        news_id = sub_data['news_id']
        print(f"  [PASS] Farmer News Submission: Successfully posted new advisory (ID #{news_id})")

        # 4. Upvote the farmer report
        res_upvote = self.client.post(f'/api/news/upvote/{news_id}')
        self.assertEqual(res_upvote.status_code, 200)
        upvote_data = res_upvote.get_json()
        self.assertTrue(upvote_data['success'])
        self.assertEqual(upvote_data['upvotes'], 1)
        print(f"  [PASS] Farmer News Upvote: Incremented upvotes to {upvote_data['upvotes']}")

        # 5. Live Feed Refresh API
        res_refresh = self.client.get('/api/news/refresh')
        self.assertEqual(res_refresh.status_code, 200)
        ref_data = res_refresh.get_json()
        self.assertTrue(ref_data['success'])
        self.assertTrue(ref_data['count'] > 0)
        self.assertIn('last_updated', ref_data)
        print(f"  [PASS] News Live Refresh API: Live feed synchronized with {ref_data['count']} stories (Last sync: {ref_data['last_updated']})")

if __name__ == '__main__':
    unittest.main()



