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
## generate month and quarter columns 
month = [str(x).zfill(2)+"월" for x in range(1, 13)]
import itertools
list_tmp = ["1분기", "2분기", "3분기", "4분기"] 
quarter = list(itertools.chain.from_iterable([i, i, i] for i in list_tmp)) 
t = zip(quarter, month)
df.columns = pd.MultiIndex.from_tuples(t)
## Go with quarter 
df = df.groupby(df.columns.get_level_values(0), axis=1).sum()
#%%
df['1분기']


# %% Testing Module 
## STRATEGY 
## Making proper table on the fly 

## First row indexing 

tdf0 = df['1분기'].to_frame().groupby(['광역', '매입자연령대']).sum().T
tdf0
#%%
tdf1 = tdf0.loc[:, ('광주')].drop(['합계'], axis=1)
tdf1['기간 합'] = tdf1.sum(axis = 1)
tdf1['청년 비율'] = (tdf1['20대이하'] + tdf1['30대']) / tdf1['기간 합']
tdf1
#%%
tdf2 = tdf1.div(tdf1.sum(axis=1), axis=0).reset_index().drop(['level_0'], axis=1)
tdf2 = tdf2.rename(columns = {'level_1': '2019년'})
tdf2.set_index(['2019년'], inplace=True)
#%%
## Second column indexing 
tdf2.div(tdf2.sum(axis=1), axis=0).plot.bar(stacked=True, rot=0)
plt.show()
# %%


#%%
print ('버전: ', mpl.__version__)
print ('설치 위치: ', mpl.__file__)
print ('설정 위치: ', mpl.get_configdir())
print ('캐시 위치: ', mpl.get_cachedir())


# %%
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.style
import matplotlib as mpl
mpl.style.use('seaborn-pastel')

plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 12.
plt.rcParams['ytick.labelsize'] = 12.
plt.rcParams['axes.labelsize'] = 15.

#%%
tdf2.div(tdf2.sum(axis=1), axis=0).plot.bar(stacked=True, rot=0)
plt.show()
# %%


# %%
