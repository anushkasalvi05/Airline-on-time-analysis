#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

github_url = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/main/Sample%20-%20Superstore.xls"

df = pd.read_excel(github_url)
print(df.head())

#%%
print(df.columns)


#%%
drop_given_columns = [
    'Row ID', 'Order ID', 'Customer ID',
    'Customer Name', 'Postal Code', 'Product ID',
    'Order Date', 'Ship Date', 'Country', 'Segment'
]

clean_df = df.drop(columns=drop_given_columns)

pd.set_option('display.float_format', '{:.2f}'.format)

print(clean_df.head())

#%%
print(clean_df.columns)

#%%
group_cat = clean_df.groupby('Category').sum(numeric_only=True)

metrics_dict = {
    "Total Profit" : group_cat['Profit'],
    "Total Discount" : group_cat['Discount'],
    "Total Quantity" : group_cat['Quantity'],
    "Total Sales" : group_cat['Sales']
}

fig, ax = plt.subplots(2,2, figsize=(18,18))
ax = ax.flatten()

for i, (key, value) in enumerate(metrics_dict.items()):
    cat = value.index
    total = value.values

    maximum_cat = value.idxmax()
    minimum_cat = value.idxmin()

    print(f"{key}")
    print(f"Maximum Category: {maximum_cat}")
    print(f"Minimum Category: {minimum_cat}\n")

    explode = [0.1 if c == minimum_cat else 0 for c in cat]

    #pie chart now
    ax[i].pie(
        total,
        explode=explode,
        labels=cat,
        autopct = "%1.2f%%",
        textprops = {'fontsize': 30}
    )

    ax[i].set_title(
        key,
        fontfamily = 'serif',
        color = 'blue',
        fontsize = 35
    )

plt.tight_layout()
plt.show()

#%%
print(ales.index)
#%%
#table design q3
group_cat = clean_df.groupby('Category').sum(numeric_only=True)
sales = group_cat['Sales']
quantity = group_cat['Quantity']
discount = group_cat['Discount']
profit = group_cat['Profit']

table_design = []

for cat in group_cat.index:
    table_design.append([
        cat,
        f"{sales[cat]:.2f}",
        f"{quantity[cat]:.2f}",
        f"{discount[cat]:.2f}",
        f"{profit[cat]:.2f}"
    ])

table_design.append([
    "Maximum Value",
    f"{sales.max():.2f}",
    f"{quantity.max():.2f}",
    f"{discount.max():.2f}",
    f"{profit.max():.2f}"
])

table_design.append([
    "Minimum Value",
    f"{sales.min():.2f}",
    f"{quantity.min():.2f}",
    f"{discount.min():.2f}",
    f"{profit.min():.2f}"
])

table_design.append([
    "Maximum Feature",
    sales.idxmax(),
    quantity.idxmax(),
    discount.idxmax(),
    profit.idxmax()
])

table_design.append([
    "Minimum Feature",
    sales.idxmin(),
    quantity.idxmin(),
    discount.idxmin(),
    profit.idxmin()
])

column_names = ["Category", "Sales($)", "Quantity", "Discount($)", "Profit($)"]

fig, ax = plt.subplots(figsize=(22,10))     #tried figsize 18,8 and 15,5 and other variations but the border kept getting cut
ax.axis('off')

table1 = ax.table(
    cellText = table_design,
    colLabels = column_names,
    loc = 'center',
    cellLoc = 'center'
)

table1.auto_set_font_size(False)
table1.set_fontsize(14)
table1.scale(1.2, 2)

plt.title("Super Store - Category Summary", fontsize = 30, fontweight = 'bold')

plt.show()


#%%
#q4
sub_cat_group = clean_df.groupby('Sub-Category').sum(numeric_only=True)

categories_specified = [
    'Phones', 'Chairs', 'Storage', 'Tables',
    'Binders', 'Machines', 'Accessories',
    'Copiers', 'Bookcases', 'Appliances'
]

sub_cat_group = sub_cat_group.loc[categories_specified]

sales = sub_cat_group['Sales']
profit = sub_cat_group['Profit']

sales = sales.sort_values(ascending=False)
profit = profit.loc[sales.index]

x = np.arange(len(sales))

fig, ax2 = plt.subplots(figsize=(20,8))

bar_plot = ax2.bar(
    x,
    sales,
    width = 0.4,
    edgecolor = 'blue',
    color = '#95DEE3',
    label = 'Sales'
)

ax2.grid(axis = 'both', linestyle = '--', alpha = 0.6)

ax2.set_xlabel("Sub-Category", fontsize = 25)
ax2.set_ylabel("USD($)", fontsize = 25)

ax2.tick_params(axis='both', labelsize = 20)

ax2.set_xticks(x)
ax2.set_xticklabels(sales.index, rotation = 0, ha = 'center', fontsize = 20)

for b in bar_plot:
    height = b.get_height()
    ax2.text(
        b.get_x() + b.get_width() / 2.0,
        height + 5000,
        f"{height:,.2f}",
        ha = 'center',
        va = 'bottom',
        fontsize = 20,
        rotation = 90
    )

ax3 = ax2.twinx()            #twinx() creates a second y-axis that has the same x-axis
ax3.plot (x,
          profit,
          color='red',
          linewidth=4,
          label = 'Profit'
)

ax3.set_ylabel("USD($)", fontsize = 25)
ax3.tick_params(axis='y', labelsize = 20)

max_limit = max(sales.max(), profit.max())

ax2.set_ylim(-50000, 350000)
ax3.set_ylim(-50000, 350000)

lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax3.get_legend_handles_labels()

ax2.legend(lines1 + lines2, labels1 + labels2, loc = 'upper right', fontsize = 10)

plt.title("Sles and Profit per sub-category", fontsize = 30)
#plt.legend()
plt.tight_layout()
#plt.margins(x = 0.02)
plt.show()


#Without specifying the categories, it was giving all the sub-categories which were making the barplot crowded.


#%%
#q5
x = np.linspace(0, 2*np.pi, 400)

y_sine = np.sin(x)
y_cosine = np.cos(x)

plt.figure(figsize=(8,6))

plt.plot(x, y_sine, linestyle = '--', linewidth = 3, label = 'sine wave')
plt.plot(x, y_cosine, linestyle = '-.', linewidth = 3, label = 'cosine wave')

plt.fill_between(
    x,
    y_sine,
    y_cosine,
    where = (y_sine > y_cosine),
    color = 'green',
    alpha = 0.3
)

plt.fill_between(
    x,
    y_sine,
    y_cosine,
    where = (y_cosine > y_sine),
    color = 'orange',
    alpha = 0.3
)

plt.title('Fill between x-axis and plot line',
          fontdict = {'family' : 'serif',
                      'color' : 'blue',
                      'size' : 20}
)

plt.xlabel('x-axis',
           fontdict = {'family' : 'serif',
                       'color' : 'darkred',
                       'size' : 15
                       })

plt.legend(fontsize = 15)

plt.grid()

plt.annotate('area where sine is greater than cosine',
             xy = (2, 0.2),
             xytext = (3.2, 0.9),
             arrowprops = dict(facecolor='green',
                               shrink = 0.05,
                               width = 1),
             fontsize = 12)

plt.show()


#%%
#q6
from mpl_toolkits.mplot3d import Axes3D

x = np.arange(-4, 4, 0.01)
y = np.arange(-4, 4, 0.01)

X, Y = np.meshgrid(x, y)

Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure(figsize=(10,10))

ax4 = fig.add_subplot(111, projection='3d')

surface_plt = ax4.plot_surface(X, Y, Z, cmap = 'coolwarm', linewidth = 1)

ax4.contour(X, Y, Z,
            zdir = 'z',
            offset = -6,
            cmap = 'coolwarm',
            linewidths = 1)

ax4.contour(X, Y, Z,
            zdir = 'x',
            offset = -4,
            cmap = 'coolwarm',
            linewidths = 1)

ax4.contour(X, Y, Z,
            zdir = 'y',
            offset = 4,
            cmap = 'coolwarm',
            linewidths = 1)


ax4.set_xlim(-4, 4)
ax4.set_ylim(-4, 4)
ax4.set_zlim(-6, 2)

ax4.set_xlabel('X Label',
               fontdict = {'family' : 'serif',
                           'color' : 'darkred',
                           'size' : 15})

ax4.set_ylabel('Y Label',
               fontdict = {'family' : 'serif',
                           'color' : 'darkred',
                           'size' : 15})

ax4.set_zlabel('Z Label',
               fontdict = {'family' : 'serif',
                           'color' : 'darkred',
                           'size' : 15})

ax4.set_title('surface plot of z = sin √(x² + y²)',
               fontdict = {'family' : 'serif',
                           'color' : 'blue',
                           'size' : 25})

plt.show()


#%%
#q7
sub_cat_group = clean_df.groupby('Sub-Category').sum(numeric_only=True)

categories_specified = [
    'Phones', 'Chairs', 'Storage', 'Tables',
    'Binders', 'Machines', 'Accessories',
    'Copiers', 'Bookcases', 'Appliances'
]

sub_cat_group = sub_cat_group.loc[categories_specified]

sales = sub_cat_group['Sales']
profit = sub_cat_group['Profit']

group_cat = clean_df.groupby('Category').sum(numeric_only=True)

sales_category = group_cat['Sales']
profit_category = group_cat['Profit']

fig = plt.figure(figsize=(9,7))

ax5 = fig.add_subplot(2,1,1)

x = np.arange(len(categories_specified))

width = 0.4

ax5.bar(x - width/2, sales,
        width = 0.4,
        color = '#95DEE3',
        edgecolor = 'blue',
        label = 'Sales')

ax5.bar(x + width/2, profit,
        width = 0.4,
        color = 'lightcoral',
        edgecolor = 'red',
        label = 'Profit')

ax5.set_xticks(x)
ax5.set_xticklabels(categories_specified, fontsize = 10)
ax5.set_ylabel("USD($)", fontsize = 10)
ax5.set_title("Sales and Profit per Sub_category", fontsize = 15)

ax5.legend(fontsize = 10)
ax5.grid(True)

#piechart at bottom
ax6 = fig.add_subplot(2,2,3)
ax7 = fig.add_subplot(2,2,4)

ax6.pie(sales_category,
        labels = sales_category.index,
        autopct = '%1.2f%%'
        )
ax6.set_title("Sales", fontsize = 15)

ax7.pie(profit_category,
        labels = profit_category.index,
        autopct = '%1.2f%%'
        )
ax7.set_title("Profit", fontsize = 15)

plt.tight_layout()
plt.show()