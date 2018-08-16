$(document).ready(function () {
    $('#regbtn').click(function(){
        $('#potionlogo').fadeOut();
        $('#loginbox').fadeOut();
        $('#webtitle').fadeOut();
        $('#reigsterbox').delay(700).fadeIn()
    });
    $('#already').click(function(e){
        e.preventDefault();
        $('#potionlogo').removeClass('animate bounceInDown').fadeIn();
        $('#loginbox').removeClass('animate fadeIn').fadeIn();
        $('#webtitle').removeClass('animate fadeInDown').fadeIn();
        $('#reigsterbox').hide()
    });
});
