import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
        print(is_prowly_present)
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
