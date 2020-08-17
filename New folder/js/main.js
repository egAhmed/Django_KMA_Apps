$(document).ready(function() {
    $('[name=quantity], [name=price]').on('input', function() {
        $('[name=total]').val(parseInt($('[name=quantity]').val()) * parseInt($('[name=price]').val()));
    });
    $('[name=sumtotal], [name=paid]').on('input', function() {
        $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
    });
    // $('[name=recievedate]').on('click', function () {
    //     $('[name=recievedate]').datepicker({
    //         dateFormat: 'dd-mm-yy'
    //     });
    // });

    $('#datepicker1, #enddate').datepicker({
        dateFormat: "yy-mm-dd"
    });
    $("#editbills").on('windowload', function() {
        $("#editbills").animate({
            padding: "10px",
            margin: "20px",
            width: "800px",
            height: "800px"
        }, 500);
    });
    $("#edit-items").animate({
        padding: "10px",
        margin: "20px",
        width: "800px",
        height: "800px"
    }, 500);

    $("#f-add-bill").animate({
        padding: "10px",
        margin: "20px",
        width: "800px",
        height: "800px"
    }, 500);

    $("#d-editbill").animate({
        padding: "10px",
        margin: "20px",
        width: "400px",
        height: "400px"
    }, 500);
    // $(function (){
    //     $('[name=datepicker1]').datepicker("setDate", new Date(2008, 9, 03));
    // });
    $("#form1").animate({
        padding: "10px",
        margin: "20px",
        width: "800px",
        height: "800px"
    }, 500);
    $("#login").animate({
        padding: "10px",
        margin: "20px",
        width: "800px",
        height: "800px"
    }, 500);
    // $("#gotohome").css("color", "blueviolet");

    $("#expandform").animate({
        padding: "3px",
        margin: "3px",
        width: "1000px",
        height: "1200px"
    });

    $("#form2").animate({
        padding: "3px",
        margin: "3px",
        width: "900px",
        height: "800px"
    }, 500);

    $('#div-f-cl').animate({
        width: "900px",
        height: "800px"
    }, 1000);

    // $('#save').css('color', '');
    $("#save").animate({
        padding: "3px",
        margin: "3px",
        width: "500px",
        height: "100px"
    }, 500);
    $('#save').hideToggle()

    $("#image").animate({
        // padding: "3px",
        // margin: "3px",
        width: "1500px",
        height: "1000px"
    }, 200);

    //
    $('#table tr').click(function() {
        var href = $(this).find("a").attr("href");
        if (href) {
            window.location = href;
        }
    });

    // $("#divfooter").animate({
    //     padding: '5px',
    //     margin: '5px'
    //         // width: "inline"
    // });

    // $(function () {
    //     $('#datepicker1').datetimepicker({
    //         minDate: moment().startOf('minute').add(180, 'm'),
    //     });
    // });

    // setInterval(function () {
    //     var pickedDate = $('#datepicker1').data('DateTimePicker').date();
    //     var currentDate = moment();
    //     pickedDate = pickedDate.set({
    //         'hour': currentDate.get('hour') + 3,
    //         'minute': currentDate.get('minute'),
    //         'second': currentDate.get('second')
    //     });
    //     $('#datepicker1').data("DateTimePicker").date(pickedDate);
    // }, 1000);

    // $('#datetimepicker1').datepicker();

    // $('#p2').css("color", "blueviolet");
    // $('#all').css("color", "lightgrey");
    // $("#lb_select").css("color", "black");
    // $("#p-signup").css("color", "blue");
    // $("#record").css("color", "white");
})