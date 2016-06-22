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

function handle_reply(id) {
    var comment = $(".comment-reply");
    var textarea = $(".comment-form textarea");
    var parent = $(".comment-form input[name='parent']");
    var label = $(".comment-form label");
    comment.click(function (event) {
        event.preventDefault();
        var id = $(this).parent().attr("id");
        console.log(parseInt(id));
        var author = $(this).parent().find('.comment-author').text().trim();
        parent.val(id);
        textarea.val("@"+author+", ");
        textarea.focus();
        label.text("Reply to " + author);
    });
    var clear_button = $(".btn-clear");
    clear_button.click(function (event) {
        textarea.val("");
        parent.val("");
        label.text("Add comment:");
        $(".errorlist").hide();
    });
}

function handle_likes() {
    $(".post-like a").click(function (event) {
        event.preventDefault();
        var id = $('.post-like a').attr("id");
        var $this = $(this);
        $.ajax({
               type: "POST",
               url: "/like/",
               data: {'post_id': $(this).attr('id'), 'csrfmiddlewaretoken': csrf},
               dataType: "json",
               success: function(response) {
                   if (response.status != 'AUTH_REQUIRED') {
                       if (response.status == "LIKED") {
                           $this.addClass('liked');
                       } else {
                           $this.removeClass('liked');
                       }
                   }
                   var id = $this.attr("id");
                   $('.likes#'+id).text(response.likes);
                },
                error: function(rs, e) {
                       console.log(rs.responseText); // For debug
                }
          });
    });
}

$(document).ready(function() {
    initMenu();
    hljs.initHighlightingOnLoad();
    handle_reply();
    handle_likes();
});


$(window).on("scroll", function() {
    if ($(window).scrollTop() > 50) {
        $('#sidebar-wrapper').addClass('sidebar-wrapper-scrolled')
    } else {
        console.log("top")
        $('#sidebar-wrapper').removeClass('sidebar-wrapper-scrolled')
    }
});