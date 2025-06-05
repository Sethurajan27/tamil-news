from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.mailtm_client import MailTMClient
import time
import re
import tempfile
import os

def init_driver(headless=True):
    options = Options()

    # ✅ Always enable headless mode for CI (GitHub Actions)
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Use a unique temporary user data directory
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # ✅ Avoid using extensions and background network calls
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    return driver

def openai_signup(driver, mail_client):
    print("🔐 Signing up for OpenAI...")
    email = mail_client.account['email']
    password = mail_client.account['password']
    print(driver.current_url)
    print(driver.page_source)
    driver.save_screenshot("screenshot.png")
    driver.get('https://auth.openai.com/signup')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(email)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()

    print("Waiting for verification email...")
    email_text = mail_client.wait_for_email("Verify your email")
    
    match = re.search(r'https://auth\\.openai\\.com[^\\s]+', email_text)
    if match:
        verification_link = match.group(0)
        driver.get(verification_link)
        print("Verification complete.")
    else:
        raise Exception("Verification link not found in email.")