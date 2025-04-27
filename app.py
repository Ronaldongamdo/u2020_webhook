from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

@app.route("/nur_u2020", methods=["POST"])
def download_nur():
    data = request.get_json()
    report_date = data.get("date")

    if not report_date:
        return jsonify({"error": "Date manquante"}), 400

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # facultatif
        prefs = {"download.default_directory": "/tmp"}  # modifie si besoin
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)
        driver.get("https://172.26.130.32:31943/unisso/login.action")

        driver.find_element(By.NAME, "username").send_keys("fsbz6851")
        driver.find_element(By.NAME, "password").send_keys("Huawei1+11")
        driver.find_element(By.NAME, "login").click()
        time.sleep(3)

        driver.find_element(By.LINK_TEXT, "Report Management").click()
        time.sleep(2)

        search_input = driver.find_element(By.NAME, "search")
        search_input.send_keys(f"NUR {report_date}")
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        driver.find_element(By.PARTIAL_LINK_TEXT, report_date).click()
        time.sleep(10)

        driver.quit()

        return jsonify({"status": "Téléchargement terminé"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
