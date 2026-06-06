import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    url = "https://www.dropbox.com/scl/fi/s0e5f5mj6mxgqh6jkjqdg/Deklaracija.parquet?rlkey=rdkx6gnzbddag6psam7g34l2n&st=oxs84wsk&raw=1"
    df = pd.read_parquet(url)
    df = df[df['suma'] > 0].copy()
    df.drop(columns=['_type', '_id', '_revision', '_page.next', 'eiles_nr'], inplace=True)
    df_clean = df.dropna(subset=['suma'])
    return df_clean
