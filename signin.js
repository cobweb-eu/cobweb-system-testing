// Test script to perform a user login on the portal, produces screen captures to show before and after
var links;
var idpLinks;
var loginButton;
var secondLink;
var loggedInLinks;
var logOutButton;

casper.test.begin('Test the log in function', 4, function suite(test) {
    casper.start('https://dyfi.cobwebproject.eu', function() {
		// Retrieves a list of menu options available in the top bar
		 links = this.evaluate(function() {
        var elements = __utils__.findAll('i');
        return elements.map(function(e) {
            return e.getAttribute('class');
        });
    });
    });
	
	casper.then(function() {
		console.log('looking for user button');
		// This is the button to click to log in within the set of controls returned
		secondLink = links[2];
		// Start building up the control name to use in the button click event
		secondLink = secondLink.replace(/ /g, ".");
		secondLink = 'i.' + secondLink;
		// Check the button exists
		this.test.assertExists(secondLink);
		// Click the button
		this.click(secondLink);
	});
	
	
	
	casper.wait(3000, function(){
		// Checks the url of the page once the login button is clicked
		console.log('clicked ok, new location is ' + this.getCurrentUrl());
		// Function to retrieve all the button controls on the new page
		idpLinks = this.evaluate(function() {
			var elements = __utils__.findAll('button');
			return elements.map(function(e) {
				return e.getAttribute('class');
			});
		});
	});
	
	casper.then(function(){
		// Gets the login with Cobweb account button (1st on page)
		loginButton = idpLinks[0];
		// Builds up the control name to use in the button click event
		loginButton = loginButton.replace(/ /g, ".");
		loginButton = 'button.' + loginButton;
		// Tests the button exists
		test.assertExists(loginButton);
		// Clicks the button
		this.click(loginButton);
	});
	
	
	casper.wait(3000, function(){
		// Gets the URL of the new page after button click
		console.log('cobweb idp clicked ok, new location is ' + this.getCurrentUrl());
	});
	
	casper.wait(3000, function() {
		// Complete the login form
		console.log('filling in form');
        this.fill('form#login', {
					'j_username' : '', // enter your username here
					'j_password' : '' // enter your password here

				}, true);
    });
	
	// ensures the link to login is available to click, for some reason the link has to be clicked twice to recognise the fact you are logged in
	casper.wait(3000, function() {
		console.log('trying to click the link again');
		test.assertExists(secondLink);
		this.click(secondLink);	
    });
	
	// Set the screen size
	casper.then(function(){
		this.viewport(1920, 1200);
	});
	
	casper.wait(5000, function(){
		// Retrieves the available menu options in the top navigation bar
		 loggedInLinks = this.evaluate(function() {
        var elements = __utils__.findAll('i');
        return elements.map(function(e) {
            return e.getAttribute('class');
        });
    });
	});
	
	
	casper.then(function(){
		// Retrieves the log out button details from the array of links
		logOutButton = loggedInLinks[3];
		// Build up the control name to be used in the button click event
		var newLogOutBtn = logOutButton.replace(/ /g, ".");
		logOutButton = 'i.' + newLogOutBtn;
		// Check the button exists
		test.assertExists(logOutButton, "log out link visible, user is logged in");
		// Return a screenshot to check and confirm that the login link is no longer visible
		casper.capture("return.png"); 
	});
	
	// Run all tests and finish
	casper.run(function() {
        test.done();
    });
	
	phantom.clearCookies();
});