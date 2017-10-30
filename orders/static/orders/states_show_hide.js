/**
 * Created by moshe on 8/1/17.
 */
var territory_elem = $('#id_territory');
var is_non_profit = $('#is-non-profit');

territory_elem.change(function () {
    if ($(this).val() === 'United States') {
        $('#usa_states').show();
    } else {
        $('#usa_states').hide();
    }
});

is_non_profit.click(function () {
    $('#non-profit').show();
});

$('#is-not-non-profit').click(function () {
    $('#non-profit').hide();
});

if (territory_elem.val() === 'United States') {
    $('#usa_states').show();
} else {
    $('#usa_states').hide();
}

if (is_non_profit.val() === 'selected') {
    $('#non-profit').show();
} else {
    $('#non-profit').hide();
}