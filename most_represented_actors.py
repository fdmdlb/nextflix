import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_top_people = pd.read_csv('./data/6ko_top5_movies_people.csv')

fig, axs = plt.subplots(1, figsize=(10,5))
sns.barplot(data=df_top_people,y='primaryName', x="count", hue='category', ax=axs)
axs.set_xlabel('number of titles')
axs.set_ylabel('')
plt.xticks(rotation=0)
plt.yticks(fontsize=15)
plt.suptitle('Top 5 Numbers of movies per person')
sns.set_style("whitegrid")
plt.show()