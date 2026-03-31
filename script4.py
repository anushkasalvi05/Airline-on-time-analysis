#%%
import yfinance as yf
import pandas as pd
from tabulate import tabulate

#%%
stocks = ['AAPL', 'ORCL', 'TSLA', 'IBM', 'YELP', 'MSFT']
stk_start_date = '2013-01-01'
stk_end_date = '2024-05-22'

#%%
df = yf.download(stocks, start=stk_start_date, end=stk_end_date, auto_adjust=False, group_by='ticker')

#%%
#features
columns_names_table = ["High", "Low", "Open", "Close", "Volume", "Adj Close"]

#%%
#fucntion creation
def table_design(math_type, title):
    empty_stock_list = []

    for ticker in stocks:
        values = getattr(df[ticker][columns_names_table], math_type)().round(2)
        empty_stock_list.append([ticker] + values.tolist())
        #in the above block getattr is used to dynamically call the method on our stock dta.
        #this data is stored in empty_stock_list
        #and temporary storied in df2
    #min-max values now
    df2 = pd.DataFrame([r[1:] for r in empty_stock_list], columns = columns_names_table, index = stocks)
    #heps to calculate summaray statistcs and min max values for each company
    min_max_stock_val = [
        ["Maximum Value"] + df2.max().tolist(),
        ["Minimum Value"] + df2.min().tolist(),
        ["Maximum company name"] + df2.idxmax().tolist(),
        ["Minimum company name"] + df2.idxmin().tolist()
    ]

    final_table_create = empty_stock_list + min_max_stock_val
    stock_table_header = ["Name / Feature"] + columns_names_table
    print(f"\n{title}")
    print(tabulate(final_table_create, headers = stock_table_header, tablefmt = "grid", floatfmt = ".2f"))

#%%
#calling the func
#all stats methods are called......mean,var,std and var
table_design('mean', "                            Mean Value Comparison")
table_design('var', "                             Varaiance Comparison")
table_design('std', "                             Standard Deviation Comparison")
table_design('median', "                          Median Comparison")



#%%
#correlation for APPLE
apple_stock_info = df['AAPL'][columns_names_table]
correlation_apple = apple_stock_info.corr().round(2)
print("\n                      Correlation Matrix for Apple (AAPL): ")
print(tabulate(correlation_apple, headers = columns_names_table, tablefmt = "grid"))


#%%
#all other companies
other_comp_stocks = ['ORCL', 'TSLA', 'IBM', 'YELP', 'MSFT']
for xyz in other_comp_stocks:
    company_stock_info = df[xyz]
    correlation_matrx = company_stock_info.corr().round(2)

    print(f"\n                Correlation Matrix for {xyz}:")
    print(tabulate(correlation_matrx, headers = columns_names_table, tablefmt = "grid"))



#%%
#volatality using standard dev
stdev_volatility_comp = []
for a in stocks:
    volatile_comp = df[a]['Adj Close'].std()
    stdev_volatility_comp.append([a, round(volatile_comp, 2)])

stdev_volatility_comp.sort(key = lambda x: x[1])
print("                       Volatility Comparison: \n")
print(tabulate(stdev_volatility_comp, headers = columns_names_table, tablefmt = "grid"))


