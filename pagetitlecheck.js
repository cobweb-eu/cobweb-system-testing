casper.test.begin("Loading dyfi homepage", 1, function suite(test) {
	casper.start("https://dyfi.cobwebproject.eu", function() {
	this.echo(this.getTitle());
	});
 
	casper.then(function() {
		test.assertTitle("COBWEB Dyfi Biosphere Reserve Portal (Beta) - Cobweb", "COBWEB Dyfi Biosphere Reserve Portal (Beta) - Cobweb");
	});
 
	
 
	casper.run(function() {
		test.done();
	});
});