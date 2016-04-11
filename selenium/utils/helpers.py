""" Helpers for testing COBWEB using selenium

    These are generic base classes that provide useful sub functions
    when executing COBWEB tests through selenium
"""
import StringIO
import unittest
import datetime
import logging
import pycurl
import random
import json
import os

from time import sleep

from owslib.wfs import WebFeatureService

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from . import conditions as ECENV
from . import Survey
from . import statics as CS
from . import pp, convert_from_friendly_name, parse_observation

PLATFORM_VERSION = '4.4'


class SimpleGetter(object):
    """ SimpleGetter class simply defines some convenience
        functions for performing single and multi element
        selection using selenium, CSS and XPATH. Expects to
        have a selenium webdriver instance at self.driver
    """

    def get_by_id(self, _id):
        """ Get an element selected by its ID
        """
        return self.driver.find_element_by_id(_id)

    def get_by_xpath(self, xpath_query):
        """ Get an element by an xpath query
        """
        return self.driver.find_element_by_xpath(xpath_query)

    def list_by_xpath(self, xpath_query):
        """ Get a list of elements with an xpath query
        """
        return self.driver.find_elements_by_xpath(xpath_query)

    def get_by_css(self, css_query):
        """ Get a single element with a CSS selector expression
        """
        return self.driver.find_element_by_css_selector(css_query)

    def list_by_css(self, css_query):
        """ Get a list of elements with a CSS selector expression
        """
        return self.driver.find_elements_by_css_selector(css_query)

    def check_exists(self, function, selector):
        """ Check if an element exists according to a function and selector

            Takes an arbitrary function pointer, and a selector and calls
            the function with the selector as argument. It catches the
            NoSuchElementException and returns false if it raised
        """
        try:
            function(selector)
        except NoSuchElementException:
            return False
        return True


class SurveyHelper(unittest.TestCase, SimpleGetter):
    """ Base class that can perform a number of abstract
        functions related to surveys on the COBWEB portal

        Sub-classed by others to write system-tests, or included within
        them to support other module tests
    """

    def assertVisible(self, element):
        """ Assert that a web_element is displayed
        """
        return self.assertTrue(element.is_displayed())

    def setUp(self):
        """ Set up the pre-requisites for each individual test
        """
        # Check if an extending class has set the driver yet
        if not hasattr(self, 'driver'):
            self.driver = webdriver.Firefox()
        self.driver.set_window_size(1280, 1024)
        self.wait = WebDriverWait(self.driver, 20)
        self.long_wait = WebDriverWait(self.driver, 60)
        self.public_wfs = WebFeatureService(CS.WFS_PUB_URL, version='2.0.0')
        self.private_wfs = WebFeatureService(CS.WFS_SEC_URL, version='2.0.0')

    def tearDown(self):
        """ Cleanup after the test
        """
        self.driver.close()

    def _accept_cookie_sign_in(self):
        """ Accept the cookie policy and perform sign in
        """
        self.driver.get(CS.LIVE_URL)
        self.long_wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.COOKIE_ACCEPT))
        ).click()

        self._login_with(self.USERNAME, self.PASSWORD)

    def _logout(self):
        """ Go the protected url and logout, will not work if not logged in
        """
        self.driver.get(CS.PRIV_URL)
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.LOGOUT_LINK))
        ).click()
        self.current_user = None

    def _create_survey(self, name, group_name='regusecase', abstract=CS.SURVEY_ABSTRACT):
        """ Create a new survey using name parameter as first base
            And group_name as second base.
            Appends the date-time to the name, and returns a
            Survey object with name and id attributes representing
            the newly created survey in COBWEB
        """
        # Load metadata editor, configure and create new survey
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.CREATION_TOOLBOX))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.ADD_CONTENT_BUTTON))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.SURVEY_DATASET_SELECT))
        ).click()
        self.get_by_xpath(CS.SURVEY_TEMPLATE_SELECT).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.METADATA_GROUP_NAME))
        ).send_keys(group_name)
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
        abstract_input.send_keys(abstract)
        self.get_by_xpath(CS.METADATA_SAVECLOSE_BUTTON).click()
        survey_link = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH, '//a[text()="%s"]'%survey_name
            ))
        )
        return Survey(survey_link.get_attribute('href').split('/')[-1], survey_name)

    def _create_public_survey(self, name, group_name='regusecase', abstract=CS.SURVEY_ABSTRACT):
        """ Create a new public survey using name parameter as first base
            And group_name as second base.
            Appends the date-time to the name, and returns a
            Survey object with name and id attributes representing
            the newly created survey in COBWEB
        """
        # Load metadata editor, configure and create new survey
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.CREATION_TOOLBOX))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.ADD_CONTENT_BUTTON))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.SURVEY_DATASET_SELECT))
        ).click()
        self.get_by_xpath(CS.SURVEY_TEMPLATE_SELECT).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.METADATA_GROUP_NAME))
        ).send_keys(group_name)
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
        abstract_input.send_keys(abstract)

        # Select 'Make public' button, wait until button changes colour, then save/close
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.PUBLISH_BUTTON))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.UNPUBLISH_BUTTON))
        )
        self.get_by_xpath(CS.METADATA_SAVECLOSE_BUTTON).click()
        survey_link = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH, '//a[text()="%s"]'%survey_name
            ))
        )
        return Survey(survey_link.get_attribute('href').split('/')[-1], survey_name)

    def _author_survey(self, survey):
        """ Author a previously created survey

            This involves opening the survey designer
            and adding various fields to the survey
        """
        # First go to the survey page
        self.driver.get(CS.SURVEY_DETAIL_URL + survey.id)
        # Load the survey detail page for our new survey, click survey designer
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.AUTH_TOOL_BUTTON))
        ).click()

        # Switch to new window, check title of loaded survey
        # We want to wait for this window first, the old window seems to be mysteriously destroyed?
        new_window = self.wait.until(ECENV.new_window_created(self.driver.window_handles))
        self.driver.switch_to.window(new_window)
        title = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.AT_SURVEY_TITLE))
        )
        self.assertIn(survey.name, title.text)

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
        text_title = self.get_by_id(CS.AT_TEXT_TITLE)
        text_title.clear()
        text_title.send_keys(CS.TEXT_INPUT_TITLE)
        # and placeholder
        text_placeholder = self.get_by_id(CS.AT_PLACEHOLDER)
        text_placeholder.clear()
        text_placeholder.send_keys("3.14159")
        self.get_by_xpath(CS.AT_OPTIONS_SUBMIT_BUTTON).click()

        # Save survey
        self.get_by_xpath(CS.AT_SAVE_BUTTON).click()
        # Wait for confirmation and close window
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.AT_SAVE_CONFIRM))
        )
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def _author_image_capture_survey(self, survey):
        """ Author a previously created survey

            This involves opening the survey designer
            and adding image capture widget
        """
        # First go to the survey page
        self.driver.get(CS.SURVEY_DETAIL_URL + survey.id)
        # Load the survey detail page for our new survey, click survey designer
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.AUTH_TOOL_BUTTON))
        ).click()

        # Switch to new window, check title of loaded survey
        self.driver.switch_to_window(self.driver.window_handles[1])
        title = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.AT_SURVEY_TITLE))
        )
        self.assertIn(survey.name, title.text)

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
        text_title = self.get_by_id(CS.AT_TEXT_TITLE)
        text_title.clear()
        text_title.send_keys(CS.TEXT_INPUT_TITLE)
        # and placeholder
        text_placeholder = self.get_by_id(CS.AT_PLACEHOLDER)
        text_placeholder.clear()
        text_placeholder.send_keys("3.14159")
        self.get_by_xpath(CS.AT_OPTIONS_SUBMIT_BUTTON).click()

        # Save survey
        self.get_by_xpath(CS.AT_SAVE_BUTTON).click()
        # Wait for confirmation and close window
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.AT_SAVE_CONFIRM))
        )
        self.driver.close()

    def _join_survey(self, survey):
        """ Join a survey as the currently logged in user """
        self.driver.get(CS.SURVEY_DETAIL_URL + survey.id)
        join_link = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.JOIN_LINK))
        )
        join_link.click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.JOINED_CONFIRM))
        )
        sleep(5)

    def _login_with(self, username, password):
        """ Log in to COBWEB IDP using the username and password provided

            This function assumes you are at a COBWEB
            page with the login link currently visible
        """
        # click login link, choose COBWEB IdP
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
        self.current_user = username

    def _delete_survey(self, survey):
        """ Log in as the coord account and delete the survey provided
        """
        self.driver.delete_all_cookies()
        self.driver.get(CS.LIVE_URL)
        self._accept_cookie_sign_in()
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.CREATION_TOOLBOX))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.METADATA_SEARCH_INPUT))
        ).send_keys(survey.id)
        self.get_by_xpath(CS.METADATA_SEARCH_GO).click()

        s_link = self.wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                'a[data-ng-href="catalog.search#/metadata/%s"]'%survey.id
            ))
        )

        s_link.find_element_by_xpath('../../td[3]/a').click()

    def _publish_survey(self, survey):
        """ Publish a survey

            Goes to the creation toolbox and finds the link for the survey
            according to its name. Clicks the link, and then clicks publish
        """
        self.driver.get(CS.CREATION_TOOLBOX_URL)
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.MY_ITEMS_CHECK))
        ).click()
        survey_link = self.wait.until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//a[text()="%s"]'%survey.name))
        )
        survey_link.find_element_by_xpath(CS.XPATH_SURVEY_EDIT_REL).click()
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

    def _remove_user_from_group(self, user, group_name):
        """ Login as admin, find the user, find the group and deselect it
        """
        self.driver.get(CS.PRIV_URL)
        self._logout()
        self._login_with(self.USERNAME, self.PASSWORD)
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.ADMIN_CONSOLE))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.USERS_AND_GROUPS))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.MANAGE_USERS))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.USER_FILTER))
        ).send_keys(user.uuid)
        self.get_by_xpath('//a[contains(., "%s")]'%user.uuid).click()
        membership_list = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.PARTICIPANT_LIST))
        )

        group_option = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                '//option[contains(., "%s") and @selected]'%group_name))
        )


        # action chain to shift-click the option to deselect
        act = ActionChains(self.driver)
        act.key_down(Keys.CONTROL).click(group_option).key_up(Keys.CONTROL).perform()

        # save the user
        self.get_by_xpath(CS.SAVE_USER_BUTTON).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//p[contains(., "userUpdated")]'))
        )

    def check_observation_minimap(self, survey, observation):
        """ Checks that an observation is visible through the portal

            This check looks at the minimap (contingency viewer) and
            takes the survey and observation details to check against
        """
        self.driver.get(CS.SURVEY_DETAIL_URL + survey.id)
        self.driver.switch_to.frame(self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.IFRAME))))

        minimap = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[name()="svg"]')))

        act = ActionChains(self.driver)
        act.move_to_element(minimap).move_by_offset(0, -5).click().perform()

        try:
            minimap_info = self.wait.until(
                EC.visibility_of_element_located((By.XPATH,
                                                  CS.MINIMAP_OBS_DETAILS))
            )
            obs_details = parse_observation(minimap_info.text.split('\n'))
        except TimeoutException:
            self.fail("Minimap popup did not appear")
        finally:
            self.driver.switch_to.default_content()


        self.assertEqual(obs_details['Name'], observation)
        self.assertEqual(obs_details[CS.TEXT_INPUT_TITLE], CS.OBSERVATION_TEXT)

    def check_public_observation_wfs(self, survey, observation):
        res = json.load(self.public_wfs.getfeature('sid-%s'%survey.id,
                                                   outputFormat='json'))
        self._check_features_contain_observation(res, observation)

    def check_private_observation_wfs(self, survey, observation, uuid):
        """ Checks that an observation is visible on the private WFS
            endpoint. This check needs to send uuid and cookie info.

            :param survey: The survey object to check results on
            :param observation: The name of the observation to check for
            :param uuid: The uuid of the user to perform the check as
        """
        log = logging.getLogger('SurveyHelper.check_private_observation_wfs')

        request = self.private_wfs.getGETGetFeatureRequest('sid-%s'%survey.id,
                                                      outputFormat='json')
        log.debug("performing request %s"%request)
        strbuf = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, request)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(c.WRITEDATA, strbuf)
        c.setopt(pycurl.HTTPHEADER, ['AJP_employeeNumber: %s'%uuid])
        c.setopt(pycurl.COOKIE, 'surveys="%s"; AJP_employeeNumber="%s"'%(survey.id, uuid))
        c.perform()
        c.close()
        log.debug("Got response: %s"%strbuf.getvalue())
        response = json.load(strbuf)
        strbuf.close()
        self._check_features_contain_observation(response, observation)

    def _check_features_contain_observation(self, json_features, observation):
        """ Check parsed JSON for existence of the specific observation """
        log = logging.getLogger('SurveyHelper._check_features_contain_observation')
        log.debug('Looking for observation %s in json'%observation)
        log.debug(pp.pformat(json_features))
        # slim list down to required observation, check some still left!
        my_observations = [f['properties'] for f in json_features['features']
                          if f['properties']['qa_name'] == observation]
        self.assertGreater(len(my_observations), 0, "No matching observations")

        # Test observation has the right text (take first matching)
        obs = my_observations[0][convert_from_friendly_name(CS.TEXT_INPUT_TITLE)]
        self.assertEqual(obs, CS.OBSERVATION_TEXT,
                         "Observation text does not match")

class AppHelper(unittest.TestCase, SimpleGetter):
    """ Base class to perform a number of functions
        on the COBWEB app on an emulated android device

        This class uses appium to perform the commands
        and is extended or included by other classes to
        support tests
    """


    def runTest(self):
        """ Placeholder to allow construction independently from
            unittest test cases
        """
        pass

    def setUp(self):
        """ Set up the pre-requisites for the tests """
        from appium import webdriver as appdriver
        app = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'COBWEB-debug.apk'))
        desired_caps = {
            'app': app,
            'appPackage': 'uk.ac.edina.cobweb',
            'appActivity': '.MainActivity',
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
        """ Cleanup after each test """
        self.driver.quit()

    def _close_eula(self):
        """ Close the EULA dialog
        """
        self.wait.until(
            EC.element_to_be_clickable((By.ID, CS.APP_EULA_ACCEPT))
        ).click()

    def get_active_page(self):
        """ Return the active page in the app
        """
        return self.get_by_css(CS.APP_ACTIVE_PAGE)

    def change_page(self, page, page_id = None, button_class = None):
        """ If not in the page use the nav button to change pages
        """
        log = logging.getLogger('AppHelper.change_page')

        # If not specific selectors were given assume the convention name
        if not page_id:
            page_id = page + '-page'
        if not button_class:
            button_class = page + '-button'

        log.debug('Finding the active page')
        active_page = self.get_active_page()
        log.debug(dir(active_page))

        if active_page.id is not page_id:
            log.debug('Changing to page: ' + page_id)
            button = active_page.find_element_by_css_selector(
                CS.APP_NAV_BTN_FMT.format(button_class=button_class)
            )
            self.assertTrue(button.is_displayed)
            button.click()

        return self.wait.until(
            EC.presence_of_element_located((By.ID, page_id))
        )

    def login_with(self, username, password):
        """ Log in to the app with the username and password provided
        """
        download_nav_link = self.get_by_css(CS.APP_DOWNLOAD_NAV).click()

        # Get list of active pages before clicking login (opens new page)
        whs = self.driver.window_handles
        cwh = self.driver.current_window_handle

        # Click Login button
        self.get_by_css(CS.APP_LOGIN_LINK).click()
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

        # Wait for successful return
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, CS.APP_LOGOUT_LINK))
            )
        except TimeoutException:
            self.fail("Login did not complete successfuly")
        self.current_user = username

    def sync_surveys(self):
        """ Synchronise the registered surveys
        """
        # Wait for return back to logged in Download page, click Download button
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, CS.APP_SYNC_BUTTON))
        ).click()

        sleep(3)

        self.wait.until(
            EC.invisibility_of_element_located((By.ID, 'download-popup-popup'))
        )

    def sync_public_survey(self, survey):
        """ Sync to a particular public survey
        """
        # Check if we are on the download page already, if not click it
        if not self.check_exists(self.get_by_id, "download-page"):
            self.get_by_css(CS.APP_DOWNLOAD_NAV).click()
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CS.APP_DL_PUB))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, CS.APP_PUB_LIST))
        )
        self.get_by_xpath(CS.PUBLIC_FILTER).send_keys(survey.name[:7])
        switch_xpath = '//input[@data-editor-name="%s.edtr"]'%survey.id
        switch = self.wait.until(
            EC.presence_of_element_located((By.XPATH, switch_xpath))
        )
        the_link = switch.find_element_by_xpath('..')
        if not switch.is_selected():
            the_link.click()
        else:
            the_link.click()
            sleep(0.5)
            the_link.click()
        # wait for sync to dissapear
        sleep(0.5)
        self.wait.until(
            EC.invisibility_of_element_located((By.ID, CS.APP_PUB_DL_POPUP))
        )
        self.assertEqual(switch.is_selected(), True, "Failed to sync public survey")

    def close_eula_login_sync_surveys(self, username, password):
        """ Convenience to close eula, login and sync all in one
        """
        self._close_eula()
        self.login_with(username, password)
        self.sync_surveys()

    def make_observation(self, survey, observation_text):
        """ Make an observation to a survey using the provided text
        """
        log = logging.getLogger('AppHelper.make_observation')
        log.debug("Making observation on %s as %s"%(survey.name, self.current_user))
        observation_name = self._begin_observation(survey)

        text_input = self.get_by_css(CS.APP_TEXT_OBS_2)
        text_input.send_keys(observation_text)
        self.driver.find_element_by_css_selector(CS.APP_RECORD_OBS).click()

        # Wait for GPS fix warning to appear, then dissappear - or not!
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))
        self.long_wait.until(EC.invisibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))

        # Save observation (without moving it)
        self.get_by_id(CS.APP_SAVE_OBS).click()

        # Upload observations
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.APP_LIST_OBS))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.APP_OBS_UPLOAD))
        ).click()

        # Wait for confirm box to appear and dissapear
        sleep(3)

        # Check our observation is uploaded
        obs_link = self.get_by_xpath('//a[text()="%s"]'%observation_name)
        tick_div = obs_link.find_element_by_xpath('../../div[1]')
        self.assertIn("saved-records-list-synced-true",
                      tick_div.get_attribute("class"))
        log.debug("Made observation %s"%observation_name)
        return observation_name

    def make_simple_observation(self, survey):
        """ Make an image observation on the survey

            This will just select the first image from recent list
        """
        observation_name = self._begin_observation(survey)

        # Fill image observation
        self.driver.find_element_by_css_selector(CS.APP_RECORD_OBS).click()

        # Wait for GPS fix warning to appear, then dissappear - or not!
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))
        self.long_wait.until(EC.invisibility_of_element_located((By.XPATH, CS.APP_GPS_SYNC)))

        # Save observation (without moving it)
        self.get_by_id(CS.APP_SAVE_OBS).click()

        # Upload observations
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.APP_LIST_OBS))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, CS.APP_OBS_UPLOAD))
        ).click()

        # Wait for confirm box to appear and dissapear
        sleep(3)

        # Check our observation is uploaded
        obs_link = self.get_by_xpath('//a[text()="%s"]'%observation_name)
        tick_div = obs_link.find_element_by_xpath('../../div[1]')
        self.assertIn("saved-records-list-synced-true",
                      tick_div.get_attribute("class"))

        return observation_name


    def _begin_observation(self, survey):
        """ Starts an observation, returns the observation name
        """
        log = logging.getLogger('AppHelper._begin_observation')
        # Check if we are at capture page, if not, take us there!
        if not self.check_exists(self.get_by_id, "capture-page"):
            capture_links = self.list_by_xpath('//a[contains(., "Capture")]')
            # WHY MORE THAN ONE!?
            for link in capture_links:
                try:
                    link.click()
                except ElementNotVisibleException:
                    log.debug("Found invisible 'capture' link")
                else:
                    log.debug("Got visible capture link")
                    break

            self.wait.until(
                EC.visibility_of_element_located((By.ID, CS.APP_CAP_VIEW))
            )

        # Check if there are some surveys
        found_surveys = self.list_by_css(CS.APP_SURVEY_LINKS)
        # Find and click our survey
        survey_ids = [el.get_attribute("data-editor-type").split('.')[0] for el in found_surveys]

        log.debug('Looking for survey %s'%survey)
        log.debug('looking in %s'%survey_ids)

        self.assertIn(survey.id, survey_ids, "Survey not in synced list")
        found_surveys[survey_ids.index(survey.id)].click()

        # Name the observation, return to be stored as global to check later
        observation_name = "App%s"%random.randint(0, 99999)

        # Make an observation - use text fields
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, CS.APP_TEXT_OBS_1))
            ).send_keys(observation_name)
        except TimeoutException:
            self.fail("Failed to bring up observation page for survey")

        return observation_name
