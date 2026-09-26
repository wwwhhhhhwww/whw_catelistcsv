import pandas as pd

df = pd.read_excel(r'C:\Users\110\PycharmProjects\zeosyn_data\ZEOSYN.xlsx')
#print(df)
print(df.shape)                    # 行数、列数
#print(df.columns.tolist())         # 全部列名（100 个）
#print(df.head())                   # 前 5 行

#print(df.isna().all(axis=1).sum())      # 完全空的行有几个
#print(df.drop(columns=['Unnamed: 0']).isna().all(axis=1).sum())
#print(df.duplicated().sum())            # 完全重复的行有几对
#print(df['Code1'].notna().sum())        # Code1（产物骨架）非空的行数
#print(df['Code1'].nunique())            # 一共有多少种不同的产物骨架
#print(df['normed'].value_counts(dropna=False))


#B10e
df_clean = df[df['doi'].notna()]     # 布尔索引（B6 学过）+ notna（B7 学过）
print(df_clean.shape)
print(df_clean['Code1'].value_counts())
print(df_clean['Code1'].value_counts().head(10))
print((df_clean['Code1'] == 'MFI').mean())


# 沸石骨架的"结构描述符"表
df_zeos = pd.read_csv(r'C:\Users\110\PycharmProjects\zeosyn_data\zeolite_descriptors.csv')
df_zeos = df_zeos.rename(columns={'Unnamed: 0': 'Code'})     # ← 练你刚问的 rename
print(df_zeos.shape)
print(df_zeos.columns.tolist())

# OSDA（模板分子）的"性质描述符"表
df_osda = pd.read_csv(r'C:\Users\110\PycharmProjects\zeosyn_data\osda_descriptors.csv')
df_osda = df_osda.drop(columns=['Unnamed: 0'])               # ← 练 drop（对比 rename）
print(df_osda.shape)
print(df_osda.columns.tolist()[:20])

