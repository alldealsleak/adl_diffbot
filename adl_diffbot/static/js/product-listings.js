$(document).on('click', '#btn-refresh', function(){
    drawTable();
});

function drawTable() {
    $('.table-responsive').empty();
    $('#products_list_template').clone(true).attr('id', 'products_list_table').removeAttr('style').appendTo('.table-responsive');

    var productsTable = $('#products_list_table').dataTable({
        'bServerSide': true,
        'sAjaxSource': '/products/',
        'iDisplayLength': 25,
        'fnServerParams': function (aoData) {
            $('.overlay').show();
        },
        'fnServerData': function(sSource, aoData, fnCallback) {
            sSource += '?' + $("#product_filter_form").serialize();
            $.ajax({
                'dataType': 'json',
                'type': 'GET',
                'url': sSource,
                'data': aoData,
                'success': [fnCallback]
            });
        },
        'fnDrawCallback': function( oSettings ) {
            /* Every time we re-draw the table we copy the pagination bar into
               the upper side of the screen.
            */

            $('.dataTables_paginate.paging_full_numbers.copy').remove();
            $('.dataTables_paginate.paging_full_numbers:not(copy)').clone(true).addClass("copy").prependTo("#products_list_table_wrapper");


            $('input[aria-controls="products_list_table"]').keypress(function() {
                $('.dataTables_paginate.paging_full_numbers.copy').remove();
                $('.dataTables_paginate.paging_full_numbers:not(copy)').clone(true).addClass("copy").prependTo("#products_list_table_wrapper");
            });

            $('[aria-controls="products_list_table"][name="products_list_table_length"]').change(function() {
                $('.dataTables_paginate.paging_full_numbers.copy').remove();
                $('.dataTables_paginate.paging_full_numbers:not(copy)').clone(true).addClass("copy").prependTo("#products_list_table_wrapper");
            });

            $('.overlay').hide();
        }

    });

    // Filter box submits only after the user has finished typing
    var typingTimer;

    // On keyup, start the countdown
    $('#products_list_table_filter input').unbind(
        'keypress keyup').bind(
            'keypress keyup', function(e) {
                typingTimer = setTimeout(function() {
                    productsTable.fnFilter($('#products_list_table_filter input').val());
            }, 1200);
    });

    // On keydown, clear the countdown
    $('#products_list_table_filter input').unbind('keypress keydown').bind(
        'keypress keydown', function(e) {
        clearTimeout(typingTimer);
    });
}