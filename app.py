from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from langdetect import detect
from predict import predict_news

import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import random
import certifi

app = Flask(__name__)
app.secret_key = "fake_news_secret_key_123"

# ---------------- MongoDB (FIXED) ----------------
MONGO_URI = "mongodb+srv://macsonaaron10_db_user:FakeNews12345@cluster0.tsk4jbb.mongodb.net/fake_news_db?retryWrites=true&w=majority"

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )

    db = client["fake_news_db"]
    collection = db["articles"]
    users = db["users"]

    client.server_info()
    print("✅ MongoDB Connected Successfully")

except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    collection = None
    users = None


# ---------------- TRANSLATION ----------------
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text


# ---------------- BBC FETCH ----------------
def fetch_bbc_article():
    base_url = "https://www.bbc.com"
    url = "https://www.bbc.com/news"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "/news/" in href:
                if href.startswith("/"):
                    href = base_url + href
                if href not in links:
                    links.append(href)

        if not links:
            return "BBC news not found"

        article_url = random.choice(links)

        article_res = requests.get(article_url, headers=headers, timeout=10)
        article_soup = BeautifulSoup(article_res.text, "html.parser")

        paragraphs = article_soup.find_all("p")

        text = " ".join(
            p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 40
        )

        if len(text) < 200:
            return "BBC article too short"

        return text[:3000]

    except Exception as e:
        return "Error fetching BBC: " + str(e)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users is not None:
            user = users.find_one({"username": username, "password": password})
        else:
            user = None

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users is not None and users.find_one({"username": username}):
            return render_template("signup.html", error="User already exists")

        if users is not None:
            users.insert_one({"username": username, "password": password})

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    prediction = None
    confidence = None
    language = None

    if request.method == "POST":
        news_text = request.form["news"]

        try:
            language = detect(news_text)
        except:
            language = "unknown"

        news_text = translate_to_english(news_text)

        if len(news_text.split()) < 8:
            news_text += " news report official statement confirmed"

        result = predict_news(news_text)

        prediction = result["prediction"]
        confidence = result["confidence"]

        try:
            if collection is not None:
                collection.insert_one({
                    "title": news_text,
                    "prediction": prediction,
                    "confidence": confidence,
                    "language": language
                })
        except:
            pass

    # 🔥 FIX: dashboard crash protection
    try:
        if collection is not None:
            history = list(collection.find().sort("_id", -1).limit(20))
        else:
            history = []
    except ServerSelectionTimeoutError:
        history = []

    return render_template(
        "dashboard.html",
        prediction=prediction,
        confidence=confidence,
        language=language,
        history=history
    )


# ---------------- BBC ROUTE ----------------
@app.route("/bbc")
def bbc():

    if "user" not in session:
        return redirect(url_for("login"))

    news_text = fetch_bbc_article()

    try:
        language = detect(news_text)
    except:
        language = "unknown"

    news_text = translate_to_english(news_text)
    news_text += " BBC reports official confirmation"

    result = predict_news(news_text)

    try:
        if collection is not None:
            collection.insert_one({
                "title": news_text,
                "prediction": result["prediction"],
                "confidence": result["confidence"],
                "language": language
            })
    except:
        pass

    return redirect(url_for("dashboard"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)