import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from envsys.utils.testing.selenium import conditions as ECENV
from envsys.utils.testing.selenium.cobweb import cobweb_statics as CS
from cobweb_reg_use_case_tests import COBWEBSurveyTest

class PublishTests(COBWEBSurveyTest):
    
    def setUp(self):
        self.driver = webdriver.Chrome('C:\Users\Admin.ENVSYS-704\Desktop\Extra\chromedriver_win32\chromedriver.exe')
        self.driver.set_window_size(1280, 1024)
        self.wait = WebDriverWait(self.driver, 20)
        self.long_wait = WebDriverWait(self.driver, 50)
        self.USERNAME = 'MHiggins'
        self.PASSWORD = 'webboc_9625'
           
    def tearDown(self):
        self.driver.close()
        
    def test_visible(self):
        self._accept_cookie_sign_in()
        public_survey_name = self._create_survey("PubTest Public")
        
        self.driver.get(CS.LIVE_URL)
        private_survey_name = self._create_survey("PubTest Private")
        survey_link = self.get_by_xpath('//a[text()="%s"]'%public_survey_name)
        edit_link = survey_link.find_element_by_xpath(CS.XPATH_SURVEY_EDIT_REL)
        edit_link.click()
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
    #Delete cookies to clear login, return to the homepage
        self.driver.delete_all_cookies()
        self.driver.get(CS.LIVE_URL)
        #Access Search Tool
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.NAVBAR_SEARCH))
        ).click()
    #Input the title of Public Survey, press search/enter
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.NSEARCH_INPUT))
        ).send_keys(public_survey_name)
        self.get_by_xpath(CS.NSEARCH_SUBMIT).click()
        
    #If survey is visible, true, if not, false/fail
        self.wait.until(
            EC.visibility_of_element_located(By.XPATH, ('//a[contains(., "%s")]'%public_survey_name))
        )
        
    #Check private survey is not shown!
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.NSEARCH_INPUT))
        ).send_keys(private_survey_name)
        self.get_by_xpath(CS.NSEARCH_SUBMIT).click()
        matching_survey_links = self.list_by_xpath('//a[contains(., "%s")]'%private_survey_name)
        self.assertEqual(len(matching_survey_links), 0, 'Private survey visible when not logged in!')
        
    #Next, test for visibility of the Private Survey. Return to homepage, sign-in as Registered User account
        self.driver.delete_all_cookies()
        self.driver.get(CS.LIVE_URL)
        self.USERNAME = "PublishTester1"
        self.PASSWORD = "password"
        self._login_with(self.USERNAME, self.PASSWORD)
    #Return to search tool, input Private Survey title into search bar, press search/enter
        self.assertEqual(len(matching_survey_links), 0, 'Private survey visible when not logged in!')
        
    #If survey is visible, true, if not false/fail. Portal end of test is complete.
        self.assertTrue(False)
        

if __name__ == '__main__':
    unittest.main()