from flask import Flask, Response
from flask_cors import CORS
from playwright.sync_api import sync_playwright
import os
import json
import time

def load_currency_data():
    url = "https://www.conectate.com.do/articulo/precio-del-dolar-euro-rd-tasa-de-hoy/"
    result = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)

            # Espera inicial
            page.wait_for_selector("table.widget_currency_table", timeout=30000)

            # Esperar hasta que ambas tablas estén disponibles (máximo 10s)
            max_wait = 10
            waited = 0
            tables = page.query_selector_all("table.widget_currency_table")
            while len(tables) < 2 and waited < max_wait:
                print(f"[DEBUG] Solo {len(tables)} tabla(s) encontradas. Esperando más...")
                time.sleep(1)
                waited += 1
                tables = page.query_selector_all("table.widget_currency_table")

            print(f"[DEBUG] Se encontraron {len(tables)} tabla(s)")

            for table in tables:
                tds = table.query_selector_all("td.text-center")
                if len(tds) >= 4:
                    block = {
                        "moneda": tds[0].inner_text().strip(),
                        "ayer": tds[1].inner_text().strip(),
                        "hoy": tds[2].inner_text().strip(),
                        "diff": tds[3].inner_text().strip()
                    }
                    result.append(block)

            browser.close()

    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")

    return result

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

app.run(host='0.0.0.0', port=port)
