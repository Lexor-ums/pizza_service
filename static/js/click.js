$(document).ready(function() {
    $(".make-buy").click(function(event) {
        var price = $.get('/cost', { data : event.target.id} );
        price.done( function(results) {
            $('.total-cost').html(+$('.total-cost').html() + Number(results.cost));
            $('.total-items').html(+$('.total-items').html() + 1);
            $.post('/set_cookies', { total_cost : $('.total-cost').html(),
                total_items : $('.total-items').html()})
            $.post('/add_to_list', {id : Number(event.target.id)} )
        });
    });

    $('.btn-number').click(function(e){
    e.preventDefault();

    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    price     = parseInt(input.attr('price'));
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {

            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
                $('.total-cost').html(+$('.total-cost').html() - Number(price));
                $('.total-items').html(+$('.total-items').html() - 1);
                $.post('/set_cookies', { total_cost : $('.total-cost').html(),
                    total_items : $('.total-items').html()})
                $.post('/remove_from_list', {id : Number(parseInt(input.attr('id')))} )
            }
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
                $('.total-cost').html(+$('.total-cost').html() + Number(price));
                $('.total-items').html(+$('.total-items').html() + 1);
                $.post('/set_cookies', { total_cost : $('.total-cost').html(),
                    total_items : $('.total-items').html()})
                $.post('/add_to_list', {id : Number(parseInt(input.attr('id')))} )
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});


    $('.input-number').focusin(function(){
   $(this).data('oldValue', $(this).val());
});


    $('.input-number').change(function() {

    minValue =  parseInt($(this).attr('min'));
    maxValue =  parseInt($(this).attr('max'));
    price = parseInt($(this).attr('price'));
    valueCurrent = parseInt($(this).val());

    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }
});


    $(".input-number").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

    $(".no-data").hide();

    $(".confirm-btn").click(function () {
        if ($("input[id='formName']").val() == '' || $("input[id='formAddress']").val() == '') {
            $(".no-data").show();
        }
        else {
            $(".no-data").hide();
            $.post('/set_cookies', { total_cost : 0} );
            $.post('/set_cookies', { total_items : 0} );
            $.post('/set_cookies', { name : $("input[id='formName']").val()});
            $.post('/set_cookies', { address : $("input[id='formAddress']").val()});
            $.post('/generate_order');
            $(location).attr('href', '/');

        }
    });

});
