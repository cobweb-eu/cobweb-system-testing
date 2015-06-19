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

from cobweb_reg_use_case_tests import SurveyTest, AppTests
from envsys.general.structures import AuthUser
from envsys.testing.cobweb.structures import Survey
from envsys.testing.cobweb import cobweb_statics as CS

PUB_OBS_TEXT = "public observation"

class RawObservationTests(SurveyHelper):
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
        
        # Set up pre-requisites for the test
        self._accept_cookie_sign_in() # Uses self.USERNAME
        
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
        
        # Start the app, sync public survey, and make observation
        
        self.pub_obs_name = self._perform_public_observation(
            self.user_a,
            self.public_survey,
            PUB_OBS_TEXT
        )
        self.priv_obs_name = self._perform_private_observation(
            self.user_a,
            self.private_survey,
            PUB_OBS_TEXT
        )
        
        # 
        
    def _perform_public_observation(user, survey, text):
        appHelper = AppHelper()
        appHelper.setUp()
        appHelper.close_eula()
        appHelper.login_with(user.id, user.pw)
        appHelper.sync_public_survey(survey)
        obs_name = appHelper.make_observation(survey, text)
        appHelper.tearDown()
        return obs_name
    
    def _perform_private_observation(user, survey, text):
        appHelper = AppHelper()
        appHelper.setUp()
        appHelper.close_eula_login_sync_surveys(user.id, user.pw)
        obs_name = appHelper.make_observation(survey, text)
        appHelper.tearDown()
        return obs_name
    

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

