import streamlit as st
import requests
import pandas as pd

# ------------------ Web Scraping API Configuration ------------------
SCRAPER_API_KEY = "541a9d4121e17f3aa740e31181e289ec"  # Your ScraperAPI Key

# Function to fetch Instagram usernames from a hashtag page
def fetch_instagram_usernames(hashtag):
    url = f"https://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url=https://www.instagram.com/explore/tags/{hashtag}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.text
        usernames = list(set([x.split('href="/')[1].split('/')[0] for x in data.split() if 'href="/' in x and "/p/" not in x]))
        return usernames
    return []

# ------------------ Streamlit UI ------------------
st.title("🔍 Instagram Username Extractor (No API Required)")
st.markdown("This app extracts **public usernames** from Instagram posts under a hashtag using ScraperAPI.")

# User input
hashtag = st.text_input("Enter Hashtag (e.g., MassageDelhi)")
search_button = st.button("Search Instagram")

if search_button and hashtag:
    with st.spinner("Searching Instagram..."):
        usernames = fetch_instagram_usernames(hashtag)
        
        if usernames:
            df = pd.DataFrame(usernames, columns=["Instagram Username"])
            st.write("### 📊 Extracted Usernames")
            st.dataframe(df)
            st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name="instagram_usernames.csv", mime="text/csv")
        else:
            st.error("No usernames found. Try another hashtag.")
