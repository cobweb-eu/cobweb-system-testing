import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from utils import conditions as ECENV
from utils import statics as CS
from utils.helpers import SurveyHelper


class PublishTests(SurveyHelper):

    def setUp(self):
        """self.driver = webdriver.Chrome('C:\Users\Admin.ENVSYS-704\Desktop\Extra\chromedriver_win32\chromedriver.exe')"""
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1280, 1024)
        self.wait = WebDriverWait(self.driver, 20)
        self.long_wait = WebDriverWait(self.driver, 50)
        self.USERNAME = 'MHiggins'
        self.PASSWORD = 'webboc_9625'
        self._accept_cookie_sign_in()
        self.public_survey_name = self._create_survey("PubTest Public")
        self.driver.get(CS.PRIV_URL)
        self.private_survey_name = self._create_survey("PubTest Private")
        survey_link = self.get_by_xpath('//a[text()="%s"]'%self.public_survey_name)
        edit_link = survey_link.find_element_by_xpath(CS.XPATH_SURVEY_EDIT_REL)
        edit_link.click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.METADATA_BOUNDBOX))
        )
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.PUBLISH_BUTTON))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.UNPUBLISH_BUTTON))
        )
        self.get_by_xpath(CS.METADATA_SAVECLOSE_BUTTON).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.SURVEY_LIST_AREA))
        )
    def tearDown(self):
        self._delete_survey(self.private_survey_name)
        self._delete_survey(self.public_survey_name)

        self.driver.close()

    def test_visible(self):
        # Delete cookies to clear login, return to the homepage
        self.driver.get(CS.LIVE_URL)
        # Access Search Tool
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.NAVBAR_SEARCH))
        ).click()
        # Input the title of Public Survey, press search/enter
        self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.NSEARCH_INPUT))
        ).send_keys(self.public_survey_name)
        self.get_by_xpath(CS.NSEARCH_SUBMIT).click()
        # If survey is visible, true, if not, false/fail

        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, '//a[contains(., "%s")]'%self.public_survey_name))
            )
        except TimeoutException:
            self.fail("Did not find survey in search")

        # Check private survey is not shown!
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.NSEARCH_CLEAR))
        ).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.NSEARCH_INPUT))
        ).send_keys(self.private_survey_name)
        self.get_by_xpath(CS.NSEARCH_SUBMIT).click()

        # YOU NEED A SELF.WAIT.UNTIL to not do any more processing until search
        # results are returned

        matching_survey_links = self.list_by_xpath('//a[contains(., "%s")]'%self.private_survey_name)
        self.assertEqual(len(matching_survey_links), 0, 'Private survey visible when not logged in!')

        # Next, test for visibility of the Private Survey. Return to homepage, sign-in as Registered User account
        self.driver.get(CS.PRIV_URL)
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGOUT_LINK))
        ).click()
        self.USERNAME = "PublishTester1"
        self.PASSWORD = "password"
        self._login_with(self.USERNAME, self.PASSWORD)
        # Return to search tool, input Private Survey title into search bar, press search/enter
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.NSEARCH_INPUT))
        ).send_keys(self.private_survey_name)
        self.get_by_xpath(CS.NSEARCH_SUBMIT).click()
        self.assertEqual(len(matching_survey_links), 1, 'Private survey NOT visible when logged in!')

        # If survey is visible, true, if not false/fail. Portal end of test is complete.
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
