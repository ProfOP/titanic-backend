import google.generativeai as genai
import os

# ---------------------------------------------------------
# OPTION 1: Set key directly (Quickest for testing)
# Replace with your actual key
API_KEY = "AIzaSyCf8MmWTqC3KoMv6IivDxUaQM_mTQGfzf0"
# ---------------------------------------------------------

# OPTION 2: Use Environment Variable (Better for security)
# API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: API Key is missing.")
else:
    try:
        genai.configure(api_key=API_KEY)

        print("Fetching available models...\n")
        print(f"{'Model Name':<40} | {'Supported Generation Methods'}")
        print("-" * 80)

        for m in genai.list_models():
            # Most users only care about models that generate content (chat/text)
            # as opposed to embedding models.
            methods = ", ".join(m.supported_generation_methods)
            print(f"{m.name:<40} | {methods}")

    except Exception as e:
        print(f"Error fetching models: {e}")