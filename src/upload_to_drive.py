import requests
import base64
import os
from src.delete_accounts import delete_openai_account, delete_elevenlabs_account

def upload_to_drive_via_webapp(file_path, web_app_url, file_name=None, folder_id=None, driver=None, email=None, password=None):
    with open(file_path, 'rb') as f:
        file_data = base64.b64encode(f.read()).decode('utf-8')

    if file_name is None:
        file_name = os.path.basename(file_path)

    payload = {
        'fileName': file_name,
        'fileData': file_data
    }

    if folder_id:
        payload['folderId'] = folder_id

    response = requests.post(web_app_url, data=payload)
    result = response.json()

    if result.get("success"):
        print("✅ Upload successful. Initiating account deletion...")
        if driver and email and password:
            delete_openai_account(driver, email, password)
            delete_elevenlabs_account(driver)
    else:
        print("❌ Upload failed:", result.get("error"))

    return result
