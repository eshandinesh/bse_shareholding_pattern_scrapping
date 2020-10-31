import time
import requests
import pandas as pd

from utils import *


def scrapping_jobs(quarter_link, driver, scrip_code, scrip_name):
    quarter_link.click()
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))

    """
    Shareholding pattern scrapping
    """

    r = requests.get(driver.current_url, headers=header)
    dfs = pd.read_html(r.text)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    temp_df = dfs[4][[0, 1, 3]]
    temp_df.columns = temp_df.iloc[0]
    temp_df = temp_df.iloc[3:-1]
    temp_df.insert(loc=0, column='Scrip_code', value=[scrip_code]*temp_df.shape[0])
    temp_df.insert(loc=1, column='Company', value=[scrip_name]*temp_df.shape[0])
    temp_df.insert(loc=2, column='Quarter', value=[str(dfs[2][3][1]).split(':')[-1]]*temp_df.shape[0])
    temp_df.to_csv('shareholding_pattern_{}_{}.csv'.format(scrip_name, str(dfs[2][3][1]).split(':')[-1]), index=False)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))

    """
    Promoter shareholding pattern scrapping
    """

    promoter_link = driver.find_element_by_xpath('//table[@class="tbmain"]/tbody/tr[1]/td/a')
    promoter_url = "https://www.bseindia.com/corporates/" + str(promoter_link.get_attribute('onclick')).split('"')[1]
    promoter_r = requests.get(promoter_url, headers=header)
    promoter_df = pd.read_html(promoter_r.text)
    temp_promoter_df = promoter_df[3]
    temp_promoter_df.columns = temp_promoter_df.iloc[0]
    temp_promoter_df = temp_promoter_df.iloc[3:]
    temp_promoter_df.insert(loc=0, column='Scrip_code', value=[scrip_code] * temp_promoter_df.shape[0])
    temp_promoter_df.insert(loc=1, column='Company', value=[scrip_name] * temp_promoter_df.shape[0])
    temp_promoter_df.insert(loc=2, column='Quarter', value=[str(dfs[2][3][1]).split(':')[-1]] * temp_promoter_df.shape[0])
    temp_promoter_df.to_csv(
        'promoter_shareholding_pattern_{}_{}.csv'.format(scrip_name, str(dfs[2][3][1]).split(':')[-1]), index=False)

    """
    Public shareholding pattern scrapping
    """

    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    public_link = driver.find_element_by_xpath('//table[@class="tbmain"]/tbody/tr[2]/td/a')
    public_url = "https://www.bseindia.com/corporates/" + str(public_link.get_attribute('onclick')).split('"')[1]
    public_r = requests.get(public_url, headers=header)
    public_df = pd.read_html(public_r.text)
    temp_public_df = public_df[3]
    temp_public_df.columns = temp_public_df.iloc[0]
    temp_public_df = temp_public_df.iloc[6:]
    temp_public_df.insert(loc=0, column='Scrip_code', value=[scrip_code] * temp_public_df.shape[0])
    temp_public_df.insert(loc=1, column='Company', value=[scrip_name] * temp_public_df.shape[0])
    temp_public_df.insert(loc=2, column='Quarter',
                            value=[str(dfs[2][3][1]).split(':')[-1]] * temp_public_df.shape[0])
    temp_public_df.to_csv(
        'public_shareholding_pattern_{}_{}.csv'.format(scrip_name, str(dfs[2][3][1]).split(':')[-1]), index=False)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


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
    scrip_name = "CAMLIN FINE SCIENCES LTD"
    scrip_code = 532834

    input_security = driver.find_element_by_xpath('//input[@class="textbox2"]')
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    input_security.click()
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    input_security.send_keys("CAMLIN FINE SCIENCES LTD")
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    select_security = driver.find_element_by_xpath('//div[@id="ajax_response_smart"]/ul/li')
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    select_security.click()
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    period = driver.find_element_by_xpath('//option[text()="Last 1 year"]')
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    period.click()
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    submit = driver.find_element_by_xpath('//input[@value="Submit"]')
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    submit.click()
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    base_url = driver.current_url
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    for i in range(1, 5):
        i = i+1
        quarter_link = driver.find_element_by_xpath('//table[@class="mGrid"]/tbody/tr[{}]/td[4]/a'.format(i))
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        scrapping_jobs(quarter_link, driver, scrip_code, scrip_name)

