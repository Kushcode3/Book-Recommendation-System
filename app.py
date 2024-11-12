import streamlit as st
import pickle
import numpy as np
import pandas as pd


popular_books_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books_with_ratings = pickle.load(open('books_with_ratings.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


def Top_popular_books(n):
    top_n_books = popular_books_df.reset_index(drop=True).head(n)

    return top_n_books
    

def recommend(book_name):
    # index fetch
    if book_name in pt.index:
        index = np.where(pt.index == book_name)[0][0]

        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = books_with_ratings[books_with_ratings['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))

            data.append(item)

        return data

    else:
        return None
        
# Streamlit UI components
st.title("Book Recommender")

# Text input for book name
book_name = st.text_area("Enter book name")

if st.button('Recommend'):
    if book_name:
        # Get recommendations based on input book name
        result = recommend(book_name)

        if result:
            # Convert result to DataFrame for proper table display
            result_df = pd.DataFrame(result, columns=["Book Title", "Book Author"])
            st.table(result_df)
        else:
            st.error('Book not found in our database.')
    else:
        st.warning('Please enter a book name to get recommendations.')

# Display Top 5 popular books
if st.button('Top Books'):
    top_books = Top_popular_books(5)
    st.table(top_books)
