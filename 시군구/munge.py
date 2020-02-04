# %% import 
import numpy as np 
import pandas as pd 
import os

# %% This is to be changed according to coding condtion 
base_dir = 'C:/Users/anari/'
base_dir = 'D:/'
github_dir = 'github/adp-kap_1/data/'
excel_file = '월별_매입자연령대별_아파트매매거래_동호수.xlsx'
excel_dir = os.path.join(base_dir, github_dir, excel_file)

# Install xlrd in terminal!

## Load xlsx files
df_from_excel = pd.read_excel(
    excel_dir,
    sheet_name = 'Sheet1', 
    header = 10
)
# Check df 
# df_from_excel

# %% Fix df
## Fix column names 
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
## Check df 
df.describe()

# %% Set grouping rules 
## set row index 
df.set_index(['광역', '시군구1', '시군구2', '매입자연령대'], inplace=True)
#%%



#%%
## generate month and quarter columns 
month = [str(x).zfill(2)+"월" for x in range(1, 13)]
import itertools
list_tmp = ["1분기", "2분기", "3분기", "4분기"] 
quarter = list(itertools.chain.from_iterable([i, i, i] for i in list_tmp)) 
t = zip(quarter, month)
df.columns = pd.MultiIndex.from_tuples(t)
## Go with quarter 
#df = df.groupby(df.columns.get_level_values(0), axis=1).sum()
#%% 시군구1 
df0 = df.groupby(['광역', '시군구1']).sum()
df0.to_pickle('시군구1.pkl')
# %%
