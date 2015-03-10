var links;

casper.start('https://dyfi.cobwebproject.eu', function() {
    links = this.evaluate(function() {
        var elements = __utils__.findAll('a');
        return elements.map(function(e) {
            return e.getAttribute('href');
        });
    });
});



casper.run(function() {
	this.echo(JSON.stringify(links));
	casper.exit();
});

