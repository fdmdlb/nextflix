import pandas as pd

df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
print('Top 10 in number of media translated')
print(df_top10number)
print()

print('Top 10 in number of minutes translated')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')
print(df_top10minutes)

