import pandas as pd
import streamlit as st

df = pd.read_csv("data/dataset_empreendedorismo_df.csv")

st.title("Laboratório de Estatística — MPE-DF")
st.write(df)