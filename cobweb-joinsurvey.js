// Test script to join a survey on the portal, produces screen captures to show before and after

var firstUrl;
var x = require('casper').selectXPath;

var XPATH_LOGIN_LINK = '//a[text()=" Sign in"]';
var XPATH_LOGOUT_LINK = '//a[text()=" Sign out"]';
var XPATH_COBWEB_IDP_BUTTON = '//button[1]';
var XPATH_COOKIE_ACCEPT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[1]/p[3]/span[1]';
var XPATH_SURVEY_LINK = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[1]/div/div/div[3]/div/div/div[3]/div[11]/div/div[3]/a';
var XPATH_JOIN_SURVEY_BUTTON = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[4]/div[2]/div/a';
var XPATH_PARTICIPATING_ON_SURVEY = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[4]/div/div[4]/div[2]/div/a/span[3]';

casper.test.begin('Test join survey functionality', 11, function suite(test) {
	casper.start('https://dyfi.cobwebproject.eu');
	
    casper.then(function () {
        this.viewport(1920, 1200);
    });
    
    // this may help mitigate no logout visible bug
	casper.thenClick(x(XPATH_COOKIE_ACCEPT), function() {
	    console.log("Accepting cookie policy");
	});
	    	
	casper.then(function() {
		this.test.assertVisible({
		    type: 'xpath',
			path: XPATH_LOGIN_LINK
		}, 'Login link found');
		
		this.test.assertNotVisible({
		    type: 'xpath',
			path: XPATH_LOGOUT_LINK
		}, 'No logout link');
   
		firstUrl = this.getCurrentUrl();
	});
		    
	casper.thenClick(x(XPATH_LOGIN_LINK), function() {
        console.log("Clicked login link");
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.test.pass('WAYF Page Loaded');
        }, function timeout() {
            casper.test.fail('Timed out waiting for WAYF page to load (5s)', {name: 'WAYF Page Loaded'});
        }
    );
		
    casper.then(function() {
		this.test.assertExists({
		    type: 'xpath',
			path: XPATH_COBWEB_IDP_BUTTON
		}, 'COBWEB IDP button found');
		firstUrl = this.getCurrentUrl();
    });
    
	casper.thenClick(x(XPATH_COBWEB_IDP_BUTTON), function() {
        console.log("Clicked COBWEB IDP button");
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.test.pass("COBWEB Login page loaded");
        }, function timeout() {
            casper.test.fail("Timed out waiting for COBWEB login page to load (5s)", {name: 'COBWEB Login page loaded'});
        }
    );

	casper.then(function() {
		// Complete the login form
		console.log('Posting to login form');
		firstUrl = this.getCurrentUrl();
        this.fill('form#login', {
		    'j_username' : '', // enter your username here
		    'j_password' : '' // enter your password here
		}, true);
    });
    
    casper.waitFor(
        function check() {
            return this.getCurrentUrl() != firstUrl;
        }, function then() {
            casper.test.pass("Login form returned");
        }, function timeout() {
            caspter.test.fail("Timed out waiting for login form to return(5s)", {name: 'Login form returned'});
        }
    );
   
    // try click the login link again because of bug!
    casper.thenClick(x(XPATH_LOGIN_LINK), function() {
        console.log("Clicked login link again");
    });
    
    casper.then(function() {
        console.log('Looking for logout link');
		this.test.assertVisible({
		    type: 'xpath',
			path: XPATH_LOGOUT_LINK
		}, 'logout link found');
		
		this.test.assertNotVisible({
		    type: 'xpath',
			path: XPATH_LOGIN_LINK
		}, 'Login link not visible');
    });
    
    
	casper.then(function(){
		console.log('Looking for first survey link');
		this.test.assertVisible({
			type: 'xpath',
			path: XPATH_SURVEY_LINK
		}, 'First survey link found');
	});
	
	casper.thenClick(x(XPATH_SURVEY_LINK), function() {
        console.log("Clicked first survey link");
    });
	
	casper.waitFor(
        function check() {
			var surveyUrl = this.getCurrentUrl();
			return surveyUrl.indexOf("metadata") > -1;
			
        }, function then() {
            casper.test.pass("Survey page returned");
        }, function timeout() {
            caspter.test.fail("Timed out waiting for survey page to return(5s)", {name: 'Survey page returned'});
        }
    );
	
	casper.then(function(){
		console.log('Looking for join survey button');
		this.test.assertVisible({
			type: 'xpath',
			path: XPATH_JOIN_SURVEY_BUTTON
		}, 'Join survey button found');
	});
	
	casper.thenClick(x(XPATH_JOIN_SURVEY_BUTTON), function() {
        console.log("Clicked join survey button");
    });
	
	
	casper.waitUntilVisible(x(XPATH_PARTICIPATING_ON_SURVEY), function() {
        this.echo('User is participating on survey.');
    });
	
    casper.then(function() {
        casper.capture("./joined_survey_display.png");
    });
    
	// Run all tests and finish
	casper.run(function() {
        test.done();
    });
	
	phantom.clearCookies();
});
