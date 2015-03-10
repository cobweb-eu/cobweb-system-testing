// Currently work in progress

casper.test.begin('Sign In User', 1, function(test){
    casper.start('https://dyfi.cobwebproject.eu/idp/Authn/UserPassword');

	
		casper.waitUntilVisible('form#login', function() {
		
        this.fill('form#login', {
					'j_username' : 'franm28',
					'j_password' : ''

				}, true);
    });
		
		//this.click('button.form-element.form-button');
   
	
	 casper.wait(10000, function(){
		test.assertHttpStatus(200, 'this status says it is ok, even though your password is wrong');
       this.echo(this.getHTML());
    });

   

	casper.wait(10000, function(){
	this.echo(this.getHTML());
      
    });
	
	 phantom.clearCookies();

    casper.run(function(){
        test.done();
    });
});
