import time
from google import genai

client = genai.Client(api_key="AQ.Ab8RN6L-QtYVJl3dsBrMmYP8IX_cWa4n_HlYhQCdf9-dvjE7u")

print("⏳ Sitting tight for 35 seconds to let Google's cool-down timer clear...")
time.sleep(35)

print("🚀 Retrying the endpoint now...")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hello"
    )
    print("\n🎉 SUCCESS! Response from Gemini:")
    print(response.text)
except Exception as e:
    print("\n❌ Error:")
    print(e)