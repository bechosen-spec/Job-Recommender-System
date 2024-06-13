import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the TF-IDF vectorizer and cosine similarity matrix
tdif = joblib.load('/path/to/tfidf_vectorizer.pkl')
cosine_sim = joblib.load('/path/to/cosine_similarity.pkl')

# Load the job dataset (assuming you have the 'dice_com-job_us_sample.csv' file)
df1 = pd.read_csv('/content/gdrive/MyDrive/job dataset/dice_com-job_us_sample.csv')
df1 = df1.dropna()
indices = pd.Series(df1.index, index=df1['jobtitle']).drop_duplicates()

# Define the job recommendation function
def get_recommendation(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key= lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:16]
    tech_indices = [i[0] for i in sim_scores]
    return df1['jobtitle'].iloc[tech_indices]

# Create the Streamlit app
def main():
    st.title('Job Recommender System')

    job_title = st.text_input('Enter a job title:', 'Lead DevOps Engineer')

    if st.button('Get Job Recommendations'):
        recommendations = get_recommendation(job_title)
        st.subheader('Recommended Jobs:')
        for job in recommendations:
            st.write(job)

if __name__ == '__main__':
    main()
