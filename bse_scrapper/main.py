import os
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
    temp_promoter_df = temp_promoter_df.iloc[3:-2]
    nationality_list, category_list = get_nationality_category_promoter(temp_promoter_df)
    temp_promoter_df.insert(loc=0, column='Scrip_code', value=[scrip_code] * temp_promoter_df.shape[0])
    temp_promoter_df.insert(loc=1, column='Company', value=[scrip_name] * temp_promoter_df.shape[0])
    temp_promoter_df.insert(loc=2, column='Quarter', value=[str(dfs[2][3][1]).split(':')[-1]] * temp_promoter_df.shape[0])
    temp_promoter_df.insert(loc=3, column='Nationality', value=nationality_list)
    temp_promoter_df.insert(loc=4, column='Category', value=category_list)
    final_df = temp_promoter_df[['Scrip_code', 'Company', 'Quarter', 'Nationality', 'Category',
                                 'Category of shareholder', 'Nos. of shareholders', 'Total nos. shares held']]
    try:
        delete_row = final_df[final_df['Category of shareholder']=='Sub Total A1'].index
        final_df = final_df.drop(delete_row)
    except:
        pass

    # final_df.dropna()
    try:
        delete_row_na = final_df[final_df['Total nos. shares held'] is None].index
        final_df = final_df.drop(delete_row_na)
    except:
        pass
    os.chdir(pro_dir_path)
    final_df.to_csv(
        'promoter_shareholding_pattern_{}_{}.csv'.format(scrip_name, str(dfs[2][3][1]).split(':')[-1]), index=False)
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

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
    temp_public_df = temp_public_df.iloc[6:-5]
    institution_list, category_list = get_nationality_category_public(temp_public_df)
    temp_public_df.insert(loc=0, column='Scrip_code', value=[scrip_code] * temp_public_df.shape[0])
    temp_public_df.insert(loc=1, column='Company', value=[scrip_name] * temp_public_df.shape[0])
    temp_public_df.insert(loc=2, column='Quarter',
                            value=[str(dfs[2][3][1]).split(':')[-1]] * temp_public_df.shape[0])
    temp_public_df.insert(loc=3, column='Nationality', value=institution_list)
    temp_public_df.insert(loc=4, column='Category', value=category_list)
    final_df = temp_public_df[['Scrip_code', 'Company', 'Quarter', 'Nationality', 'Category',
                                 'Category & Name of the Shareholders', 'No. of shareholder',
                                 'Total no. shares held']]
    try:
        delete_row_1 = final_df[final_df['Category & Name of the Shareholders'] == 'Sub Total B1'].index
        final_df = final_df.drop(delete_row_1)
    except:
        pass

    try:
        delete_row_2 = final_df[final_df['Category & Name of the Shareholders'] == 'Sub Total B2'].index
        final_df = final_df.drop(delete_row_2)
    except:
        pass

    try:
        delete_row_3 = final_df[final_df['Category & Name of the Shareholders'] == 'Sub Total B3'].index
        final_df = final_df.drop(delete_row_3)
    except:
        pass

    final_df.rename(columns={'Category & Name of the Shareholders': 'Category of shareholder',
                             'No. of shareholder': 'Nos. of shareholders',
                             'Total no. shares held': 'Total nos. shares held'},
                    inplace=True)

    # final_df.dropna()
    try:
        delete_row_na = final_df[final_df['Total nos. shares held'] is None].index
        final_df = final_df.drop(delete_row_na)
    except:
        pass
    os.chdir(pub_dir_path)
    final_df.to_csv(
        'public_shareholding_pattern_{}_{}.csv'.format(scrip_name, str(dfs[2][3][1]).split(':')[-1]), index=False)
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
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

    scrips = ['INFOSYS LTD']
    codes = ['500209']

    # scrips = ['CAMLIN FINE SCIENCES LTD', 'AARTI DRUGS LTD', 'APOLLO HOSPITALS ENTERPRISE LTD',
    #           'RELIANCE INDUSTRIES LTD', 'STATE BANK OF INDIA']
    # codes = ['532834', '524348', '508869', '500325', '500112']

    pre_final_dir = 'pre_final'
    pre_final_dir_path = os.path.join(os.getcwd(), pre_final_dir)
    if not os.path.exists(pre_final_dir_path):
        os.makedirs(pre_final_dir_path)

    for scrip_name, scrip_code in zip(scrips, codes):
        # scrip_name = "APOLLO HOSPITALS ENTERPRISE LTD"
        # scrip_code = 508869
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        driver.get("https://www.bseindia.com/corporates/Sharehold_Searchnew.aspx")

        pub_dir, pro_dir = scrip_name + '_public', scrip_name + '_promoter'
        pub_dir_path, pro_dir_path = os.path.join(os.getcwd(), pub_dir), os.path.join(os.getcwd(), pro_dir)
        if not os.path.exists(pro_dir_path):
            os.makedirs(pro_dir_path)

        if not os.path.exists(pub_dir_path):
            os.makedirs(pub_dir_path)

        input_security = driver.find_element_by_xpath('//input[@class="textbox2"]')
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        input_security.click()
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        input_security.send_keys(scrip_name)
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
        for i in range(1, 7):
            i = i+1
            try:
                quarter_link = driver.find_element_by_xpath('//table[@class="mGrid"]/tbody/tr[{}]/td[4]/a'.format(i))
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                scrapping_jobs(quarter_link, driver, scrip_code, scrip_name)
            except:
                continue

        li = []
        os.chdir(pro_dir_path)
        for f in os.listdir(pro_dir_path):
            li.append(pd.read_csv(f))
        os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

        os.chdir(pub_dir_path)
        for f in os.listdir(pub_dir_path):
            li.append(pd.read_csv(f))
        os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

        frame = pd.concat(li, axis=0, ignore_index=True)
        os.chdir(pre_final_dir_path)
        frame.to_csv('final_{}.csv'.format(scrip_name))
        os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

    list = []
    os.chdir(pre_final_dir_path)
    for f in os.listdir(pre_final_dir_path):
        list.append(pd.read_csv(f))
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

    frame = pd.concat(list, axis=0, ignore_index=True)
    frame.to_csv('final.csv')
    add_details_in_headers_with_noentries()
