$('#starts_with').keyup(function() {
    console.log('sending the following information', $('#herbSearchForm').serialize());
    $.ajax({
       method: "POST",
       url: "/search",
       data: $('#herbSearchForm').serialize()
    })
    .done(function( response ) {
       console.log('received response:', response);
       $('#placeholder').html(response);
    });
});
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})
$(function () {
    $('[data-toggle="popover"]').popover()
})
$('.popover-dismiss').popover({
    trigger: 'focus'
})
