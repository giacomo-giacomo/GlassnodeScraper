from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pandas as pd
import re

# Credentials
USERNAME = ""
PASSWORD = ""

# Setup headless Chrome browser
options = Options()
#options.add_argument("--headless=new")
#options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114 Safari/537.36")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://studio.glassnode.com/home")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy='login-btn']"))
    )
    login_button.click()
    time.sleep(5)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='email-password-fragment-email-input']"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='email-password-fragment-password-input']"))
    )

    email_input.send_keys(USERNAME)
    time.sleep(5)
    password_input.send_keys(PASSWORD)
    time.sleep(5)

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
    )
    submit_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Dashboard')]"))
    )
    print("Login successful.")
    time.sleep(5)

    # Extract cookies after login
    cookies = driver.get_cookies()
    cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

    time.sleep(5)

    target_urls = [
        "https://api.glassnode.com/v1/metrics/addresses/active_count?a=POL&i=24h&referrer=charts",
        "https://api.glassnode.com/v1/metrics/addresses/count?a=POL&i=24h&referrer=charts"
    ]
    for url in target_urls:

        # Send authenticated request using session cookies
        headers = {
            "Cookie": cookie_string,
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        print(response)
        data = response.json()
        time.sleep(3)

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df.columns = ['timestamp', 'value']
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

        # Save to CSV
        metric_name = re.sub(r'[^a-zA-Z0-9_]', '_', url.split("/metrics/")[-1])
        df.to_csv(f"{metric_name}.csv", index=False)
        time.sleep(3)

except Exception as e:
    print(f"Error during login or data fetch: {e}")

finally:
    driver.quit()
