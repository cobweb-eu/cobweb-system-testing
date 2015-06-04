""" This is a python script to run the full registered use case test
    through the COBWEB system. It will load the portal, log in, create a survey
    with some questions, log out, log in as a user account, join the survey.
    It will then perform the necessary actions on an emulated device to submit
    an observation, before returning to the portal to check it is correctly
    visible.
    
    This test will concentrate on running the registered usecase, rather
    than checking every part of the portal on the way functions correctly.
    These checks will be covered by separate tests...
"""
import logging
import unittest
import datetime
import random
import sys
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

#sys.path.append('/home/envsys/src/libenvsys/python') # for below imports

from envsys.utils.testing.selenium import convenience as selutils
from envsys.utils.testing.selenium import conditions as ECENV
from envsys.utils.testing.selenium.cobweb import cobweb_statics as CS

TEST_USER_USERNAME = 'AutoIntegrationTestUser1'
OBSERVATION_TEXT = '3.5'

PLATFORM_VERSION = '4.4'

TEST_SURVEY = "9be11f06-d2ce-414d-81d4-83cf1834395a"

class COBWEBSurveyTest(unittest.TestCase, selutils.SimpleGetter):
    
    def assertVisible(self, element):
        return self.assertTrue(element.is_displayed())
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1280, 1024)
        self.wait = WebDriverWait(self.driver, 20)
        
    def tearDown(self):
        self.driver.close()
            
    def _accept_cookie_sign_in(self):
        self.driver.get(CS.LIVE_URL)
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.COOKIE_ACCEPT))
        ).click()
        
        self._login_with(self.USERNAME, self.PASSWORD)
    
    def _create_survey(self, name): 
        # Load metadata editor, configure and create new survey
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGOUT_LINK))
        )
        self.get_by_css(CS.CREATION_TOOLBOX).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.ADD_CONTENT_BUTTON))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.SURVEY_DATASET_SELECT))
        ).click()
        self.get_by_xpath(CS.SURVEY_TEMPLATE_SELECT).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.METADATA_GROUP_NAME))
        ).send_keys('RegUseCaseTest')
        self.get_by_xpath(CS.SURVEY_CREATE_BUTTON).click()
        
        # Set up / rename new survey
        survey_name = "%s %s"%(name, datetime.datetime.now())
        title_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.SURVEY_TITLE_INPUT))
        )
        abstract_input = self.get_by_xpath(CS.SURVEY_ABSTRACT_INPUT)
        title_input.clear()
        title_input.send_keys(survey_name)
        abstract_input.clear()
        abstract_input.send_keys(CS.SURVEY_ABSTRACT)
        self.get_by_xpath(CS.METADATA_SAVECLOSE_BUTTON).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.SURVEY_LIST_AREA))
        )
        
        return survey_name
    
    def _author_survey(self):
         # Modify the survey - set the first question
        self.get_by_xpath(CS.AT_TITLE_EDIT).click()
        text_title = self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.AT_TEXT_TITLE))
        )
        text_title.clear()
        text_title.send_keys("Your Name")
        self.get_by_xpath(CS.AT_OPTIONS_SUBMIT_BUTTON).click()
        
        # Drag and drop a widget
        drag_from = self.get_by_id(CS.AT_TEXT_CAP_WIDGET)
        drag_to = self.get_by_id(CS.AT_DROP_AREA)
        action_chains = ActionChains(self.driver)
        action_chains.drag_and_drop(drag_from, drag_to).perform()
        # Change title
        text_title = self.get_by_selector(CS.SEL_AT_TEXT_TITLE)
        text_title.clear()
        text_title.send_keys("Science Value")
        # and placeholder
        text_placeholder = self.get_by_id(CS.AT_PLACEHOLDER)
        text_placeholder.clear()
        text_placeholder.send_keys("3.14159")
        self.get_by_xpath(CS.AT_OPTIONS_SUBMIT_BUTTON).click()
        
        # Save survey
        self.get_by_selector(CS.SEL_AT_SAVE_BUTTON).click()
        # Wait for confirmation and close window
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.AT_SAVE_CONFIRM))
        )
        self.driver.close()

    def _search_join_survey(self, survey_name):
        # Join survey, search for it first
        self.get_by_selector(CS.SEL_SEARCH_INPUT).send_keys(survey_name)
        self.get_by_selector(CS.SEL_SEARCH_SUBMIT).click()
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              'a[title="%s"]'%survey_name))
        ).click()
        
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.JOIN_LINK))
        ).click()
    
        confirmed_box = self.get_by_selector(CS.SEL_JOINED_CONFIRM)
        self.assertTrue(confirmed_box.is_displayed())
        
        # return the survey_id
        return self.driver.current_url.split('/')[-1]
    
    def _login_with(self, username, password):
        # Perform login, click login link, choose COBWEB IdP
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGIN_LINK))
        ).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, 'content')))
        self.get_by_css(CS.IDP_BUTTON).click()
        
        # Login with username, password
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.USER_INPUT))
        ).send_keys(username)
        self.get_by_css(CS.PW_INPUT).send_keys(password)
        self.get_by_css(CS.LOGIN_SUBMIT).click()
        
        # Wait for the page to return logged in
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGOUT_LINK))
        )
 
        
class PortalTests(COBWEBSurveyTest):
    def setUp(self):
        self.USERNAME = 'sebclarke'
        self.PASSWORD = 'password'
        super(PortalTests, self).setUp()
    
    def test_login_create_survey(self):
        self._accept_cookie_sign_in()
        survey_name = self._create_survey("RegUseCase Test")
        
        # Load the survey detail page for our new survey, click survey designer
        self.get_by_xpath('//a[text()="%s"]'%survey_name).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.SURVEY_DETAIL_TITLE))
        )
        self.get_by_xpath(CS.AUTH_TOOL_BUTTON).click()
        
        # Switch to new window, check title of loaded survey
        self.driver.switch_to_window(self.driver.window_handles[1])
        title = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.AT_SURVEY_TITLE))
        )
        self.assertIn(survey_name, title.text)
        
        # Author the survey - add fields etc
        self._author_survey()
        
        # Switch back to main window and logout, login as test user
        self.driver.switch_to_window(self.driver.window_handles[0])
        self.get_by_selector(CS.SEL_LOGOUT_LINK).click()
        self._login_with(TEST_USER_USERNAME, PASSWORD)
    
        # Search and join the survey as test user
        global active_survey_id
        active_survey_id = self._search_join_survey(survey_name)
    
    
class AppTests(unittest.TestCase, selutils.SimpleGetter):
    def setUp(self):
        from appium import webdriver as appdriver
        app = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'COBWEB-0.0.7.apk'))
        desired_caps = {
            'app': app,
            'appPackage': 'uk.ac.edina.cobweb',
            'appActivity': '.COBWEB',
            'platformName': 'Android',
            'platformVersion': PLATFORM_VERSION,
            'deviceName': 'Android Emulator'
        }
        
        if (PLATFORM_VERSION != '4.4'):
            desired_caps['automationName'] = 'selendroid'

        self.driver = appdriver.Remote('http://localhost:4723/wd/hub',
                                       desired_caps)
        self.driver.switch_to.context('WEBVIEW_uk.ac.edina.cobweb')
        
        self.wait = WebDriverWait(self.driver, 20)
        self.long_wait = WebDriverWait(self.driver, 50)
        
    def tearDown(self):
        self.driver.quit()
    
    def close_eula_login_sync_surveys(self, username, password):
        # Wait for EULA Dialog - app fully open - then close
        self.wait.until(
            EC.element_to_be_clickable((By.ID, CS.APP_EULA_ACCEPT))
        ).click()
        
        # Click the download nav bar link
        download_nav_link = self.get_by_css(CS.APP_DOWNLOAD_NAV).click()
        
        # Get list of active pages before clicking login (opens new page)
        whs = self.driver.window_handles
        cwh = self.driver.current_window_handle
        
        # Click Login button
        self.get_by_css(CS.APP_LOGIN_LINK).click()
        
        # Wait for, Detect and switch to new window
        new_window = self.wait.until(ECENV.new_window_created(whs))
        self.driver.switch_to_window(new_window)
    
        # Select COBWEB IDP
        self.get_by_css(CS.IDP_BUTTON).click()
        # Fill form fields
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.USER_INPUT))
        ).send_keys(username)
        password_input = self.driver.find_element_by_css_selector(CS.PW_INPUT)
        password_input.send_keys(password)
        self.driver.find_element_by_css_selector(CS.LOGIN_SUBMIT).click()
        self.driver.switch_to_window(cwh)
        
        # Wait for return back to logged in Download page, click Download button
        try :
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, CS.APP_SYNC_BUTTON))
            ).click()
        except TimeoutException:
            self.fail("Log in failed, did not return to app logged in")
        
    def make_observation(self, survey_id, observation_text):
        try :
            self.wait.until(        # Wait to be returned to capture page
                EC.visibility_of_element_located((By.ID, CS.APP_CAP_VIEW)))
        except TimeoutException:    # if we arent, survey syncing probably failed
            self.fail("Survey syncing (downloading registered surveys) failed")
            
        # Check if there are some surveys
        found_surveys = self.list_by_css(CS.APP_SURVEY_LINKS)
        
        # Find and click our survey
        survey_ids = [el.get_attribute("data-editor-type") for el in found_surveys]
        self.assertIn(survey_id, survey_ids)
        found_surveys[survey_ids.index(survey_id)].click()
        
        # Make an observation - use text fields
        observation_name = "App%s"%random.randint(0, 40000)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.APP_TEXT_OBS_1))
        ).send_keys(observation_name)
        text_input = self.get_by_css(CS.APP_TEXT_OBS_2)
        text_input.send_keys(observation_text)
        self.driver.find_element_by_css_selector(CS.APP_RECORD_OBS).click()
        
        # Wait for GPS fix warning to appear, then dissappear - or not!
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))
        self.long_wait.until(EC.invisibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))
        
        # Save observation (without moving it)
        self.get_by_id(CS.APP_SAVE_OBS).click()
        
        # Upload observations
        self.get_by_xpath(CS.APP_LIST_OBS).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.APP_OBS_LIST)))
        self.get_by_xpath(CS.APP_OBS_UPLOAD).click()
        
        # Wait for confirm box to appear and dissapear
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))
        self.long_wait.until(
            EC.invisibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))
        
        # Check our observation is uploaded
        obs_link = self.get_by_xpath('//a[text()="%s"]'%observation_name)
        tick_div = obs_link.find_element_by_xpath('../../div[1]')
        self.assertIn("saved-records-list-synced-true",
                      tick_div.get_attribute("class"))
        
    def test_login_make_observation(self):
        self.close_eula_login_sync_surveys(TEST_USER_USERNAME, PASSWORD)
        self.make_observation(TEST_SURVEY, OBSERVATION_TEXT)
        
        
def suite():
    suite = unittest.TestSuite()
    #suite.addTest(PortalTests('test_login_create_survey'))
    suite.addTest(AppTests('test_login_make_observation'))
    return suite
    
def load_tests(loader, standard_tests, pattern):
    return suite()

if __name__ == '__main__':
    unittest.main()
