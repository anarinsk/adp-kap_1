# -*- coding: utf-8 -*-
"""
"""

# %% import 
import numpy as np 
import pandas as pd 
import os
# %% This is to be changed according to coding env.
## for generating dir 
def gen_dir(terminal, where="work"):
    if where == "work": 
        base_dir = 'D:/'
    else:
        base_dir = 'C:/Users/anari/'
    
    github_dir = 'github/adp-kap_1/'
    return os.path.join(base_dir, github_dir, terminal)

excel_dir = gen_dir('data/월별_매입자연령대별_아파트매매거래_동호수.xlsx')

## Install xlrd by `conda install xlrd`


# %% functions 
## for loading & massaging xlsx 
def process_raw(dir=excel_dir):
    """ function for loading excel data  
    
    Args: 
        dir(str):  folder for xlsx 
    
    returns: 
        DataFrames          

    """    
    df_from_excel = pd.read_excel(
    dir,
    sheet_name = 'Sheet1', 
    header = 10)

    renames = {'지 역': '광역', 'Unnamed: 1': "시군구1", 'Unnamed: 2': '시군구2'}
    df_from_excel.rename(columns=renames, inplace=True)
    df = df_from_excel.copy()
    ## Fill nan 
    df['광역'] = df['광역'].fillna(method='ffill') 
    df = df.groupby('광역').apply(lambda x: x.iloc[8:,:])
    df['시군구1'] = df['시군구1'].fillna(method='ffill') 
    df['시군구2'] = df['시군구2'].fillna(method='ffill') 
    df = df.loc[df['광역'] != '전국']
    df.replace('-', 0, inplace=True)
    df.fillna(0, inplace=True)

    return df 
## for massaging data 
def gen_refdt(period='m', groups=['광역', '시군구1', '매입자연령대'], dir=excel_dir):
    """ function for generating excel data  
    
    Args: 
        period(str): 'm' for month, 'q' for quarter 
        dir(str):  folder for xlsx 
    
    returns: 
        DataFrames          

    """    
    dt = process_raw(dir)
    dt.set_index(['광역', '시군구1', '시군구2', '매입자연령대'], inplace=True)
    month = [str(x).zfill(2)+"월" for x in range(1, 13)]    
    quarter = list(itertools.chain.from_iterable([i, i, i] for i in ["1분기", "2분기", "3분기", "4분기"] )) 
    t = zip(quarter, month)
    dt.columns = pd.MultiIndex.from_tuples(t)
    ## Go with quarter 
    if period == 'q':  
        dt = dt.groupby(dt.columns.get_level_values(0), axis=1).sum()
    else:   
        dt = dt.groupby(dt.columns.get_level_values(1), axis=1).sum()
    
    return dt.groupby(groups).sum().T     

#%%
tdf1 = gen_refdt('m', ['광역', '매입자연령대']).drop(columns = ['합계'], level=1)
def gen_columns(x):
    x.columns = [col[1] for col in x.columns]
    x['합계'] = x.sum(axis=1)   
    x['청년 구매율'] = (x['20대이하'] + x['30대'])/x.drop('합계', axis=1).sum(axis=1)
    return x.reset_index()

tdf2 = tdf1.groupby(level=0, axis=1).apply(gen_columns)
tdf2.to_pickle(gen_dir('광역/광역.pkl', where='work'))

## End of code