from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

app = Flask(__name__)

# -------------------------------
# User Agents Pool
# -------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36"
]

# -------------------------------
# Job Extractor (now returns full HTML)
# -------------------------------
def extract_job_html(url):
    if not isinstance(url, str) or not url.strip():
        return {"error": "Invalid URL provided", "Job Link": url}

    # Selenium options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--incognito")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Pick a random User-Agent
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    job_data = {"Job Link": url, "User-Agent": user_agent}

    try:
        driver.get(url)

        # Random delay per URL (between 2 and 6 seconds)
        sleep_time = random.randint(2, 6)
        time.sleep(sleep_time)

        # Get full page source (HTML)
        page_html = driver.page_source
        job_data["HTML"] = page_html
        job_data["DelayUsed"] = sleep_time

    except Exception as e:
        job_data["error"] = str(e)

    finally:
        driver.quit()

    return job_data


# -------------------------------
# Flask Route
# -------------------------------
@app.route("/fetch-jobs", methods=["POST"])
def fetch_jobs():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request body"}), 400

    results = []
    if isinstance(data, list):
        for item in data:
            job_link = None
            if isinstance(item, dict):
                job_link = item.get("Job Link")
            elif isinstance(item, str):
                job_link = item

            if job_link:
                results.append(extract_job_html(job_link))
            else:
                results.append({"Job Link": None, "error": "Invalid item in request"})
    else:
        return jsonify({"error": "Invalid input. Must be a list of job links or objects."}), 400

    return jsonify(results)


if __name__ == "__main__":
    app.run(port=3001, debug=True)
