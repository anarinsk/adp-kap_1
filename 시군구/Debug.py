#%%
dir = 'D:/github/adp-kap_1/data/월별_매입자연령대별_아파트매매거래_동호수.xlsx'
df_from_excel = pd.read_excel(
    dir,
    sheet_name = 'Sheet1', 
    header = 10)

#%%
renames = {'지 역': '광역', 'Unnamed: 1': "시군구1", 'Unnamed: 2': '시군구2'}
df_from_excel.rename(columns=renames, inplace=True)
df = df_from_excel.copy()
#%%
## Fill nan 
df.replace('-', 0, inplace=True)
df['광역'] = df['광역'].fillna(method='ffill') 
df = df.groupby('광역').apply(lambda x: x.iloc[8:,:])
df['시군구1'] = df['시군구1'].fillna(method='ffill') 
df['시군구2'] = df['시군구2'].fillna(method='ffill') 
df = df.loc[df['광역'] != '전국']
df.fillna(0, inplace=True)
#%%


# %%
df 

# %%
df['광역'] = df['광역'].fillna(method='ffill') 
df.groupby('광역').apply(lambda x: x.iloc[8:,:])
# %%
