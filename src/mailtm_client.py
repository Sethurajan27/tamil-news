import os
import time
import string
import random
import requests
import urllib3

# Disable HTTPS warnings (you may remove in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MailTMClient:
    BASE_URL = "https://api.mail.tm"

    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.address = None
        self.password = None
        self.create_account()

    def create_account(self):
        # Step 1: Get domain
        domain_resp = self.session.get(f"{self.BASE_URL}/domains", verify=False)
        domain_data = domain_resp.json()
        print("📥 Domain response:", domain_data)

        domain = domain_data['hydra:member'][0]['domain']

        # Step 2: Generate email and password
        self.address = f"news_{os.urandom(4).hex()}@{domain}"
        self.password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # Step 3: Create account
        acc_data = {"address": self.address, "password": self.password}
        acc_resp = self.session.post(f"{self.BASE_URL}/accounts", json=acc_data, verify=False)
        print("📤 Account creation response:", acc_resp.status_code, acc_resp.text)

        if acc_resp.status_code != 201:
            raise Exception(f"❌ Account creation failed: {acc_resp.text}")

        # Step 4: Get token
        token_resp = self.session.post(f"{self.BASE_URL}/token", json=acc_data, verify=False)
        print("🔐 Token response:", token_resp.status_code, token_resp.text)

        if token_resp.status_code != 200:
            raise Exception(f"❌ Token fetch failed: {token_resp.text}")

        self.token = token_resp.json()["token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        print(f"✅ Account ready: {self.address}")

    def wait_for_email(self, subject_filter, timeout=300):
        start = time.time()
        while time.time() - start < timeout:
            inbox_resp = self.session.get(f"{self.BASE_URL}/messages", verify=False)
            inbox = inbox_resp.json()
            print("📬 Inbox check:", inbox)

            for msg in inbox.get('hydra:member', []):
                if subject_filter in msg['subject']:
                    msg_id = msg['id']
                    message = self.session.get(f"{self.BASE_URL}/messages/{msg_id}", verify=False).json()
                    print("📧 Email received:", message['subject'])
                    return message['text']

            time.sleep(5)
        raise TimeoutError("⏰ Email not received in time.")