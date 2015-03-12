// Test script to perform a user login on the portal, produces screen captures to show before and after
casper.test.begin('Test the log in function', 3, function suite(test) {
    casper.start('https://dyfi.cobwebproject.eu', function() {
	
		// First tests that the url to search is available before clicking it
		test.assertExists('i.fa.glyphicon.glyphicon-log-in');
    });
	
	// ensures the link is available to click
	casper.waitUntilVisible('i.fa.glyphicon.glyphicon-log-in', function() {
        this.click('i.fa.glyphicon.glyphicon-log-in');
		
    });
	
	casper.wait(3000, function(){
	console.log('clicked ok, new location is ' + this.getCurrentUrl());
	});
	
	casper.waitUntilVisible('button.btn.btn-success', function() {
        test.assertExists('button.btn.btn-success');
		this.click('button.btn.btn-success');
    });
	
	casper.wait(3000, function(){
	console.log('cobweb idp clicked ok, new location is ' + this.getCurrentUrl());
	});
	
	casper.waitUntilVisible('form#login', function() {
		
        this.fill('form#login', {
					'j_username' : '', // enter your username here
					'j_password' : '' // enter your password here

				}, true);
    });
	
	// ensures the link is available to click, for some reason the link has to be clicked twice to recognise the fact you are logged in
	casper.waitUntilVisible('i.fa.glyphicon.glyphicon-log-in', function() {
        this.click('i.fa.glyphicon.glyphicon-log-in');
		
    });
	
	// Set the screen size
	casper.then(function(){
		this.viewport(1920, 1200);
	});
	
	casper.wait(5000, function(){
	  test.assertExists('i.fa.glyphicon.glyphicon-log-out', "log out link visible, user is logged in");
     casper.capture("return.png"); 
    });
	
	// Run all tests and finish
	casper.run(function() {
        test.done();
    });
	
	phantom.clearCookies();
});