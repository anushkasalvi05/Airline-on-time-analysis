#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable

np.random.seed(6401)

x=PrettyTable()
name1 = ['Index']
name2 = [f"A{i}" for i in range(1,16)]
x.field_names = name1 + name2
data = np.random.rand(6,15)
df = pd.DataFrame(data.round(2), columns = name2, index = [f"{i}" for i in range(1,7)])
df.reset_index(inplace = True)
for i in range(6):
    x.add_row(df.iloc[i,:])
print(x.get_string(title = 'dummy dataset'))

#%%
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
print(tips.head())

print(f"{tips['sex'].value_counts()}")

tip_sex_count = tips.loc[:,['sex','tip']].groupby(['sex']).count()
tip_sex_count.reset_index(inplace = True)

tip_sex_count.columns = ['sex','count']
print(tip_sex_count)


ax = tip_sex_count.plot(kind='bar', x='sex', y='count', title="count bar plot", grid=True, fontsize=10, xlabel='gender', ylabel='count')

for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+ 0.5, int(bar.get_height), ha='center', va='bottom', fontsize=15)
plt.tight_layout()
plt.show()

#%%
url = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/refs/heads/main/nba.csv"
df = pd.read_csv(url)
print(df.head())
df.columns



#%%


