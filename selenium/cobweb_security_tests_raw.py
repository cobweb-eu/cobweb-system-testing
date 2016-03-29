""" This is a python script to automate the testing of the security
    model within cobweb for raw observations. This will test the backend
    services (WFS/WMS) and then check the front end components.

    For public surveys:
        All users should be able to see all submitted observations
    For private surveys:
        Non-memeber: see own observations only
        Member: see all observations
        Coord: see all observations

"""

import json
import unittest
import logging
import sys

from selenium import webdriver
from time import sleep

from utils.helpers import SurveyHelper, AppHelper
from utils import statics as CS
from utils import Survey, convert_from_friendly_name, CobwebUser

# STATIC TEST CONFIGURATION

group1 = "SecGroup1"
group2 = "SecGroup2"

# Use below for pre-existing surveys, instead of creating during setUp()
SURVEYS_EXIST = True
PUB_SURVEY = Survey('b7e0e8d5-1f87-4dd5-b18d-1fe43d324987', 'ObsTestPublic 2015-07-14 11:38:16.098855')
PRIV_SURVEY = Survey('e08aeaf8-640c-4135-b66a-e81d3d733800', 'ObsTestPrivate 2015-07-14 11:37:47.980029')

# Use below for pre-existing observations, instead of performing during setUp()
OBSERVATIONS_EXIST = True
PUB_OBS_NAME = 'App50164'
PRIV_OBS_NAME_A = 'App89348'
PRIV_OBS_NAME_B = 'App84673'

# The text that will be sent as the observed value
PUB_OBS_TEXT = CS.OBSERVATION_TEXT

# TEST SEQUENCE
# Create public survey
# Join and make observations
# Check coord can see observations
# Check user can see observations
# Check non-logged in user can see observations
# Create Registered survey
# Join and make observations as 2 users: A,B
# User B leaves survey
# Check A can see all observations
# Check coord can see all observations
# Check B can only see own observation
# (Check C can see nothing?)

class RawObservationTests(SurveyHelper):
    """ A class providing tests to check RAW observation visibility
        matches the defined security model for RAW observations in COBWEB

        Currently this is:
            Public surveys: All users see all observations, logged in or not
            Private surveys: Members see own observations, otherwise
            they see only their own
    """

    def setUp(self):
        """ Perform initialisation per test
            This function is called by unittest
        """
        # Store the current test
        log = logging.getLogger('RawObservationTests.setUp')
        log.debug('Setting up for %s'%self.id().split('.')[-1])

        self.USERNAME = 'sebclarke'
        self.PASSWORD = 'password'
        self.driver = webdriver.Chrome()
        self.user_a = CobwebUser('AutoIntegrationTestUser1', 'password', '11e9251a-0f64-d597-575b-9fd702ba0ab5')
        self.user_b = CobwebUser('AutoIntegrationTestUser2', 'password', '38f88da7-6550-076a-935a-ea22242258df')
        super(RawObservationTests, self).setUp()

        # Sign in with self.USERNAME
        self._accept_cookie_sign_in()

        if not SURVEYS_EXIST:
            # Create and author a private survey
            self.private_survey = self._create_survey("ObsTestPrivate", group1, CS.SURVEY_ABSTRACT)
            self._author_survey(self.private_survey)
            # Create and author public survey
            self.public_survey = self._create_public_survey("ObsTestPublic", group2, CS.SURVEY_ABSTRACT)
            self._author_survey(self.public_survey)

            # Logout from admin user, join the private survey as both users
            self.driver.get(CS.PRIV_URL)
            self._logout()
            self._login_with(self.user_a.id, self.user_a.pw)
            self._join_survey(self.private_survey)
            self._logout()
            self._login_with(self.user_b.id, self.user_b.pw)
            self._join_survey(self.private_survey)
            sleep(10) # in order to allow membership to propogage
        else:
            # Use the configured existing surveys
            self.private_survey = PRIV_SURVEY
            self.public_survey = PUB_SURVEY

        if not OBSERVATIONS_EXIST:
            # Start the app, sync surveys, and make observations
            self.pub_obs_name = self._perform_public_observation(
                self.user_a,
                self.public_survey,
                PUB_OBS_TEXT
            )
            self.priv_obs_name_a = self._perform_private_observation(
                self.user_a,
                self.private_survey,
                PUB_OBS_TEXT
            )
            self.priv_obs_name_b = self._perform_private_observation(
                self.user_b,
                self.private_survey,
                PUB_OBS_TEXT
            )
            self._remove_user_from_group(self.user_b, group1)
        else:
            self.pub_obs_name = PUB_OBS_NAME
            self.priv_obs_name_a = PRIV_OBS_NAME_A
            self.priv_obs_name_b = PRIV_OBS_NAME_B

    def tearDown(self):
        """ Perform cleanup after each test
            This function called by unittest
        """
        if not SURVEYS_EXIST:
            self._delete_survey(self.public_survey)
            self._delete_survey(self.private_survey)
        super(RawObservationTests, self).tearDown()


    def _perform_public_observation(self, user, survey, text):
        """ Perform an observation on a public survey

            This establishes an app instance, logs in,
            enables the survey in question, then performs
            the observation. Finishes by closing the AppHelper.
        """
        appHelper = AppHelper()
        appHelper.setUp()
        appHelper._close_eula()
        appHelper.login_with(user.id, user.pw)
        appHelper.sync_public_survey(survey)
        obs_name = appHelper.make_observation(survey, text)
        appHelper.tearDown()
        return obs_name

    def _perform_private_observation(self, user, survey, text):
        """ Perform an observation on a public survey

            This establishes an app instance, logs in,
            syncs the registered surveys, then performs
            the observation. Finishes by closing the AppHelper.
        """
        appHelper = AppHelper()
        appHelper.setUp()
        appHelper.close_eula_login_sync_surveys(user.id, user.pw)
        obs_name = appHelper.make_observation(survey, text)
        appHelper.tearDown()
        return obs_name

    def test_observation_visibility(self):
        """ Test that observations conform to the correct security model.
            Test through WFS/WMS and browser.
        """
        # Check that anon user can see public observation - WFS
        self.check_public_observation_wfs(self.public_survey, self.pub_obs_name)

        # Check that UserA can see both private observations
        self.check_private_observation_wfs(self.private_survey, self.priv_obs_name_a, self.user_a.id)


class PublishAuthorSyncTest(SurveyHelper):
    """ Class to help test whether the order of Create-Author-Publish
        has an effect on survey visibility on the app
    """
    def setUp(self):
        self.USERNAME = 'sebclarke'
        self.PASSWORD = 'password'
        self.driver = webdriver.Chrome()
        super(PublishAuthorSyncTest, self).setUp()
        self._accept_cookie_sign_in()

    def test_create_author_publish(self):
        self.survey_pre_author = self._create_survey("AuthorFirst")
        self._author_survey(self.survey_pre_author)
        self._publish_survey(self.survey_pre_author)

    def test_create_publish_author(self):
        self.survey_pre_publish = self._create_public_survey("PublishFirst")
        self._author_survey(self.survey_pre_publish)


def suite():
    """ Define what tests to run and the order in
        which they shall be executed for this test
    """

    # set up logging to debug the tests
    logging.basicConfig(stream=sys.stderr)
    #logging.getLogger('SurveyHelper._check_features_contain_observation').setLevel(logging.DEBUG)
    logging.getLogger('SurveyHelper.check_private_observation_wfs').setLevel(logging.DEBUG)
    #logging.getLogger('AppHelper.make_observation').setLevel(logging.DEBUG)
    #logging.getLogger('AppHelper._begin_observation').setLevel(logging.DEBUG)
    # add tests to suite
    suite = unittest.TestSuite()
    suite.addTest(RawObservationTests('test_observation_visibility'))
    #suite.addTest(RawObservationTests('test_remove_user'))
    #suite.addTest(PublishAuthorSyncTest('test_create_author_publish'))
    #suite.addTest(PublishAuthorSyncTest('test_create_publish_author'))
    return suite

def load_tests(loader, standard_tests, pattern):
    return suite()

if __name__ == '__main__':
    unittest.main()
