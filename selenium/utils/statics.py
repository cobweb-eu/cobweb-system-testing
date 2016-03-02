# Here we define static urls, text and selectors used by the tests

LIVE_URL = "http://dyfi.cobwebproject.eu"
PRIV_URL = "https://dyfi.cobwebproject.eu/geonetwork/private/eng/catalog.search#/home"
LIVE_TITLE = "COBWEB Dyfi Biosphere Reserve Portal (Beta) - Cobweb"

# Selectors go here - Warning, some are XPath, some are CSS

COOKIE_WARNING = '//div[@class="cookie-warning"]'
COOKIE_ACCEPT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[1]/p[3]/span[1]'
LOGIN_LINK = '//a[text()=" Sign in"]'
IDP_BUTTON = "form#IdPCOBWEB>button"
USER_INPUT = "input[name=j_username]"
PW_INPUT = "input[name=j_password]"
LOGIN_SUBMIT = "form#login>section>button"
LOGOUT_LINK = '//a[text()=" Sign out"]'
CREATION_TOOLBOX = 'a[href="catalog.edit"]'
MY_ITEMS_CHECK = '//*[@id="ng-app"]/body/div[2]/div/div[1]/div[1]/form/div/div/div/span/label/input'
ADD_CONTENT_BUTTON = '//span[text()="addRecord"]'
SURVEY_DATASET_SELECT = "template-survey"
METADATA_SEARCH_INPUT = '//*[@id="gn-any-field"]'
METADATA_SEARCH_GO = '//*[@id="ng-app"]/body/div[2]/div/div[1]/div[1]/form/div/div/div/div/button[1]'
SURVEY_TEMPLATE_SELECT = '//a[text()="Biodiversity (default survey template)"]'
SURVEY_CREATE_BUTTON = '//*[@id="gn-new-metadata-container"]/div[3]/div[4]/div/button[1]'
SURVEY_TITLE_INPUT = '//*[@id="gn-field-21"]'
SURVEY_ABSTRACT = "Auto-created test survey from Registered Use Case auto system test"
SURVEY_GROUP_NAME = 'RegUseCaseTest'
SURVEY_ABSTRACT_INPUT = '//*[@id="gn-field-29"]'
METADATA_SAVE_BUTTON = '//*[@id="ng-app"]/body/div[2]/div[3]/div[1]/nav/div[2]/div[3]/button[1]'
METADATA_SAVECLOSE_BUTTON = '//*[@id="ng-app"]/body/div[2]/div[3]/div[1]/nav/div[2]/button[5]'
METADATA_FADE_BACKDROP = '//*[@id="ng-app"]/body/div[2]/div[2]/div[2]/div[1]'
SURVEY_LIST_AREA = '//*[@id="ng-app"]/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/table'
SURVEY_DETAIL_TITLE = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[2]/div[1]/h2'
AUTH_TOOL_BUTTON = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[5]/div[2]/a[2]'
MAP_LINK = '//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/ul/li[3]/a'
PUBLISH_BUTTON = '//*[@id="ng-app"]/body/div[2]/div[3]/div[1]/nav/div[2]/button[1]'
UNPUBLISH_BUTTON = '//*[@id="ng-app"]/body/div[2]/div[3]/div[1]/nav/div[2]/button[2]'
AT_SURVEY_TITLE = '//*[@id="form_title"]'
AT_TITLE_EDIT = '//*[@id="fieldcontain-text-1"]/div[4]/a'
AT_TEXT_TITLE = 'text_title'
AT_OPTIONS_SUBMIT_BUTTON = '/html/body/div[8]/div[11]/div/button[1]'
AT_TEXT_CAP_WIDGET = 'text'
AT_DROP_AREA = 'form-content'
AT_PLACEHOLDER = 'text_placeholder'
AT_SAVE_BUTTON = '//a[text()="Save As"]'
METADATA_GROUP_NAME = 'groupName'
METADATA_BOUNDBOX = '//*[@id="map-drawbbox-67"]/div/canvas'
AT_SAVE_CONFIRM = 'feedback'
XPATH_SURVEY_EDIT_REL = '../../td[2]/a[1]'
SEARCH_INPUT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[1]/div/div/div[3]/div/div/div[2]/div[2]/div/input'
SEARCH_SUBMIT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[1]/div/div/div[3]/div/div/div[2]/div[2]/div/span/button'
JOIN_LINK = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[5]/div[2]/div/a'
JOINED_CONFIRM = '//span[contains(., "joined this survey")]'
MINIMAP = '//*[@id="map"]/div[1]/div[2]/div[2]/svg'
MINIMAP_OBS_DETAILS = '//*[@id="map"]/div[1]/div[2]/div[4]/div/div[1]/div'
IFRAME = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[5]/div[1]/div[2]/div[2]/div[1]/iframe'
VIEW_ON_MAP = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[5]/div[1]/div[2]/div[2]/div[1]/a'
MAP_CANVAS = '//*[@id="map"]'
MAP_LAYERS = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[3]/div/div/div[4]/button[1]'
CLOSE_LAYERS = '//*[@id="layers"]/div[1]/div[1]/button'
MAP_OBS_DETAILS = '//*[@id="map"]/div[1]/div[2]/div[4]/div/div[1]/div'

ADMIN_CONSOLE = '//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/ul/li[6]/a'
USERS_AND_GROUPS = '//*[@id="ng-app"]/body/div[2]/span/div[1]/div/a[7]'
MANAGE_USERS = '//*[@id="ng-app"]/body/div[2]/div/ul/li[2]/a'
USER_FILTER = '//*[@id="ng-app"]/body/div[2]/div/div/div/div[1]/div/div[2]/input[1]'
PARTICIPANT_LIST = '//*[@id="groups_RegisteredUser"]'
SAVE_USER_BUTTON = '//*[@id="gn-btn-user-save"]'
PUBLIC_FILTER = '//*[@id="editors-list-container"]/form/div/input'
CAP_NAV_TEXT = 'Capture'

NAVBAR_SEARCH = '//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/ul/li[2]/a'
NSEARCH_INPUT = '//*[@id="gn-any-field"]'
NSEARCH_SUBMIT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/form/div/div/div[1]/div[1]/div/div/button[2]'
NSEARCH_CLEAR = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/form/div/div/div[1]/div[1]/div/div/button[3]'
NSEARCH_RESULTS = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[2]/div/div[2]'

CREATION_TOOLBOX_URL = 'https://dyfi.cobwebproject.eu/geonetwork/private/eng/catalog.edit'
SURVEY_DETAIL_URL = 'https://dyfi.cobwebproject.eu/geonetwork/private/eng/catalog.search#/metadata/'

APP_EULA_ACCEPT = 'home-accept-eula'
APP_DOWNLOAD_NAV = 'a.download-button'
APP_CAPTURE_NAV = 'a.capture-button'
APP_LOGIN_LINK = 'div#home-content-login>a'
APP_SYNC_BUTTON = 'div.sync-download-button'
APP_CAP_VIEW = 'capture-page'
APP_SURVEY_LINKS = 'a[data-editor-type]'
APP_TEXT_OBS_1 = "input#form-text-1"
APP_TEXT_OBS_2 = "input#form-text-2"
APP_RECORD_OBS = "input[name=record]"
APP_GPS_SYNC = '/html/body/div[7]/h1'
APP_SAVE_OBS = 'annotate-preview-ok'
APP_LIST_OBS = '//*[@id="map-records-buttons-list"]/a'
APP_OBS_LIST = '//*[@id="saved-records-list"]'
APP_OBS_UPLOAD = '//*[@id="saved-records-page-header-upload"]'
APP_LOGOUT_LINK = '//p[text()="Logout"]'
APP_DL_PUB = 'a.download-public-forms'
APP_PUB_LIST = 'editors-list'
APP_PUB_DL_POPUP = 'download-popup-popup'

URL_LOGOUT = 'https://ds.cobweb.secure-dimensions.de/WAYF/logout?return=https%3A%2F%2Fdyfi.cobwebproject.eu%2FShibboleth.sso%2FLogout%3Freturn%3Dhttps%3A%2F%2Fdyfi.cobwebproject.eu'
TEXT_INPUT_TITLE = "Science Value"
OBSERVATION_TEXT = '3.5'

WFS_PUB_URL = 'https://dyfi.cobwebproject.eu/geoserver/public/wfs'
WFS_SEC_URL = 'https://dyfi.cobwebproject.eu/geoserver/cobweb/wfs'
