$(document).ready(function() {
    $(".dropdown-item").click(function() {
    	// disable link
    	$(this).prop("disabled", true);
    	// add spinner to link
    	$(this).html(
    	`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
    	);
	});
});

$('.dropdown-menu').click(function(e) {
	// keep dropdowns open after click
	e.stopPropagation();
});