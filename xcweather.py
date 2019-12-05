from bs4 import BeautifulSoup
import requests
from selenium import webdriver


class XCWeatherLocation(object):

    def __init__(self, location):
        self.location = location
        self.base = "https://www.xcweather.co.uk/forecast/"

    def get_report(self):
        browser = webdriver.Chrome()

        browser.get(self.base + self.location)

        # if response.status_code != 200:
        #     raise Exception("Request error {}".format(response.status_code))

        soup = BeautifulSoup(browser.page_source, 'lxml')
        print(soup)

        # rows = soup.find_all('tr', _class='fcastrow')

        print(rows)


class XCWeatherReport(object):

    def __init__(self, location):
        self.location = location



if __name__ == "__main__":
    
    xc = XCWeatherLocation("Weston-super-Mare")
    xc.get_report()