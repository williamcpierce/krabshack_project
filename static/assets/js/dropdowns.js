$(document).ready(function() {
    $(".kt-menu__item").click(function() {
        // disable link
        $(this).prop("disabled", true);
        // add spinner to link
        $(this).html(
        `<a class="kt-menu__link">
			<span class="kt-menu__link-icon">
				<div class="kt-spinner kt-spinner--sm kt-spinner--brand">
    			</div>
			</span>
			<span class="kt-menu__link-text">Loading...</span>
		</a>`
        );
    });
});

