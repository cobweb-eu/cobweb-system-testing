// Script to test the first part of the registered user use-case
// This script will log in to the portal, create a survey, add some questions and save it

// useful environment variables
var x = require('casper').selectXPath;
var mouse = require('mouse').create(casper);

// base name for our testing surveys
var TEST_SURVEY_TITLE_BASE = "RegUseCase Test Survey ";

// XPath selectors for our elements
var XPATH_COOKIE_ACCEPT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[1]/p[3]/span[1]';
var XPATH_LOGIN_LINK = '//a[text()=" Sign in"]';
var XPATH_LOGOUT_LINK = '//a[text()=" Sign out"]';
var XPATH_COBWEB_IDP_BUTTON = '//button[1]';
var XPATH_ADD_NEW_RECORD_LINK = '//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/ul/li[5]/a'
var XPATH_ADD_CONTENT_BUTTON = '//span[text()="Create..."]';
var XPATH_SURVEY_DATASET_SELECTOR = '//*[@id="template-survey"]';
var XPATH_SURVEY_TEMPLATE_SELECTOR = '//a[text()="Biodiversity (default survey template)"]';
var XPATH_SURVEY_TEMPLATES_LIST = '//*[@id="gn-new-metadata-container"]/div[3]/div[2]/div/div[2]/div';
var XPATH_GROUP_NAME_INPUT = '//*[@id="groupName"]';
var XPATH_SURVEY_CREATE_BUTTON = '//*[@id="gn-new-metadata-container"]/div[3]/div[4]/div/button[1]';
var XPATH_SURVEY_METADATA_FORM = '//*[@id="gn-el-16"]';
var XPATH_SURVEY_TITLE_INPUT = '//*[@id="gn-field-21"]';
var XPATH_SURVEY_METADATA_SAVECLOSE_BUTTON = '//*[@id="ng-app"]/body/div[2]/div[3]/div[1]/nav/div[2]/button[5]';
var XPATH_SURVEY_EDITOR_LIST_LINK = '//a[text()="TEMP"]';
var XPATH_SURVEY_DETAIL_TITLE = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[2]/div[1]/h2';
var XPATH_AT_SURVEY_TITLE = '//*[@id="form_title"]';
var XPATH_AUTH_TOOL_BUTTON = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[4]/div[2]/a[2]';
var XPATH_AT_TITLE_EDIT = '//*[@id="fieldcontain-text-1"]/div[4]/a';
var XPATH_AT_OPTIONS_DIALOG = '/html/body/div[8]';
var XPATH_AT_TEXT_TITLE = '//*[@id="text_title"]';
var XPATH_AT_OPTIONS_SUBMIT_BUTTON = '/html/body/div[8]/div[11]/div/button[1]';
var XPATH_AT_IMAGE_CAP_WIDGET = '//*[@id="elements"]/li[7]';
var XPATH_AT_DROPPABLE_AREA = '//*[@id="form-content"]';
var XPATH_AT_IMAGE_TITLE_INPUT = '//*[@id="image_title"]';
var XPATH_AT_SAVE_BUTTON = '//a[text()="Save As"]';
var XPATH_AT_SAVE_CONFIRM_DIALOG = '//*[@id="feedback"]';
var XPATH_AT_SAVE_CONFIRM_CLOSE_BUTTON = '//*[@id="feedback"]/div[1]/button';
var XPATH_AT_SAVE_STATUS = '//*[@id="sync_status"]';
var XPATH_SURVEY_LIST_AREA = '//*[@id="ng-app"]/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/table';
var XPATH_METADATA_SAVE_BUTTON = '//*[@id="ng-app"]/body/div[2]/div[3]/div[1]/nav/div[2]/div[3]/button[1]';
var XPATH_METADATA_FADE_BACKDROP = '//*[@id="ng-app"]/body/div[2]/div[2]/div[2]/div[1]';
var XPATH_METADATA_ABSTRACT_INPUT = '//*[@id="gn-field-29"]';

// global scope variables
var firstUrl;
var test_run_time = new Date();
var test_survey_title = TEST_SURVEY_TITLE_BASE.concat(test_run_time.toString());

// start the tests!
casper.test.begin('Registered user use-case test', 34, function suite(test) {
    casper.start('https://dyfi.cobwebproject.eu');
   
    // set up the viewport for screen capping
    casper.then(function () {
        this.viewport(1920, 1200);
    }); 
    
    // test correct page has loaded
    casper.then(function() {
        test.assertTitle("COBWEB Dyfi Biosphere Reserve Portal (Beta) - Cobweb", "Portal homepage displayed");
        casper.capture('image_output/1_Start_Page.png');
    });
    
    casper.then(function() {
       this.test.assertExists({
		    type: 'xpath',
			path: '//div[@class="cookie-warning"]'
		}, 'Cookie warning displayed');
    });
    
    // accept the cookie policy
	casper.thenClick(x(XPATH_COOKIE_ACCEPT), function() {
	    console.log("Accepting cookie policy");
        firstUrl = this.getCurrentUrl();
	});    
	
	// click the login link
    casper.thenClick(x(XPATH_LOGIN_LINK), function() {
        console.log("Clicked login link");
    });	
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.capture('image_output/2_WAYF_Page_Pass.png');
            casper.test.pass('WAYF Page Loaded');
        }, function timeout() {
            casper.capture('image_output/2_WAYF_Page_Fail.png');
            casper.test.fail('Timed out waiting for WAYF page to load (5s)', {name: 'WAYF Page Loaded'});
        }
    );
    
    casper.thenClick(x(XPATH_COBWEB_IDP_BUTTON), function() {
        console.log("Clicked COBWEB IDP button");
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.capture('image_output/3_COBWEB_Login_Page_Pass.png');
            casper.test.pass('COBWEB Login page displayed');
            firstUrl = this.getCurrentUrl();
        }, function timeout() {
            casper.capture('image_output/3_COBWEB_Login_Page_Fail.png');
            casper.test.fail('Timed out waiting for COBWEB Login to load (5s)', {name: 'COBWEB Login page displayed'});
        }
    );
    
    casper.then(function() {
		// Complete the login form
		console.log('Posting to login form');
		firstUrl = this.getCurrentUrl();
        this.fill('form#login', {
		    'j_username' : 'sebclarke', // enter your username here
		    'j_password' : 'password' // enter your password here
		}, true);
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            console.log("Login form returned");
            firstUrl = this.getCurrentUrl();
        }
    );
    
    casper.then(function() {
        casper.capture('image_output/4_Logged_in.png');
        this.test.assertVisible({
	        type: 'xpath',
		    path: XPATH_LOGOUT_LINK
	    }, 'Successfully logged in');
    });
    
    // Assert we have the capability to create new surveys
    casper.then(function() {
        this.test.assertVisible({
            type: 'xpath',
			path: XPATH_ADD_NEW_RECORD_LINK
        }, 'Add record link found');
        firstUrl = this.getCurrentUrl();
    });
    
    // click the editor icon
    casper.thenClick(x(XPATH_ADD_NEW_RECORD_LINK), function() {
        console.log("Clicked add new record");
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.capture('image_output/5_Metadata_list_page_Pass.png');
            casper.test.pass("Main editor page loaded");
        }, function timeout() {
            casper.capture('image_output/5_Metadata_list_page_Fail.png');
            casper.test.fail("Timed out waiting for editor page(5s)", {name: 'Main editor page loaded'});
        }
    );
    
    // assert we can see the 'Add content' button
    casper.then(function() {
        this.test.assertVisible({
            type: 'xpath',
			path: XPATH_ADD_CONTENT_BUTTON
        }, 'Add content button found');
        firstUrl = this.getCurrentUrl();
    });
    
    // click add content
    casper.thenClick(x(XPATH_ADD_CONTENT_BUTTON), function() {
        console.log("Clicked add content button");
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.test.pass("Survey creation page loaded");
        }, function timeout() {    
            casper.test.fail("Timed out waiting for survey creation page (5s)", {name: 'Survey creation page loaded'});
        }
    );
    
    // we need to wait for the assets to load!
    casper.then(function() {
	    this.waitForSelector(x(XPATH_SURVEY_DATASET_SELECTOR),
	        function pass() {
    	        casper.capture('image_output/6_Survey_Creator_Page_Pass.png');
	            casper.test.pass("Survey dataset asset loaded");
	        },
	        function fail() {
                casper.capture('image_output/6_Survey_Creator_Page_Fail.png');
	            casper.test.fail("Survey creation page did not finish loading assets", {name: "Survey dataset asset loaded"});
	        }
	    );
    });
    
    // assert exists and select survey element
    casper.then(function() {
        this.test.assertVisible({
            type: 'xpath',
			path: XPATH_SURVEY_DATASET_SELECTOR
        }, 'Survey dataset is visible');
    });
    
    casper.thenClick(x(XPATH_SURVEY_DATASET_SELECTOR), function() {
        console.log("Selected survey dataset");
    });
    
    // assert the templates are shown
    casper.then(function() {
        this.test.assertVisible({
            type: 'xpath',
			path: XPATH_SURVEY_TEMPLATES_LIST
        }, 'Survey templates are displayed');
    });
    
    casper.thenClick(x(XPATH_SURVEY_TEMPLATE_SELECTOR), function() {
        console.log("Selected Biological Monitoring template");
    });

    // assert the new group name box and create button exist
    casper.then(function() {
		this.test.assertExists({
			type: 'xpath',
			path: XPATH_GROUP_NAME_INPUT
		}, 'Group name input box exists');
	});
	
    casper.then(function() {
		this.test.assertVisible({
            type: 'xpath',
			path: XPATH_SURVEY_CREATE_BUTTON
        }, 'Survey create button is visible');
    });

    // fill the form, press the submit button
    casper.then(function() {
	    var valueForGroup = 'RegUseCase Test Group';
	    var fields = {};
	    fields[XPATH_GROUP_NAME_INPUT] = valueForGroup;
		this.fillXPath('form', fields, false);
		firstUrl = this.getCurrentUrl();
        casper.capture('image_output/7_Survey_Creator_Filled.png');
    });
    
    casper.thenClick(x(XPATH_SURVEY_CREATE_BUTTON), function() {
        console.log("Filled form and clicked 'Create'");
    });

    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.test.pass("Survey created ok");
        }, function timeout() {
            casper.test.fail("Timed out waiting for survey creation (5s)", {name: 'Survey created ok'});
        }
    );
    
    // wait for all resources to load!
    casper.then(function() {
	    this.waitForSelector(x(XPATH_SURVEY_METADATA_FORM),
	        function pass() {
	            casper.capture('image_output/8_Metadata_editor_page_Pass.png');
	            casper.test.pass("Survey metadata editor loaded ok");
	        },
	        function fail() {
	            casper.capture('image_output/8_Metadata_editor_page_Fail.png');
	            casper.test.fail("Survey metatdata editor failed to laod", {name: "Survey metadata editor loaded ok"});
	        }
	    );
    });
    
    // find and open the survey metadata editor   
    casper.then(function() {
		this.test.assertVisible({
			type: 'xpath',
			path: XPATH_SURVEY_TITLE_INPUT
		}, 'Survey title input visible');
		
		this.test.assertVisible({
            type: 'xpath',
			path: XPATH_SURVEY_METADATA_SAVECLOSE_BUTTON
        }, 'Survey metadata save and close button exists');
        
        this.test.assertVisible({
            type: 'xpath',
			path: XPATH_METADATA_SAVE_BUTTON
        }, 'Survey metadata save button exists');
	});
    
    casper.then(function() {
        var fields = {};
	    fields[XPATH_SURVEY_TITLE_INPUT] = test_survey_title;
	    fields[XPATH_METADATA_ABSTRACT_INPUT] = "Auto-created test survey from Registered Use Case auto system test";
		this.fillXPath('form', fields, false);
        casper.capture('image_output/9_Metadata_editor_page_filled.png');
    });
    
    casper.thenClick(x(XPATH_METADATA_SAVE_BUTTON), function() {
        console.log("Clicked Save on survey metadata editor");
    });
    
    casper.then(function() {
        this.waitWhileVisible(x(XPATH_METADATA_FADE_BACKDROP),
            function then() {
	            casper.capture('image_output/9_Metadata_editor_saved_Pass.png');
                casper.test.pass("Survey renamed successfully");
            },
            function onTimeout() {
                casper.capture('image_output/9_Metadata_editor_saved_Fail.png');
                casper.test.fail("Timed out saving the survey", {name: "Survey renamed successfully"});
            }
        );
    });
    
    // load survey metadata list again manually?
    casper.thenOpen('https://dyfi.cobwebproject.eu/geonetwork/private/eng/catalog.edit', function() {
        console.log('refreshing the metadata survey list');
    });
    
    // wait for all resources to load!
    casper.then(function() {
	    this.waitForSelector(x(XPATH_SURVEY_LIST_AREA),
	        function pass() {
                casper.capture('image_output/10_Metadata_list_new_survey_Pass.png');
	            casper.test.pass("Survey metadata list loaded ok");
	        },
	        function fail() {
                casper.capture('image_output/10_Metadata_list_new_survey_Fail.png');
	            casper.test.fail("Timed out waiting for survey metatdata editor to load (5s)", {name: "Survey metadata list loaded ok"});
	        }
        );
    });
   
    // assert we can find the survey in the list    
    var xpath_survey_list_link = '//a[text()="REPLACE"]'.replace("REPLACE", test_survey_title);
    casper.then(function() {
        casper.capture('SurveyList.png');
        this.test.assertExists({
			type: 'xpath',
			path: xpath_survey_list_link
		}, 'Found survey title in backend');
		firstUrl = this.getCurrentUrl();
    });
    
    // click on the survey
    casper.thenClick(x(xpath_survey_list_link), function() {
        console.log("Clicked on newly renamed survey");
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            this.test.assertSelectorHasText({
                type: 'xpath',
                path: XPATH_SURVEY_DETAIL_TITLE
            }, " ".concat(test_survey_title), 'Loaded survey page ok');
            casper.capture('image_output/11_Survey_Detail_Page_Pass.png');
        }, function timeout() { 
            casper.capture('image_output/11_Survey_Detail_Page_Fail.png');
            casper.test.fail("Timed out waiting for survey page (5s)", {name: 'Loaded survey page ok'});
        }
    );
    
    // click on the authoring tool
    casper.then(function() {
        this.test.assertVisible({
			type: 'xpath',
			path: XPATH_AUTH_TOOL_BUTTON
		}, 'Found survey designer button');
		firstUrl = this.getCurrentUrl();
    });
    
    casper.thenClick(x(XPATH_AUTH_TOOL_BUTTON), function() {
        console.log("Clicked on survey designer");
    });
    
    casper.waitForPopup(/cobweb-authoring-tool/, 
        function then() {
            casper.test.pass('Suvey designer pop-up launched');
        },
        function onTimeout() {
            casper.test.fail("Timed out waiting for survey designer", {name: 'Suvey designer pop-up launched'});
        }
    );
    
    casper.withPopup(/cobweb-authoring-tool/, function() {
    
        casper.viewport(1920, 1200).then(function() {
            casper.capture('image_output/12_Survey_Designer_Popup.png');
        });
        
        this.test.assertSelectorHasText({
            type: 'xpath',
            path: XPATH_AT_SURVEY_TITLE
        }, test_survey_title, 'Survey designer loaded for survey');
        
        casper.then(function() {
            this.test.assertVisible({
			    type: 'xpath',
			    path: XPATH_AT_TITLE_EDIT
		    }, 'Found pen icon for first question');
        });
        
        casper.thenClick(x(XPATH_AT_TITLE_EDIT), function() {
            console.log("Clicked pen to edit first question");
        });
        
        casper.then(function() {
            casper.capture('image_output/13_Survey_Designer_edit_title.png');
            this.test.assertVisible({
			    type: 'xpath',
			    path: XPATH_AT_OPTIONS_DIALOG
		    }, 'Widget options dialog displayed');
        });
        
        casper.then(function() {
            this.test.assertVisible({
			    type: 'xpath',
			    path: XPATH_AT_TEXT_TITLE
		    }, 'Text question title input found');
        });
        
        casper.then(function() {
            console.log("Filling text question title field");
            var fields = {};
	        fields[XPATH_AT_TEXT_TITLE] = "Your Name";
		    this.fillXPath('form', fields, false);
		    casper.capture('image_output/14_Survey_Designer_edit_title_filled.png');
        });
        
        casper.then(function() {
            this.test.assertVisible({
			    type: 'xpath',
			    path: XPATH_AT_OPTIONS_SUBMIT_BUTTON
		    }, 'Widget option submit button found');
        });
        
        casper.thenClick(x(XPATH_AT_OPTIONS_SUBMIT_BUTTON), function() {
            console.log("Clicked widget options submit button");
            casper.capture('image_output/15_Survey_Designer_edit_title_submitted.png');
        });
        
        // DRAG AND DROP CODE
        casper.then(function() {
            console.log("Attempting to drag photo capture widget");
            mouse.down(x(XPATH_AT_IMAGE_CAP_WIDGET));
            mouse.move(x(XPATH_AT_DROPPABLE_AREA));
            mouse.up(x(XPATH_AT_DROPPABLE_AREA));
        });
        
        casper.then(function() {
            casper.capture('image_output/16_Survey_Designer_added_photo.png');
            this.test.assertVisible({
			    type: 'xpath',
			    path: XPATH_AT_IMAGE_TITLE_INPUT
		    }, 'Image capture title input found');
        });
        
        casper.then(function() {
            console.log("Filling image capture title field");
            var fields = {};
	        fields[XPATH_AT_IMAGE_TITLE_INPUT] = "Take Picture!";
		    this.fillXPath('form', fields, false);
		    casper.capture('image_output/17_Survey_Designer_photo_filled.png');
        });
        
        casper.thenClick(x(XPATH_AT_OPTIONS_SUBMIT_BUTTON), function() {
            console.log("Clicked widget options submit button");
            casper.capture('image_output/18_Survey_Designer_photo_saved.png');
        });
        
        casper.then(function() {
            this.test.assertVisible({
			    type: 'xpath',
			    path: XPATH_AT_SAVE_BUTTON
		    }, 'Survey designer save button found');
        });
        
        casper.thenClick(x(XPATH_AT_SAVE_BUTTON), function() {
            console.log("Clicked survey designer save button");
        });
        
        casper.then(function() {
            this.waitUntilVisible(x(XPATH_AT_SAVE_CONFIRM_DIALOG),
                function then() {
                    casper.capture('image_output/19_Survey_Designer_save_Pass.png');
                    casper.test.pass("Survey saved successfully");
                },
                function onTimeout() {
                    casper.capture('image_output/19_Survey_Designer_save_Fail.png');
                    casper.test.fail("Timed out saving the survey", {name: "Survey saved successfully"});
                }
            );
        });
        
        casper.thenClick(x(XPATH_AT_SAVE_CONFIRM_CLOSE_BUTTON), function() {
            console.log("Clicked close on survey save confirmation");
        });
        
        casper.then(function() {
            casper.capture('image_output/20_Survey_Synchronised.png');
            this.test.assertSelectorHasText({
                type: 'xpath',
                path: XPATH_AT_SAVE_STATUS
            }, 'Synchronized', 'Survey synchronised');
        });   
        
    });
   
    
    // Run all tests and finish
	casper.run(function() {
        test.done();
    });
	
	phantom.clearCookies();
   
});
