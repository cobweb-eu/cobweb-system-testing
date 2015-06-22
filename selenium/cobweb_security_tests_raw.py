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

from envsys.testing.cobweb.helpers import SurveyHelper, AppHelper
from envsys.general.structures import AuthUser
from envsys.testing.cobweb.structures import Survey
from envsys.testing.cobweb import cobweb_statics as CS

# STATIC TEST CONFIGURATION

# Use below for pre-existing surveys, instead of creating during setUp()
SURVEYS_EXIST = False
PUB_SURVEY = Survey('survey-id', 'survey-name')     
PRIV_SURVEY = Survey('survey-id', 'survey-name')

# Use below for pre-existing observations, instead of performing during setUp()
OBSERVATIONS_EXIST = False
PUB_OBS_NAME = 'name of public observation'
PRIV_OBS_NAME_A = 'name of observation on private survey by user a'
PRIV_OBS_NAME_B = 'name of observation on private survey by user b'

# The text that will be sent as the observed value
PUB_OBS_TEXT = "public observation"


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
        self.USERNAME = 'sebclarke'
        self.PASSWORD = 'password'
        self.driver = webdriver.Chrome()
        self.user_a = AuthUser('obstestuser1', 'password')
        self.user_b = AuthUser('obstestuser2', 'password')
        super(RawObservationTests, self).setUp()
        
        # Store the current test
        #currentTest = self.id().split('.')[-1]
        
        # Sign in with self.USERNAME
        self._accept_cookie_sign_in()
                
        if not SURVEYS_EXIST:
            # Create and author a private survey
            self.private_survey = self._create_survey("ObsTestPrivate")
            self._author_survey(self.private_survey)
            # Create and author public survey
            self.public_survey = self._create_survey("ObsTestPublic")
            self._author_survey(self.public_survey)
            self._publish_survey(self.public_survey)
            # Logout from admin user, join the private survey as both users
            self.driver.get(CS.PRIV_URL)
            self._logout()
            self._login_with(self.user_a.id, self.user_a.pw)
            self._join_survey(self.private_survey)
            self._logout()
            self._login_with(self.user_b.id, self.user_b.pw)
            self._join_survey(self.private_survey)
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
        else:
            self.pub_obs_name = PUB_OBS_NAME
            self.priv_obs_name_a = PRIV_OBS_NAME_A
            self.priv_obs_name_b = PRIV_OBS_NAME_B
            
    def tearDown():
        """ Perform cleanup after each test
            This function called by unittest
        """
        if SURVEYS_EXIST:
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
        appHelper.close_eula()
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
        """ Perform the test that the observations conform to the correct
            security model. Test through WFS/WMS and browser.
        """
        # Check that anon user can see public observation
        self.driver.delete_all_cookies()
        self.check_observation_minimap(self.public_survey, self.pub_obs_name)
        # Check user A can see both - NOT GOING TO WORK WITH MINIMAP
        
        

