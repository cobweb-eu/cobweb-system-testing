// Test script to perform a user login on the portal, produces screen captures to show before and after
var links;
var idpLinks;
var loginButton;
var secondLink;
var loggedInLinks;
var logOutButton;

var editorLinks;
var adminLinks;
var optionLinks;

var listTemplates;
var listButtons;

var formTextBoxes;
var titleText;

var forms;
var saveOptions;

casper.test.begin('Test the log in function', 12, function suite(test) {
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
					'j_password' : '!' // enter your password here

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
	
	// Retrieves links to find the create survey option
	casper.then(function(){
		 editorLinks = this.evaluate(function() {
        var elements = __utils__.findAll('i');
        return elements.map(function(e) {
            return e.getAttribute('class');
        });
    });
		
	});
	
	casper.then(function(){
			this.echo(JSON.stringify(editorLinks));
			var editIcon = editorLinks[0];
			editIcon = editIcon.replace(/ /g, ".");
			editIcon = 'i.' + editIcon;
			test.assertExists(editIcon);
			this.click(editIcon);
	});
	
	// Retrieve links on admin screen
	casper.then(function(){
		 adminLinks = this.evaluate(function() {
        var elements = __utils__.findAll('a');
        return elements.map(function(e) {
            return e.getAttribute('class');
        });
    });
		
	});
	
	casper.then(function(){
		this.echo(JSON.stringify(adminLinks));
		var addNewBtn = adminLinks[adminLinks.length - 3];
		console.log(addNewBtn);
		addNewBtn = addNewBtn.replace(/ /g, ".");
			addNewBtn = 'a.' + addNewBtn;
			test.assertExists(addNewBtn);
			this.click(addNewBtn);
	});
	
	// Retrieve links on admin screen
	casper.wait(3000, function(){
        optionLinks = this.evaluate(function() {
            var elements = __utils__.findAll('a');
            return elements.map(function(e) {
                return e.getAttribute('id');
            });
        });
	});
	
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="template-survey"]'
			}, 'the element exists');
		
		});
		
		casper.then(function(){
		this.click({
				type: 'xpath',
				path: '//*[@id="template-survey"]'
			}, 'the element exists');
		
		});
		
		// Retrieve links on admin screen
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="gn-new-metadata-container"]/div[3]/div[2]/div/div[2]/div/a[1]'
			}, 'survey link exists');
		
		});
	
	
	
	casper.then(function(){
	this.click({
				type: 'xpath',
				path: '//*[@id="gn-new-metadata-container"]/div[3]/div[2]/div/div[2]/div/a[1]'
			}, 'the element exists');
		
	});
	
	// Checks the text box for completion exists
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="groupName"]'
			}, 'the group name text box exists');
			
			});
			
			
	// Complete the form with test data
	casper.then(function(){
	var valueForGroup = 'automated testing grp 6';
		this.fillXPath('form', {
				'//*[@id="groupName"]':  valueForGroup
			}, false);
			
			});
			
			// get all the buttons on the screen
			casper.then(function(){
		 listButtons = this.evaluate(function() {
        var elements = __utils__.findAll('button');
        return elements.map(function(e) {
            return e.getAttribute('class');
        });
    });
		
	});
	
	casper.then(function(){
			this.echo(JSON.stringify(listButtons));
			var createButton = listButtons[0];
			createButton = createButton.replace(/ /g, ".");
			createButton = 'button.' + createButton;
			test.assertExists(createButton);
			this.click(createButton);
	});
	
	// Checks the text box for completion exists
	casper.wait(10000, function(){
		 formTextBoxes = this.evaluate(function() {
        var elements = __utils__.findAll('input');
        return elements.map(function(e) {
            return e.getAttribute('id');
        });
			});
			});
			
			casper.then(function(){
			this.echo(JSON.stringify(formTextBoxes));
			titleText = formTextBoxes[17];
			titleText = 'input#' + titleText + '.form-control';
			console.log(titleText);
	});
	
	casper.then(function(){
	
	 forms = this.evaluate(function() {
        var elements = __utils__.findAll('form');
        return elements.map(function(e) {
            return e.getAttribute('id');
        });
			});
	});
	
	casper.then(function(){
	this.echo(JSON.stringify(forms));
	test.assertExists(titleText);
	var formid = forms[1];
	formid = 'form#' + formid;
	//titleText = titleText.replace('input','');
var item = {}
item [titleText] = 'automated test survey 115';

var payload = JSON.stringify(item);
	this.echo(payload);
	this.echo(formid);
this.sendKeys(titleText, 'automated test survey 115');

	//this.fill(formid, payload, false);
	});
	
	
	casper.wait(2000, function() {
	 saveOptions = this.evaluate(function() {
        var elements = __utils__.findAll('i');
        return elements.map(function(e) {
            return e.getAttribute('class');
        });
			});
    });
			
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="ng-app"]/body/div[2]/div[2]/div[1]/nav/div[2]/button[5]'
			}, 'the element exists');
		
			});
			
		casper.then(function(){
		this.echo(JSON.stringify(saveOptions));
		var svBtn = saveOptions[3];
		svBtn = svBtn.replace(/ /g, ".");
		svBtn = 'i.' + svBtn;
		
		
	//	 this.page.sendEvent('click', 1610, 26);
		//this.click('html body div:nth-child(2) div:nth-child(2) div.ng-scope nav div.pull-right button:nth-child(8) i');
		//	var x = require('casper').selectXPath;
//this.clickLabel('Save & close', 'span');
			//this.mouse.click(1610, 26);
			
			var x = require('casper').selectXPath;
	this.click(x('//*[@id="ng-app"]/body/div[2]/div[2]/div[1]/nav/div[2]/button[5]'));
		//this.close();  
      //  callback.apply();  
	});
	
	
	
	casper.wait(15000, function(){
		casper.capture('newscreen.png');
	});
	
	// Run all tests and finish
	casper.run(function() {
        test.done();
    });
    
	
	phantom.clearCookies();
});
