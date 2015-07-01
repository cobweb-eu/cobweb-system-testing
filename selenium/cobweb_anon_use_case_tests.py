""" This is a python script to run the full public use case test
    through the COBWEB system. It will load the portal, log in, create a public survey
    with some questions, and log out.
    It will then perform the necessary actions on an emulated device to submit
    an observation, before returning to the portal to check it is correctly
    visible.
    
    This test will concentrate on running the public or anonymous usecase, rather
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

SURVEY_BASE_NAME = "AnonUseCase Test"
SURVEY_GROUP_NAME = "AnonUseCaseTest"
SURVEY_ABSTRACT = "Auto-created test survey from Anonymous Use Case auto system test"

class AnonPortalTests(SurveyHelper):
    """ Class containing the tests for the portal side
        of anonymous use case testing.
    """
    
    def setUp(self):
        self.USERNAME = 'MHiggins'
        self.PASSWORD = 'webboc_9625'
        self.driver = webdriver.Chrome('C:\Users\Admin.ENVSYS-704\Desktop\Extra\chromedriver_win32\chromedriver.exe')
        super(PortalTests, self).setUp()
    
    def test_login_create_survey(self):
        """ Test that we can login, create and join a survey
            
            Saves the created/joined survey as a global
            so we can make observations to it and check
            that they exist later
        """
        self._accept_cookie_sign_in()
        my_survey = self._create_survey(SURVEY_BASE_NAME, SURVEY_GROUP_NAME, SURVEY_ABSTRACT)
        
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




















