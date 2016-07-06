django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
    var inlineId = $row.attr('id');
    var myRegexp = /([0-9]+)/;
    var match = myRegexp.exec(inlineId);
    var order = parseInt(match[0], 10)+1;
    var inputName = $row[0].id+"-order";
    var input = $('input[name*="'+inputName+'"]');
    input.val(order);
    console.log(order);
});


django.jQuery(document).on('formset:removed', function(event, $row, formsetName) {
    reorder($('.inline-group'), $row)
});


function reorder(parent, $row) {
    var items = parent.find('div[class*="dynamic-"]');
    items.each(function (index, element) {
        var input = $(this).find('input[name*="order"]');
        input.val(index+1);
    })
}
