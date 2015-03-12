// Test script to perform a simple text search on the portal, produces screen captures to show before and after
// FM - Although I'm not sure the actual functionality is working as yet - results do not seem to filter when manually performed
casper.test.begin('Test the search function', 5, function suite(test) {
    casper.start('https://dyfi.cobwebproject.eu', function() {
	
		// First tests that the url to search is available before clicking it
		console.log('current url location is ' + this.getCurrentUrl()); 
        test.assertExists('span.fa.fa-search');
		
    });
	
	// ensures the link is available to click
	casper.waitUntilVisible('span.fa.fa-search', function() {
        this.click('span.fa.fa-search');
    });
	
	// Waits for a the search page to load - checks the control
	casper.waitUntilVisible('input.form-control.ng-pristine.ng-valid', function() {
    console.log('clicked ok, new location is ' + this.getCurrentUrl());
	test.assertExists('input.form-control.ng-pristine.ng-valid');
	});

	// Checks the form for submission exists
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="search_container"]/form'
			}, 'the element exists');
		
		});

	// Checks the text box for completion exists
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="search_container"]/form/div[1]/div/input'
			}, 'the text box exists');
			
			});
	
	// Complete the form with test data
	casper.then(function(){
		this.fillXPath('form', {
				'//*[@id="search_container"]/form/div[1]/div/input':    'testing testing testing'
			}, false);
			
			});
	
	// Set the screen size
	casper.then(function(){
		this.viewport(1920, 1200);
	});
	
	// Perform a screen capture pre search
	casper.then(function(){
		casper.capture("search.png");
	});
	
	// Ensure the button control exists to be clicked
	casper.wait(5000, function() {
		console.log('filled text box and taken screen shot, checking button exists');
		test.assertExists('i.fa.fa-search');
	});
	
	// Click the search button
	casper.then(function(){
		console.log('clicking button');
		this.click('i.fa.fa-search');
	});
	
	// Wait some time and screen capture what the screen now shows
	casper.wait(10000, function(){
		casper.capture("searchafter.png");
	});
	
	// Run all tests and finish
	casper.run(function() {
        test.done();
    });
});