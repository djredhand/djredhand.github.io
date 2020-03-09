(function($) {
  "use strict"; // Start of use strict
  var split_str = window.location.href.split('#');
  if(split_str.length && split_str[1] == 'thank-you'){
  	$('#wmModalCenter').modal('show');
  }
})(jQuery); // End of use strict