import google.generativeai as genai

# 1. Your authenticated key string
API_KEY = "AQ.Ab8RN6J6uk3nB6AUToUbIPB57UAIMAFkzDTnQTGwQ6PmlTBPg"
genai.configure(api_key=API_KEY)

# 2. Pointing to the flash model
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Your prompt logic
test_prompt = "Give me a quick 3-step blueprint for auto-saving customer emails into an Excel sheet."

print("🚀 Connecting to the new DoDo engine pipeline...")

try:
    response = model.generate_content(test_prompt)
    print("\n✨ DoDo Engine Live Response:")
    print(response.text)
except Exception as e:
    print(f"\n❌ Execution stopped: {e}")