## https://mkjjo.github.io/python/2019/08/18/korea_population.html
## https://datascienceschool.net/view-notebook/ef921dc25e01437b9b5c532ba3b89b02/

## Install folium 
# conda install folium -c conda-forge
# %%
import requests
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import os
import webbrowser
import folium
from folium import plugins
print(folium.__version__)