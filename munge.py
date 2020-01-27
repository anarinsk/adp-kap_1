# %%
import numpy as np 
import pandas as pd 
import os

# %%
base_dir = 'C:/Users/anari/'
github_dir = 'github/adp-kap_1/data/'
excel_file = '월별_매입자연령대별_아파트매매거래_동호수.xlsx'

excel_dir = os.path.join(base_dir, github_dir, excel_file)

# %%
excel_dir

# %%
df_from_excel = pd.read_excel(
    excel_dir,
    sheet_name = 'Sheet1', 
    header = 10
)
# %%
df_from_excel

# %% Fix column names 
renames = {'지 역': '광역', 'Unnamed: 1': "시군구1", 'Unnamed: 2': '시군구2'}
df_from_excel.rename(columns=renames, inplace=True)
# %%
df_from_excel

# %% Copy working df 
df = df_from_excel.copy()

# %% Fill nan 
df['광역'] = df['광역'].fillna(method='ffill') 
df['시군구1'] = df['시군구1'].fillna(method='ffill') 
df['시군구2'] = df['시군구2'].fillna(method='ffill') 

# %%
# %%
df_vis = df.copy()
df_vis = df_vis.loc[df_vis['광역'] != '전국']
df_vis.replace('-', 0, inplace=True)
df_vis.fillna(0, inplace=True)
df_vis.groupby(['광역']).sum()

#df_vis.describe()
# %%
