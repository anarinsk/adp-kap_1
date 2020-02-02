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
mpl.style.use('seaborn-pastel')

plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 12.
plt.rcParams['ytick.labelsize'] = 12.
plt.rcParams['axes.labelsize'] = 15.
# %% This is to be changed according to coding env.
base_dir = 'C:/Users/anari/'
#base_dir = 'D:/'
github_dir = 'github/adp-kap_1/'
pkl_file = '광역.pkl'
pkl_dir = os.path.join(base_dir, github_dir, pkl_file)

# %%
df = pd.read_pickle(pkl_dir)
df
#df.set_index(['index'])
# %% Draw sum to 쳥년 구매율 
# scatter plot by each 광역 도시 
df1 = df.stack(level='광역').reset_index()
df1
# %%
a = [x for x in range(0,12)]
b = [str(x+1)+'월' for x in range(0,12)]
c = {x: y for x, y in zip(a,b)}
df1.replace({"level_0": c}, inplace=True)
#df1.set_index('level_0', inplace=True)
#%%
df1['level_0'] = pd.Categorical(df1['level_0'], ordered=True, categories=b)
df1.rename(columns={'level_0': '월'}, inplace=True)
#%%
#df1.columns
df2 = df1[['level_0', '광역', '청년 구매율', '합계']].sort_values(['광역', 'level_0']).reset_index()
df2.drop(['index'], axis=1, inplace=True)

# %%
df2.columns
# %%
df2.set_index('level_0', inplace=True)
df2
#%%
fig, ax = plt.subplots(figsize=(10, 6))
df2.groupby('광역')['청년 구매율'].plot(legend=False, color='gray', ax=ax)
df2[df2['광역']=='서울']['청년 구매율'].plot(legend=False, color='purple', ax=ax)
ax2 = ax.twinx()

ax2.set_ylim(ax.get_ylim())
ax2.set_yticks([df[col].iloc[-1] for col in yq])
ax2.set_yticklabels(yq)

# %%
plt.show()
# %%
df2['광역'].unique()

# %%
df2.groupby('광역').apply(lambda x : x[x['level_0']==1]['청년 구매율'])

# %%
df2[df2.index==11][['광역', '청년 구매율']].reset_index(drop=True).unstack()

# %%
