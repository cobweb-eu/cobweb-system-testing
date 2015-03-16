// Test script to perform a simple text search on the portal, produces screen captures to show before and after
var links;
var searchBtn;
var searchFormLinks;

casper.test.begin('Test the search function', 3, function suite(test) {
    casper.start('https://dyfi.cobwebproject.eu', function() {
		console.log('current url location is ' + this.getCurrentUrl()); 
		// Create an array of links available to find the search button
		 links = this.evaluate(function() {
			var elements = __utils__.findAll('span');
			return elements.map(function(e) {
				return e.getAttribute('class');
			});
		});
    });
	
	casper.then(function(){
		// Allocate the search button to be clicked
		searchBtn = links[5];
		// Start building up the control name to use in the button click event
		searchBtn = searchBtn.replace(/ /g, ".");
		searchBtn = 'span.' + searchBtn;
		// Click the search button
		this.click(searchBtn);
	});
	

	// Checks the form for submission exists
	casper.wait(3000, function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="ng-app"]/body/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/form'
			}, 'the element exists');
		
		});

	// Checks the text box for completion exists
	casper.then(function(){
		this.test.assertExists({
				type: 'xpath',
				path: '//*[@id="gn-any-field"]'
			}, 'the text box exists');
			
			});
	
	// Complete the form with test data
	casper.then(function(){
		this.fillXPath('form', {
				'//*[@id="gn-any-field"]':    'nottingham'
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