$(document).ready(
    function() {
        let csrftoken = null;

        $('#state').change(function() {
            let url = $('#sum_form').attr('data-url');
            let state_id = $(this).val();

            csrftoken = $('[name = "csrfmiddlewaretoken"]').val();

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            });

            $.ajax({
                type: 'get',
                dataType: 'html',
                beforeSend: function() {
                    $('#loading').html('Loading local government areas...').removeClass().addClass('alert alert-info');
                },
                url: url,
                data: {
                    'state': state_id
                },
                success: function(data) {
                    $('#loading').html('Total Result: 0').removeClass().addClass('alert alert-success');
                    $('#lga').html(data);
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    $('#loading').html(xhr.status + ': ' + thrownError).removeClass().addClass('alert alert-danger');
                    $('#btn').removeAttr('disabled');
                }
            });
        });

        $('#sum_form').submit(
            function(event) {
                event.preventDefault();

                let sum_url = $('#sum_form').attr('data-sum-url');
                let lga_id = $('#lga').val();
                csrftoken = $('[name = "csrfmiddlewaretoken"]').val();

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                    }
                });

                if (lga_id === null || lga_id === '') {
                    $('#loading').html('Please select a local government').removeClass().addClass('alert alert-danger');
                    $('#result').html('');
                    return;
                }



                $.ajax({
                    type: 'get',
                    dataType: 'html',
                    beforeSend: function() {
                        $('#loading').html('Retrieving total results in this local government').removeClass().addClass('alert alert-info');
                        $('#btn').attr('disabled', 'disabled');
                    },
                    url: sum_url,
                    data: {
                        'lga': lga_id
                    },
                    success: function(data) {
                        $('#loading').html('Data successfully retrieved. View result below').removeClass().addClass('alert alert-success')
                        $('#result').html(data);
                        $('#btn').removeAttr('disabled');

                        $('html,body').animate({
                            scrollTop: $('#btn').offset().top
                        }, 1000);
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                        $('#loading').html(xhr.status + ': ' + thrownError).removeClass().addClass('alert alert-danger');
                        $('#btn').removeAttr('disabled');
                        $('#result').html('');
                    }
                });
            }
        );
    }
);