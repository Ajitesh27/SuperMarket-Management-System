$(document).ready(function(){
    $("#index #menu a").each(function() {
        if ((window.location.pathname.indexOf($(this).attr('href'))) > -1) {
            $(this).removeClass('text-muted')
            $(this).addClass('selected');
        }
    });
});