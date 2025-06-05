import requests

def text_to_speech(api_key, text, voice_id="TxGEqnHWrfWFTfGW9XjX", output_path="output.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.6,
            "style": 0.35,
            "use_speaker_boost": True
        }
    }
    response = requests.post(url, headers=headers, json=data)
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path