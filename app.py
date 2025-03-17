import streamlit as st
import requests
import pandas as pd
import time

# ------------------ ScraperAPI Configuration ------------------
SCRAPER_API_KEY = "541a9d4121e17f3aa740e31181e289ec"  # Your ScraperAPI Key

# Function to fetch Instagram usernames from a hashtag page
def fetch_instagram_usernames(hashtag):
    url = f"https://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url=https://www.instagram.com/explore/tags/{hashtag}/&render=true&country_code=US"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.text

            # Extract usernames using Instagram's structure
            usernames = list(set([x.split('"username":"')[1].split('"')[0] for x in data.split() if '"username":"' in x]))

            # Remove Instagram official accounts if present
            usernames = [user for user in usernames if not user.startswith("instagram")]

            return usernames
        else:
            return []
    except Exception as e:
        return f"Error: {e}"

# ------------------ Streamlit UI ------------------
st.title("🔍 Instagram Username Extractor (No API Required)")
st.markdown("This app extracts **public usernames** from Instagram posts under a hashtag using ScraperAPI.")

# User input
hashtag = st.text_input("Enter Hashtag (e.g., massage)")
search_button = st.button("Search Instagram")

if search_button and hashtag:
    with st.spinner("Searching Instagram..."):
        usernames = fetch_instagram_usernames(hashtag)

        if isinstance(usernames, list) and len(usernames) > 0:
            df = pd.DataFrame(usernames, columns=["Instagram Username"])
            st.write("### 📊 Extracted Usernames")
            st.dataframe(df)
            st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name="instagram_usernames.csv", mime="text/csv")
        elif isinstance(usernames, str):
            st.error(usernames)  # Display error message if API request fails
        else:
            st.error("No usernames found. Try another hashtag.")
