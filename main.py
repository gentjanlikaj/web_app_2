from operator import index
import pandas as pd
import time
import streamlit as st
startTime = time.time()
import nltk
import nltk.data
nltk.download('punkt')


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def get_data (sentences_text , file):
    sentences =tokenizer.tokenize(sentences_text)
    df = pd.read_csv(file)

    products_list = df.values.tolist()

    resultList = []

    for p in products_list:
        keyword = p[0].lower()
        for sentence in sentences:
            if keyword in sentence.lower():
                ts = sentence
            else:
                ts = ''
        resultList.append({
            'Keyword' : keyword
            ,'Text Snippet': ts
            ,'Search Volume': p[2]
            ,'Current Position': p[6]
            ,'Destination URL': p[7]
        })
    return resultList


keywords = st.text_area('Add the article')
file_name = st.file_uploader('Upload upload websites ranking data (csv)')
if st.button('Start Process The Keyword'):
    resultList = get_data(keywords,file_name)



    outputDf = pd.DataFrame(resultList)


    st.dataframe(outputDf)
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False,).encode('utf-8')
    csv = convert_df(outputDf)


    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data_file.csv',
        mime='text/csv',
    )


    st.text(f"Execution time: { ( time.time() - startTime ) :.2f} sec")
