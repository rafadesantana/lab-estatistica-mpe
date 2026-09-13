import pandas as pd
import streamlit as st

df = pd.read_csv("data/varejo_brasileiro.csv")

st.title("Laboratório de Estatística — Varejo Brasileiro")
st.write(df)