from google_play_scraper import reviews, Sort
import pandas as pd
import time

apps = {
    "Swiggy": "com.swiggy.android",
    "Zomato": "com.application.zomato",
    "Flipkart": "com.flipkart.android",
    "PhonePe": "com.phonepe.app",
    "Amazon": "in.amazon.mShop.android.shopping"
}

all_reviews = []


for app_name, app_id in apps.items():

    print(f"\nScraping reviews for {app_name}...")

    try:
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='in',
            sort=Sort.NEWEST,
            count=1000
        )

        for review in result:

            # Keep only important fields
            all_reviews.append({
                "app_name": app_name,
                "review": review['content'],
                "rating": review['score'],
                "review_date": review['at'],
                "likes": review['thumbsUpCount']
            })

        print(f"Collected {len(result)} reviews from {app_name}")

        # Avoid hitting rate limits
        time.sleep(2)

    except Exception as e:
        print(f"Error scraping {app_name}: {e}")


df = pd.DataFrame(all_reviews)

df = df[df['review'].notnull()]
df = df[df['rating'] <= 3]
def get_sentiment(rating):

    if rating <= 2:
        return "Negative"

    elif rating == 3:
        return "Neutral"

    else:
        return "Positive"

df['sentiment'] = df['rating'].apply(get_sentiment)

def escalation_flag(review):

    keywords = [
        "refund",
        "worst",
        "fraud",
        "not working",
        "scam",
        "angry",
        "delay",
        "late",
        "bad service",
        "cancelled"
    ]

    review = str(review).lower()

    for word in keywords:
        if word in review:
            return "High"

    return "Low"

df['escalation_risk'] = df['review'].apply(escalation_flag)

def categorize_complaint(review):

    review = str(review).lower()

    if "refund" in review:
        return "Refund Issue"

    elif "delivery" in review:
        return "Delivery Issue"

    elif "payment" in review:
        return "Payment Failure"

    elif "account" in review:
        return "Account Issue"

    elif "crash" in review or "bug" in review:
        return "Technical Issue"

    else:
        return "General Complaint"

df['category'] = df['review'].apply(categorize_complaint)
df.drop_duplicates(subset=['review'], inplace=True)
df.to_csv("customer_complaints_dataset.csv", index=False)
print("\nDataset Created Successfully!")
print(f"Total Complaints Collected: {len(df)}")

print("\nSample Data:\n")
print(df.head())
high_risk = df[df['escalation_risk'] == "High"]

high_risk.to_csv("high_risk_complaints.csv", index=False)

print("\nHigh escalation complaint dataset also saved.")

import pandas as pd
import re

df = pd.read_csv("customer_complaints_dataset.csv")

print("Original Shape:", df.shape)

df.dropna(inplace=True)
df.drop_duplicates(subset=['review'], inplace=True)

def clean_text(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http\\S+', '', text)

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\\s+', ' ', text).strip()

    return text
df['review'] = df['review'].apply(clean_text)

df = df[df['review'].str.len() > 15]

bad_words = [
    'good',
    'nice',
    'ok',
    'awesome',
    'bad',
    'worst',
    'excellent',
    'super'
]

df = df[~df['review'].isin(bad_words)]

# ============================================
# REMOVE EMPTY REVIEWS AFTER CLEANING
# ============================================

df = df[df['review'].str.strip() != '']

df['category'] = df['category'].replace({
    'General Complaint': 'General Issue',
    'Delivery Issue': 'Delivery Problem',
    'Refund Issue': 'Refund Problem'
})

df['review_date'] = pd.to_datetime(
    df['review_date'],
    errors='coerce'
)
f.dropna(subset=['review_date'], inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv("cleaned_complaints_dataset.csv", index=False)

high_risk = df[df['escalation_risk'] == 'High']

high_risk.to_csv(
    "cleaned_high_risk_complaints.csv",
    index=False
)

print("\\nDataset Cleaned Successfully!")

print("\\nFinal Shape:", df.shape)

print("\\nColumns:")
print(df.columns)

print("\\nSample Cleaned Data:")
print(df.head())

print("\\nFiles Saved:")
print("1. cleaned_complaints_dataset.csv")
print("2. cleaned_high_risk_complaints.csv")
