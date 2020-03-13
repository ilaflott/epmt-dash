"""
A simple selenium test example written by python
"""
import sys
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

try:
    TEST_ADDRESS = str(sys.argv[1])
except IndexError:
    print("No Test Address given. Defaulting to localhost")
    TEST_ADDRESS = 'http://localhost:8050'

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""
    def setUp(self):
        """Start web driver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_case_1(self):
        """Find and click Recent Jobs tab"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='tabs']/div[1]/span")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_2(self):
        """Find and Click Models tab"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='tabs']/div[2]/span")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_3(self):
        """Find and Click Raw Data Toggle"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='raw-switch']/div/div/div[2]/button")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_4(self):
        """Find and Click Search Area"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='searchdf']")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_5(self):
        """Find and Click Run Analysis button"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='run-analysis-btn']")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_6(self):
        """Find and Click Create model from jobs button"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='create-newModel-btn']")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_7(self):
        """Find and Click Select All button"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='index-select-all']")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_8(self):
        """Find and Click Date start and end"""
        try:
            self.driver.get(TEST_ADDRESS)
            # Activate date picker dialog
            el = self.driver.find_element_by_xpath("//*[@id='jobs-date-picker']/div/div/div[1]")
            el.click()
            # Click start date
            el = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[1]/td[7]")
            el.click()
            # Delay
            self.driver.implicitly_wait(3)
            # Click end date
            el = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[4]")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_9(self):
        """Find and Click Available test model dropdown"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='react-select-2--value']/div[1]")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_10(self):
        """Find and Click number of jobs to display dropdown"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='react-select-3--value']/div[1]")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_11(self):
        """Find and Click issue tracker"""
        try:
            self.driver.get(TEST_ADDRESS)
            el = self.driver.find_element_by_xpath("//*[@id='version']/a")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)
    # Test Models tab

    def test_case_12(self):
        """Find and click Models tab, test all buttons"""
        try:
            self.driver.get(TEST_ADDRESS)
            # Find and click Models tab
            el = self.driver.find_element_by_xpath("//*[@id='tabs']/div[2]/span")
            el.click()
            # Find and Click Toggle Model Status
            el = self.driver.find_element_by_xpath("//*[@id='toggle-Model-btn']")
            el.click()
            # Find and Click Edit Reference Model
            el = self.driver.find_element_by_xpath("//*[@id='edit-Model-btn']")
            el.click()
            # Find and Click Delete Model button
            el = self.driver.find_element_by_xpath("//*[@id='delete-Model-btn']")
            el.click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    # def test_case_2(self):
    #     """Find and click Learn more button"""
    #     try:
    #         self.driver.get('https://www.oursky.com/')
    #         el = self.driver.find_element_by_xpath(".//*[@id='tag-line-wrap']/span/a")
    #         el.click()
    #     except NoSuchElementException as ex:
    #         self.fail(ex.msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
