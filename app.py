from flask import Flask, Response
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import json

def load_currency_data():
    url = "https://www.conectate.com.do/articulo/precio-del-dolar-euro-rd-tasa-de-hoy/"

    # Configurar Chrome en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Iniciar WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"[DEBUG] Requesting URL: {url}")
        driver.get(url)

        # Obtener el HTML renderizado
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.find_all("table", class_="widget_currency_table")
        print(f"[DEBUG] Found {len(tables)} tables")

        result = []

        for table in tables:
            tds = table.find_all("td", class_="text-center")
            if len(tds) >= 4:
                block = {
                    "moneda": tds[0].text.strip(),
                    "ayer": tds[1].text.strip(),
                    "hoy": tds[2].text.strip(),
                    "diff": tds[3].text.strip()
                }
                result.append(block)

        return result

    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return []

    finally:
        driver.quit()

def JsonUFT8(data=None):
    json_string = json.dumps(data, ensure_ascii=False)
    return Response(json_string, content_type='application/json; charset=utf-8')

app = Flask(__name__)
CORS(app)
port = int(os.environ.get("PORT", 1717))

@app.route("/", methods=['GET'])
def monedas_scraping():
    data = load_currency_data()
    return JsonUFT8(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
