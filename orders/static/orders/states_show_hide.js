/**
 * Created by moshe on 8/1/17.
 */
$('#id_territory').change(function () {
    if ($(this).val() === 'United States') {
        $('#usa_states').show();
    } else {
        $('#usa_states').hide();
    }
});

$('#is-non-profit').click(function () {
    $('#non-profit').show();
});

$('#is-not-non-profit').click(function () {
    $('#non-profit').hide();
});