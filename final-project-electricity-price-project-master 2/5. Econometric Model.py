#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sklearn import linear_model
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy
from linearmodels.panel import PanelOLS
from shiny import App, render, ui, reactive


path = "C:/Users/wynbu/Desktop/Python Final/"
eprice = pd.read_csv('E_Price.csv')

eprice = eprice.dropna()
eprice


# In[19]:


eprice = eprice[eprice['sectorName'].apply(lambda i: i in ['residential'])]
eprice = eprice.drop(columns = ['Unnamed: 0','stateDescription','sectorid','price-units','sectorName'])
eprice


# ### Econometric Model

# In[37]:


coal = pd.read_csv('coal.csv')
ng = pd.read_csv('natural_gas.csv')
coal.head()


# In[38]:


ng = ng.drop(columns = ['Unnamed: 0','units'])
ng.head()


# In[40]:


coal = coal.rename(columns={"State":"stateid",
                        "price":"value"})


# In[50]:


df_total = coal.merge(ng, on = ['stateid','period']).rename(columns={"value_x":"coal_price",
                        "value_y":"ng_price"})
df_total = df_total.merge(eprice, on = ['stateid','period']).rename(columns={"price":"e_price"})
df_total.head()


# In[52]:


df_total['period'] = pd.to_datetime(df_total['period'], format='%Y')
df_total = df_total.set_index(['stateid','period'])


# In[54]:


df_total.index


# In[57]:


reg  = PanelOLS(df_total['e_price'],df_total[['coal_price','ng_price']],entity_effects=True,time_effects=True).fit(cov_type='clustered', cluster_entity=True, cluster_time=True)
print(reg)


# In[ ]:




