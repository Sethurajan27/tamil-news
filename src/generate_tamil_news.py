from src.prompts import get_prompt
import openai

def generate_news(api_key, time_slot):
    openai.api_key = api_key
    prompt = get_prompt(time_slot)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content