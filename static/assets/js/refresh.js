$(document).ready(function() {
    $("#refresh").click(function() {
        // disable icon
        $(this).prop("disabled", true);
        // replace icon with spinning icon
        $(this).html(
        `<i class="flaticon2-refresh" style="animation: spinner-border 0.75s linear infinite;"></i>`
        );
    });
});

