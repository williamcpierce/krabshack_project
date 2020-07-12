// Change form submit behavior
$('#fit-form').on('submit', function (event) {
  event.preventDefault(); // Block normal form submission
  fit_process();
});

// Fit process AJAX
function fit_process() {

  $.ajax({
    url: "/fit/", // Endpoint
    type: "POST", // HTTP method
    data: {
      inputs: JSON.stringify(
        $(".form-control").serializeArray()
      ),
      csrfmiddlewaretoken: Cookies.get('csrftoken')
    }, // Data sent with the post request

    // Handle a successful response
    success: function (json) {
      var extra = document.getElementById('extra');
      var needed = document.getElementById('needed');
      extra.value = json.extra
      needed.value = json.required
    },

    // Handle a non-successful response
    error: function (xhr, errmsg, err) {
    }
  });
};
