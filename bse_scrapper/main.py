import time
import requests
import pandas as pd

from utils import *

if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_profile())
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    driver.get("https://www.bseindia.com/corporates/Sharehold_Searchnew.aspx")
    r = requests.get(url_main, headers=header)

    dfs = pd.read_html(r.text)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))

    print(dfs[4])
    dfs[4].to_csv('main_page_table.csv', index=False)
    time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
