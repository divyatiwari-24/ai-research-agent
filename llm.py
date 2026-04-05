from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Global variable
last_call_time = 0

def call_llm(prompt):
    global last_call_time
    import time

    # ⏳ Rate limit protection (cooldown)
    if time.time() - last_call_time < 20:
        wait_time = 20 - (time.time() - last_call_time)
        print(f"⏳ Waiting {int(wait_time)}s to avoid rate limit...")
        time.sleep(wait_time)

    for attempt in range(3):  # retry max 3 times
        try:
            response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=prompt
            )

            last_call_time = time.time()
            return response.candidates[0].content.parts[0].text

        except Exception as e:
            error_str = str(e)

            # 🔴 Handle 429 (rate limit)
            if "429" in error_str:
                wait = (attempt + 1) * 20
                print(f"⚠️ Rate limited. Waiting {wait}s...")
                time.sleep(wait)

            # 🔴 Handle 503 (server busy)
            elif "503" in error_str:
                wait = (attempt + 1) * 10
                print(f"🚦 Server busy. Retrying in {wait}s...")
                time.sleep(wait)

            else:
                print("❌ ERROR:", e)
                return "API error. Try again."

    return "⚠️ Server overloaded. Please try after some time."