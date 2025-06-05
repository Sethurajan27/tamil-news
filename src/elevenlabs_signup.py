from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.mailtm_client import MailTMClient
import time
import re

def elevenlabs_signup(driver, mail_client):
    email = mail_client.account['email']
    password = mail_client.account['password']

    driver.get('https://www.elevenlabs.io/signup')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign Up')]").click()

    print("Waiting for ElevenLabs verification email...")
    email_text = mail_client.wait_for_email("Verify your email")
    
    match = re.search(r'https://[^\\s]*elevenlabs\\.io[^\\s]+', email_text)
    if match:
        verification_link = match.group(0)
        driver.get(verification_link)
        print("Email verified for ElevenLabs.")
    else:
        raise Exception("Verification link not found in email.")

    driver.get('https://www.elevenlabs.io/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()

    time.sleep(5)
    driver.get('https://www.elevenlabs.io/account')
    time.sleep(3)
    api_key_element = driver.find_element(By.XPATH, "//*[contains(text(),'API key')]/following-sibling::div")
    api_key = api_key_element.text
    print("Retrieved ElevenLabs API key:", api_key)
    return api_key