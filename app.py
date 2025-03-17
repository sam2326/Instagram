import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import instaloader

# -------------------------------
# Google Trends Data Fetching
# -------------------------------
st.title("🔍 Live Search Trends & Instagram Engagement: Massage Services in Delhi & Gurgaon")

st.header("📊 Google Search Trends for Massage Services")

# Initialize Google Trends API
pytrends = TrendReq(hl='en-US', tz=330)

# Define search queries
search_keywords = ["Massage services near me", "Spa in Delhi", "Female massage therapist"]
pytrends.build_payload(search_keywords, geo='IN-DL,IN-HR', timeframe='now 7-d')

# Get trends data
trends_data = pytrends.interest_over_time().drop(columns=["isPartial"])

# Display Google Trends Data
st.line_chart(trends_data)
st.write("🔍 **Live search interest for massage services in Delhi & Gurgaon**")
st.dataframe(trends_data)

# -------------------------------
# Instagram Engagement Tracking
# -------------------------------
st.header("📸 Instagram Lead Tracker")

# Define hashtag
hashtag = "delhimassage"

# Load Instagram data
L = instaloader.Instaloader()
users = set()

try:
    posts = L.get_hashtag_posts(hashtag)
    for post in posts:
        users.add(post.owner_username)
        if len(users) >= 10:  # Limit results to avoid overloading
            break

    # Convert to DataFrame
    user_df = pd.DataFrame(list(users), columns=["Instagram Usernames"])

    # Display results
    st.write("🔍 **Potential Customers Engaging with Massage Hashtags:**")
    st.dataframe(user_df)

    # Save to CSV
    user_df.to_csv("potential_leads.csv", index=False)

except Exception as e:
    st.error(f"Error fetching Instagram data: {e}")

# -------------------------------
# Deployment Information
# -------------------------------
st.sidebar.header("ℹ️ How to Use")
st.sidebar.write("""
1. **View Google Search Trends** for massage services in Delhi & Gurgaon.
2. **Track Instagram Users** interacting with related hashtags.
3. **Download Lead Data** for outreach.
""")

st.sidebar.success("✅ Ready to Deploy on Streamlit Cloud!")
