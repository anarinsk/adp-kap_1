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
import random 

# Assign plotting style 
mpl.style.use('seaborn-pastel')
plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 10.
plt.rcParams['ytick.labelsize'] = 10.
plt.rcParams['axes.labelsize'] = 13.

# Global Parameters 

here = "work"
# %% Misc. & Params 
def gen_dir(terminal, where=here):
    if where == "work": 
        base_dir = 'D:/'
    else:
        base_dir = 'C:/Users/anari/'
    
    github_dir = 'github/adp-kap_1/'
    return os.path.join(base_dir, github_dir, terminal)
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
## Visualization by local-Gwangyuk

def gen_filtered_df(gwangyuk, df, total_limit=20): 
    
    my_filter1 = (df['청년 구매율'].notna()) & (df['합계'] >= total_limit) 
    df = df.loc[my_filter1 & (df['광역'].isin(gwangyuk))]
    return df 

def draw_step(data, var_y, var_x="월", alpha=0.15):
    #fig, ax = plt.subplots(figsize=(10, 6))
    data.reset_index(inplace=True)
    color = data['color'][0]    
    plt.step(data[var_x], data[var_y], where='mid', 
             linewidth=2.5, color=color, alpha=alpha)     
    plt.plot(data[var_x], data[var_y], lw=0 , color=color, marker = 'o', alpha=alpha)   

def color_assign(df, selected):
    color = plt.rcParams['axes.prop_cycle'].by_key()['color']
    df = df.assign(color='gray')
    for q in range(len(selected)):
        df.loc[df['시군구1'] == selected[q],'color'] = color[q]
    return df

def touch_fig(df):
#    
    plt.xticks(np.arange(0,12, step=1))
    xlabels = [str(x+1)+'월' for x in range(0,12)]
    ax.set_xticklabels(xlabels)
    plt.ylabel('청년 구매율')
    
    dft=df.loc[df['월']==11][['시군구1','청년 구매율']]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['시군구1'], alpha=0.2)

    dft=df.loc[df['월']==11][['시군구1','청년 구매율']]
    dft=dft[dft['시군구1'].isin(selected)]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['시군구1'], alpha=1)
#%% Funtions testing 
selected = ['은평구', '마포구']
df2 = gen_filtered_df(['서울'], df1)
df2 = color_assign(df2, selected)

random.sample(list(df2['시군구1'].unique()),2)
#%%
def draw_gwangyuk(df, 
                  two_cities="no", 
                  figsize=(9,6)):

    fig, ax = plt.subplots(figsize=figsize)

    if two_cities=="no":
        selected = random.sample(list(df2['시군구1'].unique()),2)
    else: 
        selected = two_cities

    df = color_assign(df, selected)

    for metro, group_data in df.groupby('시군구1'):
        group_data = group_data.reset_index()
        draw_step(group_data, '청년 구매율')

    for metro, group_data in df[df['시군구1'].isin(selected)].groupby('시군구1'):
        group_data = group_data.reset_index()
        draw_step(group_data, '청년 구매율', alpha=1)

    plt.xticks(np.arange(0,12, step=1))
    xlabels = [str(x+1)+'월' for x in range(0,12)]
    ax.set_xticklabels(xlabels)
    plt.ylabel('청년 구매율')
    
    dft=df.loc[df['월']==11][['시군구1','청년 구매율']]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['시군구1'], alpha=0.2)

    dft=df.loc[df['월']==11][['시군구1','청년 구매율']]
    dft=dft[dft['시군구1'].isin(selected)]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['시군구1'], alpha=1)

    return plt.show()
#plt.savefig(gen_dir('광역\youthrate.png', where='work'), dpi=300)
# %%
def draw_corr(df, my_gwangyuk=["서울"]): 
    # %% Custom filters 
    my_filter1 = (df['청년 구매율'].notna())  
    my_filter2 = my_filter1 & (df1['광역'].isin(my_gwangyuk)) 
    df = df.loc[my_filter2]
    # corr
    df_cor = df.groupby(['시군구1'])[['청년 구매율', '합계']].corr(method='kendall')
    df_cor.reset_index(inplace=True)
    df_cor = df_cor.loc[(df_cor['합계'].notna())]
    df_cor = df_cor[df_cor['level_1'] == "청년 구매율"][['시군구1', '합계']]
    df_cor.columns = ['시군구', '상관계수']
    df_cor.sort_values(['상관계수'], ascending=False)
    df2 = df_cor.sort_values(['상관계수'])

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(df2['시군구'], df2['상관계수'], align='center')
    ax.legend([r'Kendall $\tau$'])

# %%
draw_corr(df1, ["광주"])
# %%
