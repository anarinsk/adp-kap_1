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

# %%
import numpy as np
data = np.random.randint(-100, 100, 50).cumsum()
data

plt.plot(range(50), data, 'r')
plt.title('가격변동 추이')
plt.ylabel('가격')

# %%
