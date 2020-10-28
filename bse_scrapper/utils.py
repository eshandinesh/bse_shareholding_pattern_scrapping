import random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


DRIVER_PATH = "/home/pc/bse/chromedriver"
url_main = "https://www.bseindia.com/corporates/Sharehold_Searchnew.aspx"
url = "https://www.bseindia.com/corporates/shpSecurities.aspx?scripcd=537573&qtrid=107.00&Flag=New"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}



def browser_profile():
    driver = webdriver.ChromeOptions()
    driver.add_argument("--start-maximized")
    driver.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    driver.to_capabilities()
    return driver


def get_random_wait(initial_limit=1, upper_limit=5):
    return random.randint(initial_limit, upper_limit)