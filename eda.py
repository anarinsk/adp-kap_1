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
#%%
#print(plt.style.available)
plt.rcParams['axes.prop_cycle'].by_key()['color']
# %% This is to be changed according to coding env.
#base_dir = 'C:/Users/anari/'
base_dir = 'D:/'
github_dir = 'github/adp-kap_1/'
pkl_file = '광역.pkl'
pkl_dir = os.path.join(base_dir, github_dir, pkl_file)
df = pd.read_pickle(pkl_dir)
df
# %% Munge for 청년 구매율, 거래건수 합 
df1 = df.stack(level='광역').reset_index()
#a = [x+1 for x in range(0,12)]
#b = [str(x)+'월' for x in range(0,12)]
#c = {x: y for x, y in zip(a,b)}
#df1.replace({"level_0": c}, inplace=True)
#df1['level_0'] = pd.Categorical(df1['level_0'], ordered=True, categories=b)
df1.rename(columns={'level_0': '월'}, inplace=True)

#%%
df2 = df1[['월', '광역', '청년 구매율', '합계']].sort_values(['광역', '월']).reset_index()
df2.drop(['index'], axis=1, inplace=True)
df2.set_index('월', inplace=True)
# %% Mission 1: Line plot for 광역 
## https://stackoverflow.com/questions/49237522/annotate-end-of-lines-using-python-and-matplotlib


# %% Garbage


def draw_step(data, var_y, var_x="월", alpha=0.15):
    #fig, ax = plt.subplots(figsize=(10, 6))
    data.reset_index(inplace=True)
    color = data['color'][0]    
    plt.step(data[var_x], data[var_y], where='mid', 
             linewidth=2.5, color=color, alpha=alpha)     
    plt.plot(data[var_x], data[var_y], lw=0 , color=color, marker = 'o', alpha=alpha)   


def color_assign(df, selected):
    color = plt.rcParams['axes.prop_cycle'].by_key()['color']
    df['color'] = 'gray'
    for q in range(len(selected)):
        df.loc[df['광역'] == selected[q],'color'] = color[q]
    return df
#%%
fig, ax = plt.subplots(figsize=(10, 6))

selected = ['서울', '대전', '대구']

df2 = color_assign(df2, selected)

for metro, group_data in df2.groupby('광역'):
    group_data = group_data.reset_index()
    draw_step(group_data, '청년 구매율')

for metro, group_data in df2[df2['광역'] .isin(selected)].groupby('광역'):
    group_data = group_data.reset_index()
    draw_step(group_data, '청년 구매율', alpha=1)

def touch_fig(df):
#    
    plt.xticks(np.arange(0,12, step=1))
    xlabels = [str(x+1)+'월' for x in range(0,12)]
    ax.set_xticklabels(xlabels)
    plt.ylabel('청년 구매율')
    
    dft=df[df.index == 11][['광역','청년 구매율', 'alpha']]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['광역'], alpha=0.2)

    dft=df[df.index == 11][['광역','청년 구매율', 'alpha']]
    dft=dft[dft['광역'] .isin(selected)]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['광역'], alpha=1)

touch_fig(df2)

plt.show()

#%%
dft=df2[df2.index == 11][['광역','청년 구매율']].pivot(columns='광역', values='청년 구매율')
ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks([dft[col].iloc[0] for col in dft])
ax2.set_yticklabels(dft.columns, alpha=0.2)

draw_step(df2[df2['광역']=='서울'], '청년 구매율', line_color='black', alpha=1)

plt.show()
# %%
dft=df2[df2.index == 11][['광역','청년 구매율']].pivot(columns='광역', values='청년 구매율')

# %%
dft

# %%
#df2[df2['광역']=='서울']['청년 구매율'].iloc[-1]


# %%
df2[df2['광역']=="울산"]
# %%
#df2[df2['광역'] in ['서울', '부산']]
df2[df2['광역'] .isin(['서울', '부산'])]
# %%
df2

# %%
