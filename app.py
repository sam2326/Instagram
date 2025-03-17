import streamlit as st
import openai

# ✅ Replace this with your new, secure API key
OPENAI_API_KEY = "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"

# ✅ Set API key for OpenAI
openai.api_key = OPENAI_API_KEY

st.title("🔍 ChatGPT-Powered Massage Services Tracker in Delhi & Gurgaon")

st.header("📊 AI-Powered Search Trend Analysis")

# User input for search trends
user_query = st.text_input("Enter a search query related to massage services:")

if st.button("Analyze Search Trends"):
    if user_query:
        with st.spinner("Fetching insights..."):
            try:
                # OpenAI API Call
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert in analyzing search trends."},
                        {"role": "user", "content": f"Find out how many people are searching for '{user_query}' in Delhi and Gurgaon and suggest business strategies."}
                    ]
                )
                
                result = response["choices"][0]["message"]["content"]
                st.write("📌 **AI Insights:**")
                st.write(result)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter a search query.")

st.sidebar.header("ℹ️ How to Use")
st.sidebar.write("""
1. **View AI Search Insights** for massage services in Delhi & Gurgaon.
2. **Get Business Strategy Recommendations**.
3. **Use Secure API Key Management** for deployment.
""")

st.sidebar.success("✅ Ready to Deploy on Streamlit Cloud!")
