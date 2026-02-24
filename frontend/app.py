import streamlit as st
import requests
import base64

st.set_page_config(page_title="Titanic Chat Agent", page_icon="🚢")

st.title("🚢 Titanic Dataset Chat Agent")
st.write("Ask questions about Titanic passengers and get insights with visualizations.")

# 🔹 IMPORTANT: Use your Render backend URL
BACKEND_URL = "https://titanic-backend-kyt5.onrender.com"

user_input = st.text_input("Enter your question:")

if st.button("Ask"):

    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing Titanic dataset..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"question": user_input}
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.subheader("Answer:")
                    st.write(data["response"])

                    if data.get("plot"):
                        image_bytes = base64.b64decode(data["plot"])
                        st.image(image_bytes)

            except Exception as e:
                st.error(f"Backend connection failed: {e}")