$('#edit_order').click(function () {
    $('#link_inquiry').trigger('click');
    $('#license-data').hide();
    $('#license-form').show();
});

$('.nav.nav-pills.nav-justified>li>a').click(function (e) {
    if (e.target.id === 'link_inquiry') {
        $('#license-data').show();
    } else {
        $('#pilljustified1').hide();
    }
});