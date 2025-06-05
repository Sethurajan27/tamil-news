from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def delete_openai_account(driver, email, password):
    driver.get('https://platform.openai.com/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Log in')]").click()
    time.sleep(5)
    driver.get("https://platform.openai.com/account/settings")
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[contains(text(),'Delete account')]").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[contains(text(),'Delete')]").click()
    print("OpenAI account deletion triggered.")

def delete_elevenlabs_account(driver):
    driver.get('https://www.elevenlabs.io/account')
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[contains(text(),'Delete Account')]").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[contains(text(),'Confirm')]").click()
    print("ElevenLabs account deletion triggered.")