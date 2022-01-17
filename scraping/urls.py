import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

driver = None
HOME_URL = r'https://www.wissports.net/page/show/6397536-teams-2021-' # for 2021 boys season

def set_up_driver():
    global driver

    chromedriver_autoinstaller.install()  
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('--no-sandbox')
    agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/96.0.4664.110 Safari/537.36'
    op.add_argument(f'user-agent={agent}')
    driver = webdriver.Chrome(chrome_options=op)
    driver.implicitly_wait(10) # poll for the element for 10 seconds

def close_driver():
    global driver
    driver.quit()
    

def navigate_to_team(team_name):
    global driver

    try:
        driver.get(HOME_URL)
        team_link = driver.find_element(By.XPATH, get_xpath(team_name))
        team_link.click()
    except Exception as e:
        logging.error(f"Unable to navigae to {team_name}'s page")


def change_year(year):
    global driver

    earliest_year, latest_year = 2010, 2021
    if  earliest_year < latest_year < 2010:
        raise Exception(f'Invalid Year. Must be between {earliest_year} and {latest_year}.')
    year_button = driver.find_element(By.XPATH, '//*[@id="megaDropDown-season"]')
    year_button.click()
    specific_year = driver.find_element(By.XPATH, f'//*[@label="{year}"]/option')
    specific_year.click()


def get_schedule_url(team_name, year, last_request=False):
    global driver

    navigate_to_team(team_name)
    change_year(year)
    schedule_link = driver.find_element(By.XPATH, get_xpath('Game Schedule'))
    schedule_link.click()

    current_url = driver.current_url
    if last_request:
        close_driver()
    return current_url

# def get_conf_schedule_urls(conf_name, year):
    # global driver

    # driver.get(HOME_URL)
    # conference = driver.find_element(By.XPATH, )
    # print(dir(conference))
    # urls = []
    # for team in conference:
        # get_schedule_url(team, year)

    # close_driver()
    # return urls


# not every team has a roster page
def get_roster_url(team_name, year):
    global driver

    navigate_to_team(team_name)
    change_year(year)
    roster_link = driver.find_element(By.XPATH, get_xpath('Roster'))
    roster_link.click()

    current_url = driver.current_url
    close_driver()
    return current_url


def get_stats_url(team_name, year):
    global driver

    navigate_to_team(team_name)
    change_year(year)
    stats_link = driver.find_element(By.XPATH, get_xpath('Player Stats'))
    stats_link.click()

    current_url = driver.current_url
    close_driver()
    return current_url


# generate xpath for links on a team home page
def get_xpath(text):
    return f'//a[text()="{text}"]'

