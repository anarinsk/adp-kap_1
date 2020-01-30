# %% Initialize 

## import 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.style
import matplotlib as mpl
mpl.style.use('seaborn-pastel')

## Korean font setting 
plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 12.
plt.rcParams['ytick.labelsize'] = 12.
plt.rcParams['axes.labelsize'] = 15.

## install by `conda install geopandas`
import geopandas as gpd
gpd.__version__
# %% 
seoul_file = "./data/201812기초구역DB_전체분/서울특별시/TL_KODIS_BAS_11.shp"
seoul = gpd.read_file(seoul_file, encoding='euckr')
seoul.tail(3)
# %% 
## descartes shoud be installed by `conda install descartes`
ax = seoul.plot(figsize=(11, 11), color="w", edgecolor="k")
ax.set_title("서울 특별시 기초구역도")
ax.set_axis_off()
plt.show()
# %%
sample = seoul[seoul.SIG_KOR_NM == "동작구"]

ax = plt.subplot(2, 2, 1)
sample.plot(color='k', edgecolor="w", ax=ax)
ax.set_title("동작구")
ax.set_axis_off()

ax = plt.subplot(2, 2, 2)
sample.convex_hull.plot(color='k', edgecolor="w", ax=ax)
ax.set_title("convex_hull")
ax.set_axis_off()

ax = plt.subplot(2, 2, 3)
sample.envelope.plot(color='k', edgecolor="w", ax=ax)
ax.set_title("envelope")
ax.set_axis_off()

ax = plt.subplot(2, 2, 4)
gpd.GeoSeries([sample.geometry.buffer(0.1).unary_union]
              ).plot(ax=ax, color="k", edgecolor='w')
ax.set_title("unary_union")
ax.set_axis_off()

plt.tight_layout()
plt.show()
# %%
seoul.geometry = seoul.buffer(0.5)
seoul.geometry = seoul.envelope
seoul = seoul.dissolve(by='SIG_CD')
ax = seoul.plot(figsize=(15, 15), column="SIG_KOR_NM", categorical=True,
                cmap="tab20b", edgecolor="k", legend=True, legend_kwds={'loc': 3})
ax.set_title("구 별로 묶은 서울의 기초 구역도")
ax.set_axis_off()
plt.show()

# %%
