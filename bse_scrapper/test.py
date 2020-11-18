import pandas as pd
import os

dabur=pd.read_csv("/home/pc/bse/bse_shareholding_pattern_scrapping/bse_scrapper/updated_final.csv")
print(dabur[dabur['Category'].isin(['Mutual Funds/'])][['Quarter','Nos. of shareholders','Total nos. shares held']])
print(dabur[dabur['Category'].isin(['Alternate Investment Funds'])][['Quarter','Nos. of shareholders','Total nos. shares held']])
print(dabur[dabur['Category'].isin(['Foreign Portfolio Investors'])][['Quarter','Nos. of shareholders','Total nos. shares held']])
print(dabur[dabur['Category'].isin(['Financial Institutions/ Banks'])][['Quarter','Nos. of shareholders','Total nos. shares held']])
print(dabur[dabur['Category'].isin(['Insurance Companies'])][['Quarter','Nos. of shareholders','Total nos. shares held']])
print(dabur[dabur['Category'].isin(['Venture Capital Funds'])][['Quarter','Nos. of shareholders','Total nos. shares held']])
print(dabur[dabur['Category'].isin(['Provident Funds/ Pension Funds'])][['Quarter','Nos. of shareholders','Total nos. shares held']])