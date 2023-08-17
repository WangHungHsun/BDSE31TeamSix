#!/usr/bin/env python
# coding: utf-8

# In[1]:


#基本模块
import numpy as np
import pandas as pd
#画图模块
import matplotlib.pyplot as plt
import seaborn as sns 
#忽略wainings 
import warnings
warnings.filterwarnings('ignore')
#图表显示设置
get_ipython().run_line_magic('matplotlib', 'inline')
# 使用自带的样式进行美化
plt.style.use("ggplot")
#清理内存
import gc


# In[2]:


df_train = pd.read_csv('application_train.csv')


# In[3]:


#对年龄进行分区
age = df_train[['DAYS_BIRTH', 'TARGET']]
age['YEARS_BIRTH'] = age['DAYS_BIRTH'] / -365
age['YEARS_BINNED'] = pd.cut(age['YEARS_BIRTH'], bins = np.linspace(20, 70, num = 11))
age_groups = age.groupby('YEARS_BINNED').mean()
#作图
plt.figure(figsize = (15, 8))
plt.bar(age_groups.index.astype(str), 100 * age_groups['TARGET'], color = 'cornflowerblue', width = 0.3, alpha = 0.7, edgecolor = 'w')
plt.title('Default Rate of Age Group',fontsize = 15)
plt.xlabel('Age Group (Years)',fontsize = 12)
plt.ylabel('Default Rate (%)',fontsize = 12)
plt.xticks(rotation = 75)
plt.show()


# In[ ]:




