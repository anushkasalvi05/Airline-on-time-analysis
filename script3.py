#%%
import yfinance as yf
import pandas as pd
from tabulate import tabulate

#%%

stocks = ['AAPL', 'ORCL', 'TSLA', 'IBM', 'YELP', 'MSFT']
start_date = '2013-01-01'               #parameter as per instructions
end_date = '2024-05-22'

df = yf.download(stocks, start=start_date, end=end_date, auto_adjust=False, group_by='ticker')
#as we need to calculate average/variance going forward betetr to use ticker so that it sorts by company name. Apple, Tesla....


data_mean = []

for ticker in stocks:
    stock_mean = df[ticker].mean().round(2)
    row = [ticker] + stock_mean.tolist()
    data_mean.append(row)                             #this block of code calculates mean for each company

column_names = ["High($)", "Low($)", "Open($)", "Close($)", "Volume", "Adj Close($)"]
new_mean_df = pd.DataFrame([r[1:] for r in data_mean], columns=column_names, index=stocks)             #this block starts from numbers rather than taking in account the name of the company

#this block of code finds the maximum and minim values and adding it to list and adding title to those vlaues
maximum_value = ["Maximum Value"] + new_mean_df.max().tolist()
minimum_values = ["Minimum Value"] + new_mean_df.min().tolist()
maximum_company = ["Maximum company name"] + new_mean_df.idxmax().tolist()
minimum_company = ["Minimum company name"] + new_mean_df.idxmin().tolist()

final_table_design = data_mean + [maximum_value, minimum_values, maximum_company, minimum_company]
headers = ["Name / Feature"] + column_names

print("\n                                                  Mean Value Comparison")
print(tabulate(final_table_design, headers=headers, tablefmt="pretty", floatfmt=".2f"))


#%%
#variance comparison
data_var = []

for ticker in stocks:
    stock_var = df[ticker].var().round(2)
    row = [ticker] + stock_var.tolist()
    data_var.append(row)                    #calculates variance for each company (for loop)

column_names = ["High($)", "Low($)", "Open($)", "Close($)", "Volume", "Adj Close($)"]

new_variance_df = pd.DataFrame([r[1:] for r in data_var], columns=column_names, index=stocks)             #this block starts from var calc rather than taking in account the name of the company

#this block of code finds the maximum and minim values and adding it to list and adding title to those vlaues
maximum_var_value = ["Maximum Value"] + new_variance_df.max().tolist()
minimum_var_values = ["Minimum Value"] + new_variance_df.min().tolist()
maximum_var_company = ["Maximum company name"] + new_variance_df.idxmax().tolist()
minimum_var_company = ["Minimum company name"] + new_variance_df.idxmin().tolist()

final_table_design1 = data_var + [maximum_var_value, minimum_var_values, maximum_var_company, minimum_var_company]
headers = ["Name / Feature"] + column_names

print("\n                                                  Variance Comparison")
print(tabulate(final_table_design1, headers=headers, tablefmt="pretty", floatfmt=".2f"))


#%%
#standard deviation
data_std = []

for ticker in stocks:
    stock_std = df[ticker].std().round(2)                 #calculates std
    row = [ticker] + stock_std.tolist()
    data_std.append(row)

column_names = ["High($)", "Low($)", "Open($)", "Close($)", "Volume", "Adj Close($)"]

new_stdev_df = pd.DataFrame([r[1:] for r in data_std], columns=column_names, index=stocks)             #this block starts from std calc rather than taking in account the name of the company

#this block of code finds the maximum and minim values and adding it to list and adding title to those vlaues
maximum_std_value = ["Maximum Value"] + new_stdev_df.max().tolist()
minimum_std_values = ["Minimum Value"] + new_stdev_df.min().tolist()
maximum_std_company = ["Maximum company name"] + new_stdev_df.idxmax().tolist()
minimum_std_company = ["Minimum company name"] + new_stdev_df.idxmin().tolist()

final_table_design2 = data_std + [maximum_std_value, minimum_std_values, maximum_std_company, minimum_std_company]
headers = ["Name / Feature"] + column_names

print("\n                                                  Standard Deviation Comparison")
print(tabulate(final_table_design2, headers=headers, tablefmt="pretty", floatfmt=".2f"))


#%%
#median compariso
median_comp = []

for ticker in stocks:
    stock_median = df[ticker].median().round(2)                 #shows median which is the mid-point
    row = [ticker] + stock_median.tolist()
    median_comp.append(row)

column_names = ["High($)", "Low($)", "Open($)", "Close($)", "Volume", "Adj Close($)"]

new_median_df = pd.DataFrame([r[1:] for r in median_comp], columns=column_names, index=stocks)             #this block starts from med calc rather than taking in account the name of the company

#this block of code finds the maximum and minim values and adding it to list and adding title to those vlaues
maximum_median = ["Maximum Value"] + new_median_df.max().tolist()
minimum_median = ["Minimum Value"] + new_median_df.min().tolist()
maximum_med_company = ["Maximum company name"] + new_median_df.idxmax().tolist()
minimum_med_company = ["Minimum company name"] + new_median_df.idxmin().tolist()

final_table_design3 = median_comp + [maximum_median, minimum_median, maximum_med_company, minimum_med_company]
headers = ["Name / Feature"] + column_names

print("\n                                                  Median Comparison")
print(tabulate(final_table_design3, headers=headers, tablefmt="pretty", floatfmt=".2f"))


#%%
#correlation for APPLE

apple_info = df['AAPL']

corr_apple = apple_info.corr().round(2)

print("\n                      Correlation Matrix for Apple (AAPL): ")
print(tabulate(corr_apple, headers=headers, tablefmt="pretty"))

#%%
#Q7
#all other companies
other_stocks = ['ORCL', 'TSLA', 'IBM', 'YELP', 'MSFT']

for i in other_stocks:
    company_info = df[i]
    correlation_mx = company_info.corr().round(2)

    print(f"\n                Correlation Matrix for {i}:")
    print(tabulate(correlation_mx, headers=headers, tablefmt="pretty"))



#%%
#volatality using standard dev

stdev_volatility = []

for a in stocks:
    volatility = df[a]['Adj Close'].std()
    stdev_volatility.append([a, round(volatility, 2)])

stdev_volatility.sort(key=lambda x: x[1])

print("\n Volatility Comparison:")
print(tabulate(stdev_volatility, headers=headers, tablefmt="pretty"))



