$(document).ready(function() {
    $('#like_btn').click(function() {
        var bookSlug = $('#like_btn').data('book-slug');
        var url = "/bookepedia/book/" +bookSlug + "/add_to_top_picks/"; 

        // Send AJAX GET request
        $.get(url, function(data) {
            $('#like_count').html(data);
            $('#like_btn').hide();
        });
    });
});
