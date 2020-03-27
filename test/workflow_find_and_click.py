"""
A simple selenium test example written by python
"""
import sys
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

try:
    host = str(sys.argv[1])
except IndexError:
    print("No Test Address given. Defaulting to localhost")
    host = 'localhost'

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""
    def setUp(self):
        """Start web driver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_case_1(self):
        """Load Page, read title"""
        try:
            self.driver.get("http://" + host + ":8050/graph/bar/?expname=ESM1_historical&metric=duration,cpu_time")
            el = self.driver.find_element_by_xpath("//*[@id='page-content']/div/div[1]/div/div[1]/div/h5").text
            self.assertEqual(el, "Experiment Performance Management Tool")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
    def test_case_2(self):
        """See if experiment graph was made by id"""
        try:
            self.driver.get("http://" + host + ":8050/graph/bar/?expname=ESM1_historical&metric=duration,cpu_time")
            el = self.driver.find_element_by_id("bargraph")
            #self.assertEqual(el, "Experiment Performance Management Tool")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
    def test_case_3(self):
        """See if component graph was made by id"""
        try:
            self.driver.get("http://" + host + ":8050/graph/bar?metric=duration,cpu_time&expname=ESM1_historical&exp_component=ocean_annual_rho2_1x1deg")
            el = self.driver.find_element_by_id("bargraph")
            #self.assertEqual(el, "Experiment Performance Management Tool")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
    def test_case_4(self):
        """See if job graph was made by id"""
        try:
            self.driver.get("http://" + host + ":8050/graph/bar?metric=duration,cpu_time&expname=ESM1_historical&jobs=1234043&op=op")
            el = self.driver.find_element_by_id("bargraph")
            #self.assertEqual(el, "Experiment Performance Management Tool")
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
