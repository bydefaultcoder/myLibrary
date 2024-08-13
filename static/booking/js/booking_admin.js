(function($) {
    $(document).ready(function() {
        // Listen for changes on the location dropdown
        $('#id_location').change(function() {
            // console.log("hello")
            var locationId = $(this).val();  // Get selected location ID
            var seatDropdown = $('#id_seat');

            if (locationId) {
                // Clear the seat dropdown
                seatDropdown.empty();

                // Fetch seats associated with the selected location
                $.ajax({
                    url: '/admin/booking/get_seats_by_location/',  // URL to fetch seats
                    data: {
                        'location_id': locationId
                    },
                    success: function(data) {
                        seatDropdown.append('<option value="">Select</option>');
                        $.each(data, function(key, value) {
                            seatDropdown.append('<option value="' + key + '">' + value + '</option>');
                        });
                    }
                });
            } else {
                seatDropdown.empty();
                seatDropdown.append('<option value="">---------</option>');
            }
        });
    });
})(django.jQuery);
