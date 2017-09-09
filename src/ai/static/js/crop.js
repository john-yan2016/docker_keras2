jQuery(function($){
      
        // Create a scope-wide variable to hold the Thumbnailer instance
        var thumbnail;
        
        // Instantiate Jcrop
        $('#target').Jcrop({
  	aspectRatio: 1,
  	setSelect: [ 175, 100, 400, 300 ]
	},function(){
  	var jcrop_api = this;
  	thumbnail = this.initComponent('Thumbnailer', { width: 130, height: 130 });
	});
 });
