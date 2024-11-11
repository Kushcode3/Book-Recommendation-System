import streamlit as st
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl','rb'))
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
        print('Book not found')
        
st.title("Book Recommender")
input = st.text_area("Enter book name")

if st.button('Recommend'):

    # Predict
    result = recommend(book_name)
    # Display
    print(result)
