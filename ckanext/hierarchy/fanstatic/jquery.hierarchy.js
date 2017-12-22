"use strict";

(function (jQuery) {

	if ($('.hierarchy-search').length > 0) {
		$('.hierarchy-search').on('input', function() {
			var input_value = $(this).val().toUpperCase()
			$('.hierarchy-tree-top li').removeClass('highlighted');
			if (input_value !== '') {			    
		    	$('.hierarchy-tree-top li a').each(function() {
		    		if ($(this).text().toUpperCase().indexOf(input_value) >= 0) {
		    			$(this).parent().addClass('highlighted');
		    		}
		    	})
		    }
		});

		$('.hierarchy-search').keydown(function(event){
		    if(event.keyCode == 13) {
		      	event.preventDefault();
		      	return false;
		    }
		 });
	}

    jQuery.fn.hierarchy = function() {
      $('ul.hierarchy-tree li:last-child').addClass('last');
      return this;
    };

})(this.jQuery);

