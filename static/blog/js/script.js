function initMenu() {
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        $(".comment-replies").toggleClass("toggled-comment");
        var ph = $(".placeholder")
        ph.height($(document).height());
        $('#menu ul').hide();
    });
    $('#menu ul').hide();
    $('#menu ul').children('.current').parent().show();
    $('#menu li a').click(
    function() {
        var checkElement = $(this).next();
        if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
            $('#menu ul:visible').slideDown('normal');
            checkElement.slideUp('normal');
            return false;
        }
        if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
            $('#menu ul:visible').slideUp('normal');
            checkElement.slideDown('normal');
            return false;
        }
    }
    );
}

function cloneContent() {
    var content = $('#post-init').html();
    for (var i = 0; i < 10; i++) {
        var newdiv = $("<div class='post post"+i+"'>");
        newdiv.html(content);
        $('#post-init').after(newdiv);
    }
    var comment = $('.comment-init').html();
    for (var i = 0; i < 3; i++) {
        var newdiv = $("<div class='comment col-lg-9 col-md-8 col-sm-7 col-xs-12 comment-"+i+"'>");
        newdiv.html(comment);
        $('.comment-init').after(newdiv);
    }
    var user = $('.user-init').html();
    for (var i = 0; i < 3; i++) {
        var newdiv = $("<div class='user user"+i+"'>");
        newdiv.html(user);
        $('.user-init').after(newdiv);
    }
}

$(document).ready(function() {
    initMenu();
    cloneContent();
});


$(window).on("scroll", function() {
    if ($(window).scrollTop() > 50) {
        $('#sidebar-wrapper').addClass('sidebar-wrapper-scrolled')
    } else {
        console.log("top")
        $('#sidebar-wrapper').removeClass('sidebar-wrapper-scrolled')
    }
});