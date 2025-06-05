from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.mailtm_client import MailTMClient
import time
import re

def init_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def openai_signup(driver, mail_client):
    email = mail_client.account['email']
    password = mail_client.account['password']

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