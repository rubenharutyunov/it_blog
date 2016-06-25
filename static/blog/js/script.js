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

function handle_likes() {
    $(".post-like a").click(function (event) {
        event.preventDefault();
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
                       var id = $this.attr("id");
                       $('.likes'+id).text(response.likes);
                   }
                },
                error: function(rs, e) {
                    console.log(rs.responseText); // For debug
                }
          });
    });
}

function handle_fav() {
    $('.post-bookmark a').click(function (event) {
        event.preventDefault();
        var $this = $(this);
        $.ajax({
               type: "POST",
               url: "/fav/",
               data: {'post_id': $(this).attr('id'), 'csrfmiddlewaretoken': csrf},
               dataType: "json",
               success: function(response) {
                   if (response.status != 'AUTH_REQUIRED') {
                       if (response.status == "ADDED") {
                           $this.addClass('fav');
                       } else {
                           $this.removeClass('fav');
                       }
                       var id = $this.attr("id");
                       $('.favs'+id).text(response.count);
                   }
                },
                error: function(rs, e) {
                    console.log(rs.responseText); // For debug
                }
          });
    });
}

function handle_comment_del() {
    $(document).on('click', '.comment-delete a', function (event) {
        event.preventDefault();
        var $this = $(this);
        $.ajax({
               type: "POST",
               url: "/del_comment/",
               data: {'comment_id': $(this).attr('class'), 'csrfmiddlewaretoken': csrf},
               dataType: "json",
               success: function(response) {
                   if (response.status == 'OK') {
                       var comment =  $('.comment#'+$this.attr('class'));
                       comment.hide('slow');
                   }
                },
                error: function(rs, e) {
                    console.log(rs.responseText); // For debug
                }
          });
    });
}

function handle_comment_add() {
    $('.comment-form button').click(function(event) {
        event.preventDefault();
        var $this = $(this);
        var form_data = $('.comment-form').serializeArray();
        form_data.push({name: 'post_id', value: $this.attr('data-post-id')});
        $.ajax({
               type: "POST",
               url: "/add_comment/",
               data: form_data,
               dataType: "json",
               success: function(response) {
                   if (response.status == 'OK') {
                       var comment_container = $('.comments-container');
                       var parent_id = $this.parent().find('input[name="parent"]').attr('value');
                       if (parent_id) {
                           $('#'+parent_id+" .comment-replies").html(response.html);
                       } else {
                           comment_container.prepend(response.html);
                       }
                       var new_comment = $('.comment#'+response.comment_id);
                       clear_comment_form();
                       $('html, body').animate({
                           scrollTop: new_comment.offset().top
                       }, 500);
                   }
                },
                error: function(rs, e) {
                    console.log(rs.responseText); // For debug
                }
          });
    });
}

function handle_reply(id) {
    var textarea = $(".comment-form textarea");
    var parent = $(".comment-form input[name='parent']");
    var label = $(".comment-form label");
    $(document).on("click", '.comment-reply', function(event) {
        event.preventDefault();
        var id = $(this).parent().attr("id");
        var author = $(this).parent().find('.comment'+ id + '-author').text().trim();
        parent.val(id);
        textarea.val("@"+author+", ");
        textarea.focus();
        label.text("Reply to " + author);
    });
    var clear_button = $(".btn-clear");
    clear_button.click(function (event) {
        clear_comment_form();
    });
}

function handle_comments_refresh() {
    $('.comments .refresh').click(function (event) {
        event.preventDefault();
        var $this = $(this);
        var post_id = $this.attr('data-post-id');
        $.ajax({
               type: "POST",
               url: "/refresh_comments/",
               data: {'post_id': post_id,'csrfmiddlewaretoken': csrf},
               dataType: "html",
               success: function(response) {
                   $this.parent().find('.comments-container').html(response).hide(0).fadeIn("slow");
                },
                error: function(rs, e) {
                    console.log(rs.responseText); // For debug
                }
          });
    })
}

function clear_comment_form() {
    var textarea = $(".comment-form textarea").val("");
    var parent = $(".comment-form input[name='parent']").val("");
    var label = $(".comment-form label").text("Add comment:");
    $(".errorlist").hide();
}

$(document).ready(function() {
    initMenu();
    hljs.initHighlightingOnLoad();
    handle_reply();
    handle_likes();
    handle_fav();
    handle_comment_del();
    handle_comment_add();
    handle_comments_refresh();
});


$(window).on("scroll", function() {
    if ($(window).scrollTop() > 50) {
        $('#sidebar-wrapper').addClass('sidebar-wrapper-scrolled')
    } else {
        $('#sidebar-wrapper').removeClass('sidebar-wrapper-scrolled')
    }
});