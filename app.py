import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# ------------------ Streamlit UI ------------------
st.title("🔍 Instagram Username Extractor (No API)")
st.markdown("This app searches Instagram and extracts public usernames from posts under a given hashtag.")

# User inputs
search_term = st.text_input("Enter Hashtag (e.g., MassageDelhi)")
search_button = st.button("Search Instagram")

if search_button and search_term:
    with st.spinner("Searching Instagram..."):
        try:
            # ------------------ Automate Instagram Search ------------------
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run in background
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            driver = webdriver.Chrome(options=options)  # Ensure you have the Chrome WebDriver installed
            driver.get("https://www.instagram.com/explore/tags/" + search_term)
            time.sleep(5)  # Wait for page to load

            # Extract usernames from the first few posts
            usernames = []
            posts = driver.find_elements("xpath", "//a[contains(@href, '/p/')]")
            for post in posts[:10]:  # Get usernames from first 10 posts
                post.click()
                time.sleep(3)
                try:
                    username = driver.find_element("xpath", "//header//a").text
                    if username and username not in usernames:
                        usernames.append(username)
                except:
                    pass
                driver.back()
                time.sleep(2)

            driver.quit()

            # ------------------ Display Results ------------------
            if usernames:
                df = pd.DataFrame(usernames, columns=["Instagram Username"])
                st.write("### 📊 Extracted Usernames")
                st.dataframe(df)
                st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name="instagram_usernames.csv", mime="text/csv")
            else:
                st.error("No usernames found. Try another hashtag.")

        except Exception as e:
            st.error(f"Error: {e}")
