function drawTable() {
    $('.table-responsive').empty();
    $('#products_list_template').clone(true).attr('id', 'products_list_table').removeAttr('style').appendTo('.table-responsive');

    var productsTable = $('#products_list_table').dataTable({
        'bServerSide': true,
        'sAjaxSource': '/products/?company_id=2&country_code=sg',
        'bProcessing': true
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