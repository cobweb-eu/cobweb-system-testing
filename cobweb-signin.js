// Test script to perform a user login on the portal, produces screen captures to show before and after
// Re-factored to use xpath to locate elements and to use waitFor to speed up execution.
// Simpler tests using xpath should mean better reporting and more reliable operation

var firstUrl;
var x = require('casper').selectXPath;

var XPATH_LOGIN_LINK = '//a[text()=" Login"]';
var XPATH_LOGOUT_LINK = '//a[text()=" Logout"]';
var XPATH_COBWEB_IDP_BUTTON = '//button[1]';
var XPATH_COOKIE_ACCEPT = '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[1]/p[3]/span[1]';

casper.test.begin('Test login functionality', 8, function suite(test) {
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
		    'j_username' : 'sebclarke', // enter your username here
		    'j_password' : 'password' // enter your password here
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
    
    
    casper.then(function() {
        casper.capture("./logged_in_new.png");
    });
    
	// Run all tests and finish
	casper.run(function() {
        test.done();
    });
	
	phantom.clearCookies();
});
