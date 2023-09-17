import unittest
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import months


class SearchingTests(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--incognito')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("https://www.google.pl/?hl=pl")

    # searching method
    def findProwlyInGoogle(self):
        accept_policy = self.driver.find_element(By.ID, "L2AGLb")
        accept_policy.click()
        search_box = self.driver.find_element(By.XPATH, "//textarea[@id='APjFqb']")
        search_box.send_keys("prowly")
        search_box.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "result-stats"))
        )

    # test searching by all category
    def testSearchingByAll(self):
        self.findProwlyInGoogle()
        search_results_by_all = self.driver.find_elements(By.CLASS_NAME, "MjjYud")
        is_prowly_present = all("prowly" in result.text.lower() for result in search_results_by_all)
        self.assertTrue(is_prowly_present, "The word 'prowly' is not present in the search results")

    # test searching by video
    def testSearchingVideos(self):
        self.findProwlyInGoogle()
        button_videos = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Wideo')]")
        button_videos.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "result-stats"))
        )
        search_result_by_video = self.driver.find_elements(By.CLASS_NAME, "g")
        is_prowly_present = all("prowly" in result.text.lower() for result in search_result_by_video)
        self.assertTrue(is_prowly_present, "The word 'prowly' is not present in the search results")

    # test searching by news
    def testSearchingCareers(self):
        self.findProwlyInGoogle()
        button_careers = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Careers')]")))
        button_careers.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "result-stats"))
        )
        search_result_by_careers = self.driver.find_elements(By.CLASS_NAME, "SoaBEf")
        is_prowly_present = all("prowly" in result.text.lower() for result in search_result_by_careers)
        self.assertTrue(is_prowly_present, "The word 'prowly' is not present in the search results")

        # method searching by date

    def changeDateFilter(self, text):
        self.findProwlyInGoogle()
        button_tool = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Narzędzia')]")))

        button_tool.click()

        button_ever = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Kiedykolwiek')]")))

        button_ever.click()
        xpath = "//a[contains(text(),'" + text + "')]"
        button_time_interval = self.driver.find_element(By.XPATH, xpath)
        button_time_interval.click()

    def testAllByLastWeek(self):
        self.filteringByDate('Ostatni tydzień', 7)

    def testAllByLastMonth(self):
        self.filteringByDate('Ostatni miesiąc', 31)

    def testAllByLastYear(self):
        self.filteringByDate('Ostatni rok', 366)

    def filteringByDate(self, date_filter_name, days):
        self.changeDateFilter(date_filter_name)
        search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
        for i in search_results:
            date_span = i.find_element(By.CLASS_NAME, "MUxGbd.wuQ4Ob.WZ8Tjf")
            if date_span is not None:
                date_list = date_span.text.split(" ")
                if (date_list[1] == "dni" or date_list[1] == "dzień") and date_list[2] == "temu":
                    self.assertLessEqual(int(date_list[0]), days)
                else:
                    month = months[date_list[1]]
                    date = datetime(int(date_list[2]), month, int(date_list[0]))
                    today = datetime.now()
                    x = today - date
                    self.assertLessEqual(x.days, days)
