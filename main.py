import pandas as pd
import time
import streamlit as st
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%Y%m%d%H%M%S")
startTime = time.time()

def get_data(file_name):
    df = pd.read_excel(file_name,'ET_PROMAT')

    df_in = df.loc[df['OUTIN'] > 0]
    df_in = df_in[['PROID', 'MATID']]
    df_out = df.loc[df['OUTIN'] <= 0]
    df_out = df_out[['PROID', 'MATID']]

    result = df_out.merge(df_in, on='PROID', how='left')
    result = result.rename(columns={'MATID_x': 'input', 'MATID_y': 'output'})
    result = result[['input', 'PROID','output']]

    return result

file_name = st.file_uploader('Upload the file xlsx')
if st.button('Start Process'):
    resultList = get_data(file_name)



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
        file_name=f'output_{current_time}.csv',
        mime='text/csv',
    )


    st.text(f"Execution time: { ( time.time() - startTime ) :.2f} sec")
