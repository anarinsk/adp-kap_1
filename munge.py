# %%
import numpy as np 
import pandas as pd 
import os

# %%
base_dir = 'C:/Users/anari/'
#base_dir = 'D:/'
github_dir = 'github/adp-kap_1/data/'
excel_file = '월별_매입자연령대별_아파트매매거래_동호수.xlsx'

excel_dir = os.path.join(base_dir, github_dir, excel_file)

# %%
# Install xlrd in terminal 
df_from_excel = pd.read_excel(
    excel_dir,
    sheet_name = 'Sheet1', 
    header = 10
)
# Check df 
#df_from_excel

# %% Fix df
# Fix column names 
renames = {'지 역': '광역', 'Unnamed: 1': "시군구1", 'Unnamed: 2': '시군구2'}
df_from_excel.rename(columns=renames, inplace=True)
df = df_from_excel.copy()
# Fill nan 
df['광역'] = df['광역'].fillna(method='ffill') 
df['시군구1'] = df['시군구1'].fillna(method='ffill') 
df['시군구2'] = df['시군구2'].fillna(method='ffill') 
df = df.loc[df['광역'] != '전국']
df.replace('-', 0, inplace=True)
df.fillna(0, inplace=True)
# Check df 
df.describe()

# %% Set grouping rules 
df.columns
# %% Testing multi-index & Multi-columns
##Testing multi-column 
df.set_index(['광역', '시군구1', '시군구2', '매입자연령대'], inplace=True)

#%%
month = ["2019년 "+str(x).zfill(2)+"월" for x in range(1, 13)]
import itertools
list_tmp = ["2019년 1분기", "2019년 2분기", "2019년 3분기", "2019년 4분기"] 
quarter = list(itertools.chain.from_iterable([i, i, i] for i in list_tmp)) 
t = zip(quarter, month)
df.columns = pd.MultiIndex.from_tuples(t)
#%%
#df.groupby([,axis=1]).sum()
#test.reset_index(level=2) 
#test.reset_index(inplace=True)

# %%
df.groupby(df.columns.get_level_values(0), axis=1).sum()
# %%