import google.generativeai as genai

# Paste your API key here
genai.configure(api_key="AQ.Ab8RN6IfsyiCCk3WZwh1YoqIIQJ8Emon7TAyv2ssvBO-pd-Ehw")

try:
    print("Knocking on Google's door...")
    # 1.5-flash is the correct current model, let's see if your key allows it
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say 'hello broski' if you can read this.")
    print("\nSUCCESS! Google says:")
    print(response.text)
except Exception as e:
    print("\nFAILED! The error is:")
    print(e)