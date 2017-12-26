/**
 * Created by moshe on 7/31/17.
 */
$('#id_distribute_on_0').click(function () {
    if ($(this).is(':checked')) {
        $('#id_youtube').show();
    } else {
        $('#id_youtube').hide();
    }
});