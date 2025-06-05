from src.mailtm_client import MailTMClient
from src.openai_signup import openai_signup, init_driver
from src.elevenlabs_signup import elevenlabs_signup
from src.generate_tamil_news import generate_news
from src.tts_convert import text_to_speech
from src.upload_to_drive import upload_to_drive_via_webapp

def main():
    mail_client = MailTMClient()
    driver = init_driver()

    print("🔐 Signing up for OpenAI...")
    openai_signup(driver, mail_client)

    print("🔐 Signing up for ElevenLabs...")
    eleven_api_key = elevenlabs_signup(driver, mail_client)

    print("📰 Generating Tamil News...")
    news = generate_news(api_key=eleven_api_key, time_slot="மாலை")

    print("🎙️ Converting to Audio...")
    audio_path = text_to_speech(eleven_api_key, news)

    print("☁️ Uploading to Google Drive...")
    upload_to_drive_via_webapp(
        file_path=audio_path,
        web_app_url="https://script.google.com/macros/s/AKfycbyb8K_EQwA9iVnNEiRnYG6xID2WfT-dWYq6QJWa90p4ejU2Z9vlmSZDrHVn_aFEZW8/exec",
        file_name="news.mp3",
        folder_id="1zWdn50DVXpBWcuX62wP2UoR0M2WU6_jb",
        driver=driver,
        email=mail_client.account['email'],
        password=mail_client.account['password']
    )

    driver.quit()

if __name__ == "__main__":
    main()