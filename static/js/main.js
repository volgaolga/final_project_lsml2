$(document).ready(function () {
    $('.loader').hide();
    $('#answer-header').hide();
    $('#answer').hide();


    $('#submit').click(function () {
        let form_data = new FormData($('#upload-comment')[0]);

        $('#answer-header').hide();
        $('#answer').hide();
        $('.loader').show();

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            dataType: "json",
            success: function (data) {
                let task_id = data.task_id;

                if (task_id) {
                    let flag = true;
                    while(flag) {
                        $.ajax({
                            type: 'GET',
                            dataType: "json",
                            url: `/task/${task_id}`,
                            async: false,
                            success: function (data) {
                                if (data.ready) {
                                    flag = false;
                                    $('.loader').hide();
                                    $('#answer-header').text('Answer: ').show();
                                    $('#answer').text(data.result).show();
                                }
                            }
                        });
                    }
                }

            }

        });

    });

});
