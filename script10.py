#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Q1
URL = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/refs/heads/main/mnist_test.csv"
df = pd.read_csv(URL)
print(df.shape)

#%%
#Q1.A
df_filtered = df[df['label'].isin(range(10))]
plt.figure(figsize=(12,12))

for i in range(100):
    pic = df_filtered.iloc[i, 1:].values.reshape(28, 28)
    plt.subplot(10,10,i+1)
    plt.imshow(pic)
    plt.axis('off')


plt.tight_layout()
plt.show()


#%%
#Q1.B



#%%
#Q2

import seaborn as sns

diamond = sns.load_dataset("diamonds")
print(diamond.head(5))
print(diamond.columns.values)    #column names

print(diamond.isna().sum())      #missing values sum

#%%
new_cleaned = diamond.dropna()      #dropping if any and new dataframe
sns.set_style("whitegrid")

print(new_cleaned.head(5))

#%%
from prettytable import PrettyTable
unique_cuts = new_cleaned['cut'].unique()
cut_table = PrettyTable()
cut_table.field_names = ['Number', 'Cut Name']
for i, cut in enumerate(unique_cuts, 1):
    cut_table.add_row([i, cut])
print("Diamond Dataset - Various Cuts")
print(cut_table)




#%%
from prettytable import PrettyTable
unique_colors = new_cleaned['color'].unique()
color_table = PrettyTable()
color_table.field_names = ['Number', 'Color Name']

for i, color in enumerate(unique_colors, 1):
    color_table.add_row([i, color])
print("Diamond Dataset - Various Colors")
print(color_table)



#%%
from prettytable import PrettyTable

unique_clarity = new_cleaned['clarity'].unique()
clarity_table = PrettyTable()
clarity_table.field_names = ['Number', 'Clarity Name']

for i, clarity in enumerate(unique_clarity, 1):
    clarity_table.add_row([i, clarity])

print("Diamond Dataset - Various Clarities")
print(clarity_table)




#%%
#Q6
sales_for_each_cut = new_cleaned['cut'].value_counts()

plt.figure(figsize=(10, 7))
sales_for_each_cut.plot(
    kind='barh',
    color='#95DEE3',
    edgecolor='red',
    linewidth=2
)

for i, v in enumerate(sales_for_each_cut):
    plt.text(v + 0.05, i, str(v), va='center', fontsize=10)

plt.title('Sales Count per Cut', fontsize=12)
plt.xlabel('Number of Sales for each cut category', fontsize=10)
plt.ylabel('Cut Category', fontsize=10)
plt.grid(True, axis='x')
plt.grid(True, axis='y')
plt.gca().invert_yaxis()        #in descendig
plt.tight_layout()
plt.show()

maximum_cut_sales = sales_for_each_cut.idxmax()
minimum_cut_sales = sales_for_each_cut.idxmin()

print(f"The diamond with {maximum_cut_sales} cut has the maximum number of sales.")
print(f"The diamond with {minimum_cut_sales} cut has the minimum number of sales.")


#%%
#Q7
sales_for_each_color = new_cleaned['color'].value_counts()

plt.figure(figsize=(10, 7))
sales_for_each_color.plot(
    kind='barh',
    color='#95DEE3',
    edgecolor='red',
    linewidth=2
)

for i, v in enumerate(sales_for_each_color):
    plt.text(v + 0.05, i, str(v), va='center', fontsize=10)

plt.title('Sales Count per Color', fontsize=12)
plt.xlabel('Number of Sales for each color category', fontsize=10)
plt.ylabel('Color Category', fontsize=10)
plt.grid(True, axis='x')
plt.grid(True, axis='y')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

maximum_color_sales = sales_for_each_color.idxmax()
minimum_color_sales = sales_for_each_color.idxmin()

print(f"The diamond with {maximum_color_sales} color has the maximum number of sales.")
print(f"The diamond with {minimum_color_sales} color has the minimum number of sales.")



#%%
#Q8
sales_for_each_clarity = new_cleaned['clarity'].value_counts()

plt.figure(figsize=(10, 7))
sales_for_each_clarity.plot(
    kind='barh',
    color='#95DEE3',
    edgecolor='red',
    linewidth=2
)

for i, v in enumerate(sales_for_each_clarity):
    plt.text(v + 0.05, i, str(v), va='center', fontsize=10)

plt.title('Sales Count per Clarity', fontsize=12)
plt.xlabel('Number of Sales for each clarity category', fontsize=10)
plt.ylabel('Clarity Category', fontsize=10)
plt.grid(True, axis='x')
plt.grid(True, axis='y')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

maximum_clarity_sales = sales_for_each_clarity.idxmax()
minimum_clarity_sales = sales_for_each_clarity.idxmin()
print(f"The diamond with {maximum_clarity_sales} clarity has the maximum number of sales.")
print(f"The diamond with {minimum_clarity_sales} clarity has the minimum number of sales.")


















