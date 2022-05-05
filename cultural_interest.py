import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')

df_top10_number['Media number'] = round(df_top10_number['titleId']/1000000,2)

df_top10_minutes['Total duration'] = round(df_top10_minutes['minutes']/60/24)

df_top10 = df_top10_number.merge(df_top10_minutes,how='inner',on='region')

df_top10 = df_top10_number.merge(df_top10_minutes,how='inner',on='region')



fig, axs = plt.subplots(1,2,figsize=(15, 5))

sns.barplot(data=df_top10,x='Media number', y='region',color='royalblue',ax=axs[0])
axs[0].set_title('Number of media translated per region')


sns.barplot(data=df_top10,x='Total duration', y='region',color='royalblue',ax=axs[1])
axs[1].set_title('Total duration translated per region in days')
axs[1].set(ylabel=None)

plt.show()