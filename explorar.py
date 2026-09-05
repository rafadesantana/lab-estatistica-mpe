import pandas as pd

df = pd.read_csv("data/dataset_empreendedorismo_df.csv")

print("formato (linhas, colunas):", df.shape)
print("colunas:", df.columns.tolist())
print(df.head())
print(df.dtypes)

