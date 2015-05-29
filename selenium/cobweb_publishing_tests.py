from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import cobweb_statics as CS # these are all my statics and selectors

from cobweb_reg_use_case_tests import TestUtils, SurveyTest

import unittest


class PublishTests(SurveyTest):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1280, 1024)
        self.wait = WebDriverWait(self.driver, 20)
        
        self._accept_cookie_sign_in()
        public_survey_name = self._create_survey("PubTest Public")
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
        self.get_by_xpath(CS.METADATA_SAVECLOSE_BUTTON)
        

    def tearDown(self):
        self.driver.close()
        
    def test_visible(self):
        self.assertTrue(False)
        
    def test_public_survey_searchable(self):
        pass