#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# 讀取兩個 CSV 檔案
df_test = pd.read_csv("application_test.csv")
df_train = pd.read_csv("application_train.csv")

# 合併兩個 DataFrame
merged_df = pd.concat([df_test, df_train], axis=0, ignore_index=True)

# 設定合併後的 DataFrame 索引為 'SK_ID_CURR'
merged_df.set_index('SK_ID_CURR', inplace=True)

# 印出合併的結果
print(merged_df)


# In[2]:


import pandas as pd

# 讀取 application_test.csv 和 application_train.csv 的 SK_ID_CURR 列
df_test = pd.read_csv("application_test.csv", usecols=['SK_ID_CURR'])
df_train = pd.read_csv("application_train.csv", usecols=['SK_ID_CURR'])

# 合併 SK_ID_CURR 列並排序
merged_id_curr = pd.concat([df_test['SK_ID_CURR'], df_train['SK_ID_CURR']], ignore_index=True)
merged_id_curr = merged_id_curr.sort_values()

# 印出合併並排序後的結果
print(merged_id_curr)


# In[3]:


import pandas as pd

# 讀取 previous_application.csv 的 SK_ID_CURR 列
df_previous = pd.read_csv("previous_application.csv", usecols=['SK_ID_CURR'])

# 進行排序
sorted_id_curr = df_previous['SK_ID_CURR'].sort_values()

# 印出合併並排序後的結果
print(sorted_id_curr)


# In[4]:


import pandas as pd

# 讀取 previous_application.csv 的 SK_ID_CURR 列
df_previous = pd.read_csv("previous_application.csv", usecols=['SK_ID_CURR'])

# 讀取 application_test.csv 和 application_train.csv 的 SK_ID_CURR 列
df_test = pd.read_csv("application_test.csv", usecols=['SK_ID_CURR'])
df_train = pd.read_csv("application_train.csv", usecols=['SK_ID_CURR'])

# 合併 application_test.csv 和 application_train.csv 的 SK_ID_CURR 列
merged_id_curr = pd.concat([df_test['SK_ID_CURR'], df_train['SK_ID_CURR']], ignore_index=True)

# 比較兩個 DataFrame 的 SK_ID_CURR 列是否有不相似之處
differences = df_previous[~df_previous['SK_ID_CURR'].isin(merged_id_curr)]

# 印出比對結果
print(differences)


# In[ ]:





# In[3]:


import pandas as pd

# Read application_test.csv and application_train.csv SK_ID_CURR columns
df_test = pd.read_csv("application_test.csv", usecols=['SK_ID_CURR'])
df_train = pd.read_csv("application_train.csv", usecols=['SK_ID_CURR'])

# Concatenate application_test.csv and application_train.csv SK_ID_CURR columns
merged_id_curr = pd.concat([df_test['SK_ID_CURR'], df_train['SK_ID_CURR']], ignore_index=True)

# Create a DataFrame to store the results
merged_df = pd.DataFrame({
    'SK_ID_CURR': pd.concat([df_test['SK_ID_CURR'].head(50),
                            df_train['SK_ID_CURR'].head(50),
                            merged_id_curr.head(50),
                            df_test['SK_ID_CURR'].tail(50),
                            df_train['SK_ID_CURR'].tail(50),
                            merged_id_curr.tail(50)]),
    'Source': ['Test'] * 50 + ['Train'] * 50 + ['Merged'] * 50 + ['Test'] * 50 + ['Train'] * 50 + ['Merged'] * 50
})

# Print the merged DataFrame
print(merged_df)


# In[4]:


# Read previous_application.csv SK_ID_CURR column
df_previous = pd.read_csv("previous_application.csv", usecols=['SK_ID_CURR'])

# Create a DataFrame to store the results
previous_df = pd.DataFrame({
    'SK_ID_CURR': pd.concat([df_previous['SK_ID_CURR'].head(50), df_previous['SK_ID_CURR'].tail(50)]),
    'Source': ['Previous'] * 50 + ['Previous'] * 50
})

# Print the previous DataFrame
print(previous_df)


# In[ ]:




