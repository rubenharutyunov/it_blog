// For new added admin inlines
django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
    var selector = $row.find('select[name*="icon"]');
    // WORKAROUND: Select2 from ready callback not working. Delete old and init again when formset added.
    var old_select = $row.find('.select2');
    if (!(old_select === undefined || old_select.length == 0)) {
        $row.find('.select2').remove();
        initSelect2(selector);
    }
});

// Add icon
function format(state) {
    var originalOption = state.element;
    return '<i class="fa ' + $(originalOption).data('icon') + '"></i>' + state.text;
}

// Init
function initSelect2(selector) {
    $(selector).select2({
        width: "120px",
        templateResult: format,
        templateSelection: format,
        escapeMarkup: function(m) {return m;}
    });
}

$(document).ready(function () {
    initSelect2('select[name*="icon"]');
});