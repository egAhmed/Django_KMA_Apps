$(document).ready(function() { // this is the way to begin with JQuery
    // 
    $('[name=quantity], [name=price]').on('input', function() {
        $('[name=total]').val(parseInt($('[name=quantity]').val()) * parseInt($('[name=price]').val()));
    });

    // Occurs on button click 
    $('#btn-edit-items').on('click', function() {
        $('[name=total]').val(parseInt($('[name=quantity]').val()) * parseInt($('[name=price]').val()));
    });

    // Occurs on button(submit) on click  
    $('#btn-add-bill').on('click', function() {
        $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
        if (parseInt($('[name=remain]').val()) == 0) {
            $('#paidDone option:contains(false)').attr('selected', true); // the way to assign a value to a dropdown(choice field)
            $('#returns').attr('checked', false); // this is the way to assign a true or false to a checkbox
        }
    });

    // Occurs on button(update) click  
    $('#btn-editbills').click(function() {
        // alert('clicked');
        $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
        if (parseInt($('[name=paid]').val()) > 0 && parseInt($('[name=sumtotal]').val()) == parseInt($('[name=paid]').val()) && parseInt($('[name=remain]').val()) == 0) {
            $('#paidDone option:contains(true)').attr('selected', true);
            // alert('it is finished');
            // $('#paidDone').val(x).change();
            // $('#returns').attr('checked', true); // this the method to assign a true or false to a checkbox
        } else {
            $('#paidDone option:contains(false)').attr('selected', false);
        }
        // if ($('[name=sumtotal]').text('')) {
        //     // alert('it is empty');
        //     parseInt($('[name=sumtotal]').val(0));
        //     // ('[name=sumtotal]').text('0');
        // }
    });

    // Occurs when the text changed
    $('[name=sumtotal], [name=paid]').on('input', function() {
        // alert("hi done");
        $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
        // if (parseInt($('[name=remain]').val()) == 0) {
        //     // $('#paidDone').val('');
        //     $('#paidDone').val('true');
        //     // $('#paidDone').val(true);
        //     // $('#returns').val(true);
        // }
    });
    // $('[name=sumtotal], [name=paid]').on('input', function() {
    //     if (parseInt($('[name=remain]').val()) == 0) {
    //         // $('#paidDone').val('');
    //         // $('#paidDone').val('true');
    //         // $('#paidDone').val(true);
    //         $('#returns').val(true);
    //     }
    // });

    // This snippet occurs when the form load when we enter the page or refresh it, this is dueto callback function
    $("#f-editbills").animate({
        padding: "10px",
        margin: "20px",
        width: "1000px",
        height: "1000px"
    }, 500, (function() {
        // alert('f-editbills loaded');
        $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
        if (parseInt($('[name=paid]').val()) > 0 && parseInt($('[name=sumtotal]').val()) == parseInt($('[name=paid]').val()) && parseInt($('[name=remain]').val()) == 0) {
            $('#paidDone option:contains(true)').attr('selected', true);
            // alert(('#paidDone').val());
            // $('#paidDone').val(x).change();
            // $('#returns').attr('checked', true); // this the method to assign a true or false to a checkbox
        } else {
            $('#paidDone option:contains(false)').attr('selected', true);
        }
    }));

    $("#btn-add-bill").on('click', function() {
        $('[name=sumtotal], [name=paid], [name=remain]').val(0)
    });

    $("#edit-items, #f-newitems").animate({
        padding: "10px",
        margin: "20px",
        width: "1000px",
        height: "1000px"
    }, 500);

    $("#f-add-bill").animate({
        padding: "10px",
        margin: "20px",
        width: "300px",
        height: "500px"
    }, 500);

    $(function() {
        $('#datepicker1, #enddate').datepicker({
            dateFormat: "yy-mm-dd"
        });
    });

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
    // $('#total').val(0);

    // $('#datepicker1, #enddate').datepicker({
    //     dateFormat: "yy-mm-dd"
    // });

    // $(function() {
    //     $("#edit-items").animate({
    //         padding: "10px",
    //         margin: "20px",
    //         width: "800px",
    //         height: "800px"
    //     }, 500);
    // });

    // $("#edit-items", "#f-add-bill", "#f-editbills").animate({
    //     padding: "10px",
    //     margin: "20px",
    //     width: "800px",
    //     height: "800px"
    // }, 500);

    // $(function() {
    //     $("#edit-items", "#f-newitems", "#f-editbills", "#f-add-bill").animate({
    //         padding: "10px",
    //         margin: "20px",
    //         width: "800px",
    //         height: "800px"
    //     }, 500);
    // });

    // $(function() {
    //     $("#f-add-bill").animate({
    //         padding: "10px",
    //         margin: "20px",
    //         width: "800px",
    //         height: "800px"
    //     }, 500);
    // });

    // $(function() {
    //     $("#f-newitems", "#f-add-bill").animate({
    //         padding: "10px",
    //         margin: "20px",
    //         width: "800px",
    //         height: "800px"
    //     }, 500);
    // });

    // $("#d-editbill").animate({
    //     padding: "10px",
    //     margin: "20px",
    //     width: "400px",
    //     height: "400px"
    // }, 500);

    // $(function (){
    //     $('[name=datepicker1]').datepicker("setDate", new Date(2008, 9, 03));
    // });

    // $('#launtype, #price, #quantity').html(document.getElementById('#launtype, #price, #quantity').innerText)
    // $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
    // $('[name=sumtotal], [name=paid]').focus(function() {
    //     $('[name=remain]').val(parseInt($('[name=sumtotal]').val()) - parseInt($('[name=paid]').val()));
    // });
    // $('[name=sumtotal], [name=paid]').find('select, input').change();
    // $('#table tr').click(function() {
    //     var href = $(this).find("a").attr("href");
    //     if (href) {
    //         window.location = href;
    //     }
    // });

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
    // $("#p-signup").css("color", "blue");
    // $("#record").css("color", "white");
})