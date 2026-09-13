import pandas as pd

df = pd.read_csv("data/varejo_brasileiro.csv")

print("formato (linhas, colunas):", df.shape)
print("colunas:", df.columns.tolist())
print(df.head())
print(df.dtypes)

