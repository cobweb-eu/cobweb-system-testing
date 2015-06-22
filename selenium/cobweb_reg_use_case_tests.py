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
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from envsys.testing.selutils import conditions as ECENV
from envsys.testing.cobweb import cobweb_statics as CS
from envsys.testing.cobweb.helpers import SurveyHelper, AppHelper
from envsys.testing.cobweb.structures import Survey
from envsys.general.functions import parse_colon_separated_results

# Statics for testing individual sub-tests (with pre-existing surveys/obs)

TEST_SURVEY_ID = "33754d35-9df0-422b-ac5c-14078eee45f6"
TEST_SURVEY_NAME = "RegUseCase Test 2015-06-18 12:01:01.939211"
TEST_OBSERVATION_NAME = ""
TESTING = False # Set to true to test individual sub-tests

# Statics for configuring input params

SURVEY_BASE_NAME = "RegUseCase Test"
TEST_USER_USERNAME = 'AutoIntegrationTestUser1'


class PortalTests(SurveyHelper):
    """ Class containing the tests for the portal side
        of registered user use-case testing
        
        Subclasses envsys.testing.cobweb.helpers.SurveyHelper providing
        unittest.TestCase functionality and simplified element lookup. Also
        provides a load of convenience functions for performing portal actions
    """
    
    def setUp(self):
        """ Set up the test pre-requisites for each test """
        self.USERNAME = 'sebclarke'
        self.PASSWORD = 'password'
        self.driver = webdriver.Chrome()
        super(PortalTests, self).setUp()
    
    def test_login_create_survey(self):
        """ Test that we can login, create and join a survey
            
            Saves the created/joined survey as a global
            so we can make observations to it and check
            that they exist later
        """
        self._accept_cookie_sign_in()
        my_survey = self._create_survey(SURVEY_BASE_NAME)
        
        # Author the survey - add fields etc
        self._author_survey(my_survey)
        
        # Switch back to main window and logout, login as test user
        self.driver.switch_to_window(self.driver.window_handles[0])
        self.get_by_xpath(CS.LOGOUT_LINK).click()
        self._login_with(TEST_USER_USERNAME, self.PASSWORD)
    
        # Search and join the survey as test user
        global active_survey
        active_survey = my_survey
        self._join_survey(active_survey)
       
    def test_login_check_observations(self):
        """ Test that we can login and see an observation
            
            First checks that we have saved globals for a survey and
            observation, then checks the details of the stored observation on
            the portal page for the stored survey
        """

        if 'active_observation_name' not in globals():
            self.fail("No observation has been made...")
        elif 'active_survey' not in globals():
            self.fail("No survey has been created...")
            
        # Login (as coord) and go to the survey detail page
        self._accept_cookie_sign_in()
        
        self._check_observation_minimap()
        
        # Now try the main map viewer also
        # Click the view on map link and wait for the map canvas
        self.driver.switch_to_default_content()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.VIEW_ON_MAP))
        ).click()
        
        map_canvas = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.MAP_CANVAS))
        )
        
        # Click the layers, find the survey and zoom to layer
        self.get_by_xpath(CS.MAP_LAYERS).click()
        label = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ('//label[contains(.,"%s")]'%SURVEY_BASE_NAME))
            )
        )
        zoom_to_extent = label.find_element_by_xpath('../button[2]')
        zoom_to_extent.click()
        self.get_by_xpath(CS.CLOSE_LAYERS).click()
    
        # Now click in the center and check the observations
        act = ActionChains(self.driver)
        act.move_to_element(map_canvas).click().perform()
    
        obs_details = parse_colon_separated_results(
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, CS.MAP_OBS_DETAILS)
                )
            ).text.split('\n')
        )
        
        # Fieldname is title, lowercase, with spaces replaced for '_'
        result_name = '_'.join([val.lower() if i > 0 else val
                                for i, val
                                in enumerate(CS.TEXT_INPUT_TITLE.split(' '))])
        
        self.assertEqual(obs_details['Qa_name'], active_observation_name)
        self.assertEqual(obs_details[result_name], CS.OBSERVATION_TEXT)
  
        
class AppTests(AppHelper):
    """ The tests on the App side of COBWEB for the
        registered user use case testing
        
        Subclasses AppHelper to provide unittest.TestCase functionality,
        simple web_element lookup and convenience functions for performing
        activities related to surveys within the app.
    """
    
    def test_login_make_observation(self):
        if 'active_survey' not in globals():
            self.fail("No survey has been made/joined")
        
        self.close_eula_login_sync_surveys(TEST_USER_USERNAME, self.PASSWORD)
        global active_observation_name
        active_observation_name = self.make_observation(active_survey, CS.OBSERVATION_TEXT)    
          
              
# Unit test boot strapping stuff, manages the whole process

def suite():
    """ Define what tests to run and the order in
        which they shall be executed for this test
    """
    suite = unittest.TestSuite()
    
    if(TESTING):
        global active_survey
        global active_observation_name
        active_survey = Survey(TEST_SURVEY_ID, TEST_SURVEY_NAME)
        active_observation_name = TEST_OBSERVATION_NAME
        
    # First, add the test for logging in and creating/joining a survey
    suite.addTest(PortalTests('test_login_create_survey'))
    
    # Next, on the app, do the logging in and making observation test
    suite.addTest(AppTests('test_login_make_observation'))
    
    # Finally, do the portal test of viewing the observation
    suite.addTest(PortalTests('test_login_check_observations'))
    
    return suite
    
def load_tests(loader, standard_tests, pattern):
    return suite()

if __name__ == '__main__':
    unittest.main()
