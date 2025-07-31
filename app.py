# import os
# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from utils.image_preprocess import predict_bird_from_image
# from utils.audio_preprocess import predict_bird_from_audio
# from gemini_info import get_bird_info
# from google_search import get_bird_image_url
# from dotenv import load_dotenv
# from werkzeug.utils import secure_filename
# import pandas as pd
# from geopy.geocoders import Nominatim
# from flask import request, redirect
# from datetime import datetime
# import pandas as pd
# import os
# from geopy.geocoders import Nominatim
# import wikipedia
#
#
#
#
#
#
# load_dotenv()
#
# app = Flask(__name__)
# app.secret_key = "supersecretkey"
#
# UPLOAD_FOLDER_IMG = 'static/uploads'
# UPLOAD_FOLDER_AUDIO = 'static/wav_uploads'
#
# app.config['UPLOAD_FOLDER_IMG'] = UPLOAD_FOLDER_IMG
# app.config['UPLOAD_FOLDER_AUDIO'] = UPLOAD_FOLDER_AUDIO
#
# os.makedirs(UPLOAD_FOLDER_IMG, exist_ok=True)
# os.makedirs(UPLOAD_FOLDER_AUDIO, exist_ok=True)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/audio_page')
# def audio_page():
#     return render_template('audio_page.html')
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/report')
# def report():
#     return render_template('report.html')
#
# @app.route('/bird_attributes')
# def bird_attributes():
#     return render_template('bird_attributes.html')
#
# @app.route("/bird-map")
# def bird_map_page():
#     return render_template("bird_map.html")
#
# @app.route("/api/bird-map-data")
# def bird_map_data():
#     base_df = pd.read_csv("geocoded_metadata.csv")
#
#     # Try to load user reports if present
#     if os.path.exists("user_reports.csv"):
#         user_df = pd.read_csv("user_reports.csv")
#         combined = pd.concat([base_df, user_df], ignore_index=True)
#     else:
#         combined = base_df
#
#     data = combined[["English Name", "Location", "Date", "latitude", "longitude"]].dropna().to_dict(orient="records")
#     return jsonify(data)
#
#
#
# @app.route('/report_sighting', methods=['POST'])
# def report_sighting():
#     bird_name = request.form['bird_name']
#     location = request.form['location']
#     date = request.form['date']
#     notes = request.form.get('notes', '')
#
#     # Geocode location
#     geolocator = Nominatim(user_agent="pakshi-bird-reporter")
#     loc = geolocator.geocode(location)
#     if not loc:
#         return "❌ Location could not be geocoded. Please try again with a valid location.", 400
#
#     # Prepare data
#     new_row = {
#         "English Name": bird_name,
#         "Location": location,
#         "Date": date,
#         "Notes": notes,
#         "latitude": loc.latitude,
#         "longitude": loc.longitude
#     }
#
#     # Append to CSV
#     report_path = "user_reports.csv"
#     df_new = pd.DataFrame([new_row])
#     if os.path.exists(report_path):
#         df_new.to_csv(report_path, mode='a', header=False, index=False)
#     else:
#         df_new.to_csv(report_path, index=False)
#
#     return redirect("/bird-map")
#
#
# @app.route('/report_from_prediction', methods=['POST'])
# def report_from_prediction():
#     bird_name = request.form['bird_name']
#     location = request.form['location']
#     date = request.form.get('date') or datetime.now().strftime("%Y-%m-%d")
#     notes = request.form.get('notes', 'Predicted via ML')
#
#     # Geocode location
#     geolocator = Nominatim(user_agent="pakshi-geo")
#     loc = geolocator.geocode(location)
#     if not loc:
#         return "❌ Location could not be geocoded. Try again.", 400
#
#     report = {
#         "English Name": bird_name,
#         "Location": location,
#         "Date": date,
#         "Notes": notes,
#         "latitude": loc.latitude,
#         "longitude": loc.longitude
#     }
#
#     df_new = pd.DataFrame([report])
#     path = "user_reports.csv"
#     if os.path.exists(path):
#         df_new.to_csv(path, mode='a', header=False, index=False)
#     else:
#         df_new.to_csv(path, index=False)
#
#     return redirect("/bird-map")
#
#
#
# @app.route('/upload/image', methods=['POST'])
# def predict_image_route():
#     if 'image_file' in request.files and request.files['image_file'].filename != '':
#         image = request.files['image_file']
#         filename = secure_filename(image.filename)
#         path = os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename)
#         image.save(path)
#
#         top_birds = predict_bird_from_image(path)  # should return list of tuples: [(label, prob), ...]
#         top_prediction = top_birds[0][0]
#
#         info = get_bird_info(top_prediction)
#         image_url = get_bird_image_url(top_prediction)
#
#         session['result'] = {
#             'top_birds': top_birds,
#             'top_prediction': top_prediction,
#             'info': info,
#             'file_url': url_for('static', filename='uploads/' + filename),
#             'image_url': image_url,
#             'is_image': True
#         }
#
#         return redirect(url_for('result'))
#     return redirect(url_for('index'))
#
# @app.route('/upload/audio', methods=['POST'])
# def predict_audio_route():
#     if 'audio_file' in request.files and request.files['audio_file'].filename != '':
#         audio = request.files['audio_file']
#         filename = secure_filename(audio.filename)
#         path = os.path.join(app.config['UPLOAD_FOLDER_AUDIO'], filename)
#         audio.save(path)
#
#         top_birds = predict_bird_from_audio(path)  # same as above
#         top_prediction = top_birds[0][0]
#
#         info = get_bird_info(top_prediction)
#         image_url = get_bird_image_url(top_prediction)
#
#         session['result'] = {
#             'top_birds': top_birds,
#             'top_prediction': top_prediction,
#             'info': info,
#             'file_url': url_for('static', filename='wav_uploads/' + filename),
#             'image_url': image_url,
#             'is_image': False
#         }
#
#         return redirect(url_for('result'))
#     return redirect(url_for('audio_page'))
#
# @app.route('/result')
# def result():
#     result_data = session.get('result', {})
#     return render_template(
#         'result.html',
#         top_birds=result_data.get('top_birds', []),
#         top_prediction=result_data.get('top_prediction'),
#         info=result_data.get('info'),
#         file_url=result_data.get('file_url'),
#         image_url=result_data.get('image_url'),
#         is_image=result_data.get('is_image', True)
#     )
#
# def get_bird_info(bird_name):
#     try:
#         summary = wikipedia.summary(bird_name, sentences=3, auto_suggest=True, redirect=True)
#         return summary
#     except Exception as e:
#         print(f"❌ Wikipedia fetch error: {e}")
#         return "No additional info available."
#
#
#
# if __name__ == "__main__":
#     app.run(debug=True)






import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.image_preprocess import predict_bird_from_image
from utils.audio_preprocess import predict_bird_from_audio
from google_search import get_bird_image_url
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime
import requests  # NEW for Wikipedia REST API

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Upload folders
UPLOAD_FOLDER_IMG = 'static/uploads'
UPLOAD_FOLDER_AUDIO = 'static/wav_uploads'

app.config['UPLOAD_FOLDER_IMG'] = UPLOAD_FOLDER_IMG
app.config['UPLOAD_FOLDER_AUDIO'] = UPLOAD_FOLDER_AUDIO

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER_IMG, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_AUDIO, exist_ok=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio_page')
def audio_page():
    return render_template('audio_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/bird_attributes')
def bird_attributes():
    return render_template('bird_attributes.html')

@app.route("/bird-map")
def bird_map_page():
    return render_template("bird_map.html")

@app.route("/api/bird-map-data")
def bird_map_data():
    base_df = pd.read_csv("geocoded_metadata.csv")

    if os.path.exists("user_reports.csv"):
        user_df = pd.read_csv("user_reports.csv")
        combined = pd.concat([base_df, user_df], ignore_index=True)
    else:
        combined = base_df

    data = combined[["English Name", "Location", "Date", "latitude", "longitude"]].dropna().to_dict(orient="records")
    return jsonify(data)

@app.route('/report_sighting', methods=['POST'])
def report_sighting():
    bird_name = request.form['bird_name']
    location = request.form['location']
    date = request.form['date']
    notes = request.form.get('notes', '')

    geolocator = Nominatim(user_agent="pakshi-bird-reporter")
    loc = geolocator.geocode(location)
    if not loc:
        return "❌ Location could not be geocoded. Please try again with a valid location.", 400

    new_row = {
        "English Name": bird_name,
        "Location": location,
        "Date": date,
        "Notes": notes,
        "latitude": loc.latitude,
        "longitude": loc.longitude
    }

    report_path = "user_reports.csv"
    df_new = pd.DataFrame([new_row])
    if os.path.exists(report_path):
        df_new.to_csv(report_path, mode='a', header=False, index=False)
    else:
        df_new.to_csv(report_path, index=False)

    return redirect("/bird-map")

@app.route('/report_from_prediction', methods=['POST'])
def report_from_prediction():
    bird_name = request.form['bird_name']
    location = request.form['location']
    date = request.form.get('date') or datetime.now().strftime("%Y-%m-%d")
    notes = request.form.get('notes', 'Predicted via ML')

    geolocator = Nominatim(user_agent="pakshi-geo")
    loc = geolocator.geocode(location)
    if not loc:
        return "❌ Location could not be geocoded. Try again.", 400

    report = {
        "English Name": bird_name,
        "Location": location,
        "Date": date,
        "Notes": notes,
        "latitude": loc.latitude,
        "longitude": loc.longitude
    }

    df_new = pd.DataFrame([report])
    path = "user_reports.csv"
    if os.path.exists(path):
        df_new.to_csv(path, mode='a', header=False, index=False)
    else:
        df_new.to_csv(path, index=False)

    return redirect("/bird-map")

@app.route('/upload/image', methods=['POST'])
def predict_image_route():
    if 'image_file' in request.files and request.files['image_file'].filename != '':
        image = request.files['image_file']
        filename = secure_filename(image.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename)
        image.save(path)

        top_birds = predict_bird_from_image(path)
        top_prediction = top_birds[0][0]

        info, wiki_image_url, wiki_page_url = get_bird_info(top_prediction)
        google_image_url = get_bird_image_url(top_prediction)

        session['result'] = {
            'top_birds': top_birds,
            'top_prediction': top_prediction,
            'info': info,
            'file_url': url_for('static', filename='uploads/' + filename),
            'image_url': wiki_image_url or google_image_url,
            'wikipedia_url': wiki_page_url,
            'is_image': True
        }

        return redirect(url_for('result'))
    return redirect(url_for('index'))

@app.route('/upload/audio', methods=['POST'])
def predict_audio_route():
    if 'audio_file' in request.files and request.files['audio_file'].filename != '':
        audio = request.files['audio_file']
        filename = secure_filename(audio.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER_AUDIO'], filename)
        audio.save(path)

        top_birds = predict_bird_from_audio(path)
        top_prediction = top_birds[0][0]

        info, wiki_image_url, wiki_page_url = get_bird_info(top_prediction)
        google_image_url = get_bird_image_url(top_prediction)

        session['result'] = {
            'top_birds': top_birds,
            'top_prediction': top_prediction,
            'info': info,
            'file_url': url_for('static', filename='wav_uploads/' + filename),
            'image_url': wiki_image_url or google_image_url,
            'wikipedia_url': wiki_page_url,
            'is_image': False
        }

        return redirect(url_for('result'))
    return redirect(url_for('audio_page'))

@app.route('/result')
def result():
    result_data = session.get('result', {})
    return render_template(
        'result.html',
        top_birds=result_data.get('top_birds', []),
        top_prediction=result_data.get('top_prediction'),
        info=result_data.get('info'),
        file_url=result_data.get('file_url'),
        image_url=result_data.get('image_url'),
        wikipedia_url=result_data.get('wikipedia_url'),
        is_image=result_data.get('is_image', True)
    )

# Wikipedia REST API based info fetcher
# def get_bird_info(bird_name):
#     try:
#         bird_title = bird_name.split('.')[-1].replace('_', ' ')
#         api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{bird_title.replace(' ', '_')}"
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             summary = data.get("extract", "No summary available.")
#             image_url = data.get("thumbnail", {}).get("source", None)
#             wikipedia_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{bird_title.replace(' ', '_')}")
#             return summary, image_url, wikipedia_url
#         else:
#             print(f"❌ Wikipedia API error {response.status_code}")
#             return "No additional info available.", None, f"https://en.wikipedia.org/wiki/{bird_title.replace(' ', '_')}"
#     except Exception as e:
#         print(f"❌ Wikipedia fetch error: {e}")
#         return "No additional info available.", None, f"https://en.wikipedia.org/wiki/{bird_title.replace(' ', '_')}"

def get_bird_info(bird_name):
    try:
        bird_query = bird_name.split('.')[-1].replace('_', ' ')
        search_query = f"{bird_query} bird"

        # 1️⃣ Search API
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_query}&format=json"
        search_response = requests.get(search_url)
        if search_response.status_code == 200:
            search_data = search_response.json()
            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
                print("❌ No search results for bird.")
                return "No additional info available.", None, f"https://en.wikipedia.org/wiki/{bird_query.replace(' ', '_')}"

            best_title = search_results[0]['title']
            print(f"✅ Wikipedia best match: {best_title}")

            # 2️⃣ Get full extract
            extract_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&exsectionformat=plain&titles={best_title.replace(' ', '_')}&format=json"
            extract_response = requests.get(extract_url)
            if extract_response.status_code == 200:
                extract_data = extract_response.json()
                pages = extract_data.get("query", {}).get("pages", {})
                page = next(iter(pages.values()))
                extract = page.get("extract", "No additional info available.")
            else:
                extract = "No additional info available."

            # 3️⃣ Also get image and official URL
            summary_api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_title.replace(' ', '_')}"
            summary_response = requests.get(summary_api)
            if summary_response.status_code == 200:
                summary_data = summary_response.json()
                image_url = summary_data.get("thumbnail", {}).get("source", None)
                wikipedia_url = summary_data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{best_title.replace(' ', '_')}")
            else:
                image_url = None
                wikipedia_url = f"https://en.wikipedia.org/wiki/{best_title.replace(' ', '_')}"

            return extract, image_url, wikipedia_url
        else:
            print(f"❌ Wikipedia Search API error {search_response.status_code}")
            return "No additional info available.", None, f"https://en.wikipedia.org/wiki/{bird_query.replace(' ', '_')}"
    except Exception as e:
        print(f"❌ Wikipedia fetch error: {e}")
        return "No additional info available.", None, f"https://en.wikipedia.org/wiki/{bird_query.replace(' ', '_')}"


if __name__ == "__main__":
    app.run(debug=True)
