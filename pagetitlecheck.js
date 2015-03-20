casper.test.begin("Dyfi homepage checks", 2, function suite(test) {
	casper.start("https://dyfi.cobwebproject.eu", function() {
		this.echo(this.getTitle());
	});
 
	casper.then(function() {
		test.assertTitle("COBWEB Dyfi Biosphere Reserve Portal (Beta) - Cobweb", "Check the page title");
	});

    casper.then(function() {
       this.test.assertExists({
		    type: 'xpath',
			path: '//div[@class="cookie-warning"]'
		}, 'Cookie warning displayed');
    });
 
	casper.run(function() {
		test.done();
	});
});
