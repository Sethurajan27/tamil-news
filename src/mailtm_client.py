import requests

class MailTMClient:
    BASE_URL = "https://api.mail.tm"

    def __init__(self):
        self.domain = self.get_domain()
        self.account = self.create_account()
        self.token = self.get_token()

    def get_domain(self):
        response = requests.get(f"{self.BASE_URL}/domains")
        data = response.json()
        domain = data["hydra:member"][0]["domain"]
        print(f"📥 Domain response: {data}")
        return domain

    def create_account(self):
        from uuid import uuid4
        self.email = f"news_{uuid4().hex[:8]}@{self.domain}"
        self.password = "Password@123"

        response = requests.post(f"{self.BASE_URL}/accounts", json={
            "address": self.email,
            "password": self.password
        })
        print(f"📤 Account creation response: {response.status_code} {response.text}")
        return {
            "email": self.email,
            "password": self.password,
            "id": response.json()["id"]
        }

    def get_token(self):
        response = requests.post(f"{self.BASE_URL}/token", json={
            "address": self.account["email"],
            "password": self.account["password"]
        })
        data = response.json()
        print(f"🔐 Token response: {response.status_code} {response.text}")
        return data["token"]

    def get_messages(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/messages", headers=headers)
        return response.json()

    def wait_for_email(self, subject_keyword, timeout=60):
        import time
        start = time.time()
        while time.time() - start < timeout:
            messages = self.get_messages()
            for msg in messages.get("hydra:member", []):
                if subject_keyword in msg["subject"]:
                    return msg
            time.sleep(5)
        raise TimeoutError(f"Timeout waiting for email with subject '{subject_keyword}'")