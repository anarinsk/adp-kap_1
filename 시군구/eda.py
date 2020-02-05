# %% import 
import numpy as np 
import pandas as pd 
import os
# matplot related 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.style
import matplotlib as mpl
import itertools
import copy

# Assign plotting style 
mpl.style.use('seaborn-pastel')
plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 9.
plt.rcParams['ytick.labelsize'] = 9.
plt.rcParams['axes.labelsize'] = 12.

# %% Misc. & Params 
def gen_dir(terminal, where=here):
    if where == "work": 
        base_dir = 'D:/'
    else:
        base_dir = 'C:/Users/anari/'
    
    github_dir = 'github/adp-kap_1/'
    return os.path.join(base_dir, github_dir, terminal)

here = "home"
# %% Load, Pivot, Massage
df = pd.read_pickle(gen_dir('시군구/시군구1.pkl'))
df1 = df.stack(level=['광역','시군구1']).reset_index()
df1.drop(columns = ['index'], inplace=True)
df1.rename(columns={'level_0': '월'}, inplace=True)

# %% Custom filters 
my_filter1 = (df1['청년 구매율'].notna()) & (df1['청년 구매율'] > 0) & (df1['합계'] > 20) 
my_filter2 = my_filter1 & (df1['광역']=='서울') 
df2 = df1.loc[my_filter2]

# %%
df_cor = df2.groupby(['시군구1'])[['청년 구매율', '합계']].corr(method='kendall')
df_cor.reset_index(inplace=True)
df_cor = df_cor.loc[(df_cor['합계'].notna())]
df_cor = df_cor[df_cor['level_1'] == "청년 구매율"][['시군구1', '합계']]
df_cor.columns = ['시군구', '상관계수']
df_cor.sort_values(['상관계수'], ascending=False)
#%%
p_df = df_cor.sort_values(['상관계수'])
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(p_df['시군구'], p_df['상관계수'], align='center')
ax.legend([r'Kendall $\tau$'])
#plt.savefig('kendalltau.png', dpi=300)
# %%
