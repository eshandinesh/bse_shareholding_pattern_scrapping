import os
import random
import pandas as pd
import numpy as np

from selenium import webdriver
from functools import reduce
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


DRIVER_PATH = "/home/pc/bse/chromedriver"
url_main = "https://www.bseindia.com/corporates/Sharehold_Searchnew.aspx"
url = "https://www.bseindia.com/corporates/shpSecurities.aspx?scripcd=537573&qtrid=107.00&Flag=New"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

nationality = {
    'A1) Indian': ['Individuals/Hindu undivided Family', 'Central Government/ State Government(s)', 'Any Other (specify)'],
    'A2) Foreign': ['Individuals (NonResident Individuals/ Foreign Individuals)', 'Any Other (specify)', 'None']
}

categories = {
  'B1) Institutions': ['Mutual Funds/', 'Alternate Investment Funds', 'Foreign Portfolio Investors',
                       'Financial Institutions/ Banks', 'Any Other (specify)',
                       'Insurance Companies', 'Financial Institutions/ Banks',
                       'Venture Capital Funds', 'Provident Funds/ Pension Funds'],
  'B2) Central Government/ State Government(s)/ President of India': ['Central Government/ State Government(s)/ President of India',
                                                                      'None', 'None',
                                                                      'None', 'None', 'None',
                                                                      'None', 'None', 'None'],
  'B3) Non-Institutions': ['Individual share capital upto Rs. 2 Lacs',
                           'Individual share capital in excess of Rs. 2 Lacs',
                           'NBFCs registered with RBI', 'Employee Trusts', 'Any Other (specify)',
                           'None', 'None', 'None', 'None'],
}


def get_nationality_category_promoter(df):
    cols = list(df['Category of shareholder'])
    for col in cols:
        if str(col).find('\xa0'):
            cols[cols.index(col)] = ' '.join(str(col).split('\xa0'))
    temp_list = [None]*df['Category of shareholder'].shape[0]
    temp_cate_list = [None] * df['Category of shareholder'].shape[0]

    try:
        temp_list[cols.index(list(nationality.keys())[0])] = str(list(nationality.keys())[0]).split(' ')[1]
        temp_cate_list[cols.index(list(nationality.keys())[0])] = str(list(nationality.keys())[0]).split(' ')[1]
    except:
        pass
    try:
        temp_list[cols.index(list(nationality.keys())[1])] = str(list(nationality.keys())[1]).split(' ')[1]
        temp_cate_list[cols.index(list(nationality.keys())[1])] = str(list(nationality.keys())[1]).split(' ')[1]
    except:
        pass

    for i in range(2):
        for j in range(2):
            try:
                temp_cate_list[cols.index(list(nationality.values())[i][j])] = cols[cols.index(list(nationality.values())[i][j])]
                # temp_cate_list[cols.index(list(nationality.values())[i][j])] = str(list(nationality.values())[i][j])
            except:
                continue

    for element in temp_list:
        if element is not None:
            continue
        else:
            temp_list[temp_list.index(element)] = temp_list[temp_list.index(element)-1]

    for element in temp_cate_list:
        if element is not None:
            continue
        else:
            temp_cate_list[temp_cate_list.index(element)] = temp_cate_list[temp_cate_list.index(element) - 1]
    return temp_list, temp_cate_list


def get_nationality_category_public(df):
    cols = list(df['Category & Name of the Shareholders'])
    for col in cols:
        if str(col).find('\xa0'):
            cols[cols.index(col)] = ' '.join(str(col).split('\xa0'))
    temp_list = [None]*df['Category & Name of the Shareholders'].shape[0]
    temp_cate_list = [None] * df['Category & Name of the Shareholders'].shape[0]
    try:
        temp_list[cols.index(list(categories.keys())[0])] = str(list(categories.keys())[0]).split(') ')[1]
        temp_cate_list[cols.index(list(categories.keys())[0])] = str(list(categories.keys())[0]).split(') ')[1]
    except:
        pass
    try:
        temp_list[cols.index(list(categories.keys())[1])] = str(list(categories.keys())[1]).split(') ')[1]
        temp_cate_list[cols.index(list(categories.keys())[1])] = str(list(categories.keys())[1]).split(') ')[1]
    except:
        pass
    try:
        temp_list[cols.index(list(categories.keys())[2])] = str(list(categories.keys())[2]).split(') ')[1]
        temp_cate_list[cols.index(list(categories.keys())[2])] = str(list(categories.keys())[2]).split(') ')[1]
    except:
        pass

    temp_col = reduce(lambda x,y:x+y, list(categories.values()))
    indices = [{i:x} for i, x in enumerate(cols) if x in temp_col]

    try:
        for index in indices:
            temp_cate_list[list(index.keys())[0]] = list(index.values())[0]
    except:
        pass

    for element in temp_list:
        if element is not None:
            continue
        else:
            temp_list[temp_list.index(element)] = temp_list[temp_list.index(element)-1]

    for element in temp_cate_list:
        if element is not None:
            continue
        else:
            temp_cate_list[temp_cate_list.index(element)] = temp_cate_list[temp_cate_list.index(element) - 1]
    return temp_list, temp_cate_list


def add_details_in_headers_with_noentries():
    os.chdir(os.getcwd())
    df = pd.read_csv('final.csv')
    index = df.index[df[df.columns.values[-1]].apply(np.isnan)]
    df = df.drop(index)
    temp_col = reduce(lambda x, y: x + y, list(categories.values()))
    cols = list(df['Category of shareholder'])
    i = 0
    for _ in range(len(cols)):
        if i >= len(cols):
            break
        elif cols[i] in temp_col and cols[i+1] in temp_col:
            Filter_df = df[df.index.isin([i])]
            # Filter_df.loc[i, df.columns.get_loc('Category of shareholder')] = cols[i] + '_details'
            df = pd.concat([df.iloc[:i], Filter_df, df.iloc[i:]]).reset_index(drop=True)
            df.loc[i+1, 'Category of shareholder'] = cols[i] + '_details'
            cols.insert(i, cols[i])
            i = i + 2
        else:
            i = i + 1
    header_list = []
    for i in range(df.shape[0]):
        if df.loc[i, 'Category'] in df.loc[i, 'Category of shareholder']:
            header_list.append(1)
        else:
            header_list.append(0)
    df.insert(loc=9, column='Header', value=header_list)
    index = df.index[df[df.columns.values[-1]].apply(np.isnan)]
    df = df.drop(index)
    df = df[df.columns.values[2:]]
    df.to_csv('updated_final.csv', index=False)


def browser_profile():
    driver = webdriver.ChromeOptions()
    driver.add_argument("--start-maximized")
    driver.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    driver.to_capabilities()
    return driver


def get_random_wait(initial_limit=1, upper_limit=5):
    return random.randint(initial_limit, upper_limit)