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


# In[4]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 假设你的数据集 df_train 已经准备好

age = df_train[['DAYS_BIRTH', 'TARGET']]
age['YEARS_BIRTH'] = age['DAYS_BIRTH'] / -365
age['YEARS_BINNED'] = pd.cut(age['YEARS_BIRTH'], bins=np.linspace(20, 70, num=11))
age_groups = age.groupby('YEARS_BINNED').mean()

# 作图
plt.figure(figsize=(15, 8))
plt.bar(age_groups.index.astype(str), 100 * age_groups['TARGET'], color='cornflowerblue', width=0.3, alpha=0.7, edgecolor='w')
plt.title('Default Rate of Age Group', fontsize=15)
plt.xlabel('Age Group (Years)', fontsize=12)
plt.ylabel('Default Rate (%)', fontsize=12)
plt.xticks(rotation=75)

# 保存图为 PNG 文件
plt.savefig('age_default_rate.png')

# 显示图
plt.show()


# In[ ]:





# In[6]:


#（OCCUPATION_TYPE）
tem = df_train.loc[:, ['OCCUPATION_TYPE', 'TARGET']]
tem.fillna('none', inplace = True)
#tem1表示各个职位中逾期的人数
tem1 = tem.groupby('OCCUPATION_TYPE').sum( )
#tem2表示各个职业的总人数
tem2 = tem.groupby('OCCUPATION_TYPE').count( )
#tem3表示各个职位逾期比率
tem3 =  tem1 / tem2 * 100
tem3.reset_index(inplace = True)
tem2.reset_index(inplace = True)
fig = plt.figure(figsize = (15, 8))
ax1 = fig.add_subplot(111)
#Count
ax1.bar('OCCUPATION_TYPE', 'TARGET', data = tem2, width = 0.3, edgecolor = 'w', label = 'Count', color = 'mediumpurple', alpha = 0.8)
plt.xlabel('Occupation Type', fontsize = 12)
plt.ylabel('Count', fontsize = 12)
plt.xticks(rotation = 75, fontsize = 12)
#设置双坐标轴，右侧Y轴
ax2 = ax1.twinx( )
#设置右侧Y轴显示百分数
import matplotlib.ticker as mtick
fmt = '%0.2f%%'
yticks = mtick.FormatStrFormatter(fmt)
#Default Rate
ax2.plot(tem3['OCCUPATION_TYPE'], tem3['TARGET'], label = 'Default Rate', linewidth = 3, color = 'orange', alpha = 0.7)
ax2.yaxis.set_major_formatter(yticks)
ax1.set_ylabel('Count', fontsize = 12)
ax2.set_ylabel('Default Rate', fontsize = 12)
legend1 = ax1.legend(loc = (.02,.94), fontsize = 10, shadow = True)
legend2 = ax2.legend(loc = (.02,.9), fontsize = 10, shadow = True)
plt.title('Count & Default Rate of Occupation Type', fontsize = 15) 

plt.savefig('carrer_default_rate.png')

plt.show( )


# In[ ]:





# In[8]:


#（DAYS_EMPLOYED）
tem = df_train.loc[:, ['DAYS_EMPLOYED', 'TARGET']]
#发现异常值DAYS_EMPLOYED = 365243，取出单独分析
tem1 = tem[tem['TARGET'] == 1]['DAYS_EMPLOYED']
tem1_norm = tem1[tem1 != 365243] / -365
tem1_a_norm = tem1[tem1 == 365243] / 365
tem0 = tem[tem['TARGET'] == 0]['DAYS_EMPLOYED']
tem0_norm = tem0[tem0 != 365243] / -365
tem0_a_norm = tem0[tem0 == 365243] / 365
fig, ax = plt.subplots(2, 1, figsize = (15, 12))
#Nomal
ax[0].hist(tem1_norm.values, bins = 100, label = '1', density = True, alpha = 0.8, color = 'salmon', edgecolor = 'w')
ax[0].hist(tem0_norm.values, bins = 100, label = '0', density = True, alpha = 0.7, color = 'cornflowerblue', edgecolor = 'w')
ax[0].set_title('Distribution  of  Years_Employed (Nomal)', fontsize = 15)
ax[0].set_xlabel('Years_Employed', fontsize = 12)
ax[0].set_ylabel('Probability', fontsize = 12)
ax[0].legend(fontsize = 'large')
#Abnomal
ax[1].hist(tem1_a_norm.values, bins = 3, label = '1',density = False, alpha = 0.8, color = 'salmon')
ax[1].hist(tem0_a_norm.values, bins = 3, label = '0',density = False, alpha = 0.7, color = 'cornflowerblue')
ax[1].set_title('Distribution  of Years_Employed (Abnomal)', fontsize = 15)
ax[1].set_xlabel('YEARS_EMPLOYED', fontsize = 12)
ax[1].set_ylabel('Count', fontsize = 12)
ax[1].legend(fontsize = 'large')

plt.savefig('DAYS_EMPLOYED_Default Rate.png')

plt.show()


# In[ ]:





# In[9]:


tem = df_train.loc[:, ['AMT_INCOME_TOTAL','TARGET']]
tem.describe()


# In[11]:


#tem1表示逾期客户的年总收入，tem0表示正常客户的年总收入
tem1 = tem[tem['TARGET'] == 1]['AMT_INCOME_TOTAL']
tem0 = tem[tem['TARGET'] == 0]['AMT_INCOME_TOTAL']
#分别取逾期和正常客户年总收入的前98%数据
tem1_98 = tem1[tem1<= np.percentile(tem1, 98)]
tem0_98 = tem0[tem0<= np.percentile(tem0, 98)]
fig, ax = plt.subplots(figsize = (15, 8), sharex = True)
plt.hist(tem1_98.values, bins = 200, label = '1', density = True, width = 5000, alpha = 0.8, color = 'gold', edgecolor = 'w')
plt.hist(tem0_98.values, bins = 200, label = '0', density = True, width = 5000, alpha = 0.7, color = 'mediumpurple', edgecolor = 'w')
plt.title('Distribution  of  Amt_Income_Total', fontsize = 15)
plt.xlabel('AMT_INCOME_TOTAL', fontsize = 12)
plt.ylabel('Probability', fontsize = 12)
plt.legend(fontsize = 'large')

plt.savefig('AMT_INCOME_TOTAL_Default Rate.png')

plt.show()


# In[ ]:





# In[12]:


tem = df_train.loc[:, ['AMT_CREDIT', 'AMT_INCOME_TOTAL', 'TARGET'] ]
#贷款占總收入的比率
tem['CreditToIncomeRatio'] = df_train['AMT_CREDIT'] / df_train['AMT_INCOME_TOTAL']
tem.describe()


# In[16]:


tem1 = tem[tem['TARGET'] == 1]['CreditToIncomeRatio']
tem0 = tem[tem['TARGET'] == 0]['CreditToIncomeRatio']
#分别取逾期和正常客户年债務收入比的前98%數據
tem1_98 = tem1[tem1 <= np.percentile(tem1, 98)]
tem0_98 = tem0[tem0 <= np.percentile(tem0, 98)]
fig, ax = plt.subplots(figsize =(15, 8), sharex = True)
plt.hist(tem1_98.values, bins = 90, label = '1', density = True, alpha = 0.7, color = 'salmon', edgecolor = 'w')
plt.hist(tem0_98.values, bins = 90, label = '0', density = True, alpha = 0.6, color = 'cornflowerblue', edgecolor = 'w')
plt.title('Distribution  of  Credit_To_Income_Ratio', fontsize = 15)
plt.xlabel('Credit To Income Ratio', fontsize = 12)
plt.ylabel('Probability', fontsize = 12)
plt.legend(fontsize = 'large')

plt.savefig('credit_to_income_ratio_distribution.png')

plt.show()


# In[ ]:





# In[21]:


#导入历史申请表
pa = pd.read_csv('previous_application.csv')
tem = pa.loc[:, ['SK_ID_CURR', 'SK_ID_PREV']]
tem = tem.groupby(['SK_ID_CURR']).count().reset_index()
tem = df_train.loc[:, ['SK_ID_CURR','TARGET']].merge(tem, how = 'left', on = 'SK_ID_CURR')
tem = tem.loc[:, ['SK_ID_PREV','TARGET']]
#tem1表示各个借款次数下的总人数
tem1 = tem.groupby('SK_ID_PREV').count()
#tem2表示各个借款次数下的违约总人数
tem2 = tem.groupby('SK_ID_PREV').sum()
#f3表示各个借款次数下的违约率
tem3 = tem2 / tem1 * 100
tem3.reset_index(inplace = True)
tem1.reset_index(inplace = True)
fig = plt.figure(figsize = (15, 8))
ax1 = fig.add_subplot(111)
#由于次数大于20的人数较少且毁约率波动很大，只选取小于20的贷款次数进行作图
ax1.bar('SK_ID_PREV', 'TARGET', width = 0.5, data = tem1[tem1['SK_ID_PREV'] < 21], 
        edgecolor = 'w', label = 'Count', color = 'navajowhite')
plt.xlabel('Times Of Previous Loans (History)', fontsize = 12)
plt.ylabel('Count', fontsize = 12)
#设置双坐标轴，右侧Y轴
ax2 = ax1.twinx( )
#设置右侧Y轴显示百分数
import matplotlib.ticker as mtick
fmt = '%0.2f%%'
yticks = mtick.FormatStrFormatter(fmt)
#Default Rate
ax2.plot(tem3[tem3['SK_ID_PREV'] < 21]['SK_ID_PREV'], tem3[tem3['SK_ID_PREV'] < 21]['TARGET'], 
         label = 'Default Rate', linewidth = 3, color = 'cornflowerblue')
ax2.yaxis.set_major_formatter(yticks)
ax2.set_ylabel('Default Rate', fontsize = 12)
legend1=ax1.legend(loc=(0.75, .94), fontsize = 10, shadow = True)
legend2=ax2.legend(loc=(0.75, .9), fontsize = 10, shadow = True)
plt.title('Count & Default Rate  of History Previous Loans Times', fontsize = 15) 

fig.savefig('loan_times_default_rate.png')

plt.show( )


# In[ ]:




