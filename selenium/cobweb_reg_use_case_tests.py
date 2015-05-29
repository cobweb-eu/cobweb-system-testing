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
import unittest
import datetime
import sys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

sys.path.append('/home/envsys/src/libenvsys/python')

from envsys.utils.testing.selenium import convenience as selutils
from envsys.utils.testing.selenium import conditions as ECENV
from envsys.utils.testing.selenium.cobweb import cobweb_statics as CS

USERNAME = 'sebclarke'
PASSWORD = 'password'

TEST_USER_USERNAME = 'AutoIntegrationTestUser1'

class SurveyTest(unittest.TestCase, selutils.SimpleGetter):
    
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
        
        # Click the login link and choose cobweb IDP
        self.get_by_xpath(CS.LOGIN_LINK).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, 'content')))
        self.get_by_css(CS.IDP_BUTTON).click()
        
        # Login with username and password
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.USER_INPUT))
        ).send_keys(USERNAME)
        self.get_by_css(CS.PW_INPUT).send_keys(PASSWORD)
        self.get_by_css(CS.LOGIN_SUBMIT).click()
    
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
        abstract_input.send_keys(CS.SURVEY_ABSTRACT)
        self.get_by_xpath(CS.METADATA_SAVECLOSE_BUTTON).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.SURVEY_LIST_AREA))
        )
        
        return survey_name


class RegisteredUseCase(SurveyTest):
    
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
        
        # Switch back to main window and logout, login as user
        self.driver.switch_to_window(self.driver.window_handles[0])
        self.get_by_selector(CS.SEL_LOGOUT_LINK).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGIN_LINK))
        ).click()   
        self.wait.until(EC.visibility_of_element_located((By.ID, 'content')))
        self.get_by_css(CS.IDP_BUTTON).click()
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.USER_INPUT))
        ).send_keys(TEST_USER_USERNAME)
        self.get_by_css(CS.PW_INPUT).send_keys(PASSWORD)
        self.get_by_css(CS.LOGIN_SUBMIT).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGOUT_LINK))
        )
        
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
        