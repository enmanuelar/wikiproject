/**
 * Created by HMachine on 08/07/2016.
 */
$(".signup-btn").click(function(){
    window.location.replace("/signup");
});

var paths = ["/signup", "/"];
if (paths.indexOf(window.location.pathname)!= -1 || window.location.pathname.substring(0, 6) === "/_edit"){
    $(".edit-btn").prop("disabled", true);
}


$(".edit-btn").click(function(){
    var content = $("#index-content").html();
    var contentDiv = $("#index-content");
    contentDiv.addClass("edit-text");
    contentDiv.text(content);
    contentDiv.prop("contenteditable","true");
    $(".edit-btn").prop("disabled", true);
    $(".save-btn").css("visibility", "visible");
});

function ajaxContent(content){
    $.ajax(window.location.pathname,{
        type: 'POST',
        dataType: 'json',
        data:{
            content: content
        }
    });
}

$(".save-btn").click(function(){
    var content = $("#index-content").text();
    var contentDiv = $("#index-content");
    contentDiv.removeClass("edit-text");
    contentDiv.prop("contenteditable","false");
    contentDiv.html(content);
    ajaxContent(content);
    $(".edit-btn").prop("disabled", false);
    $(".save-btn").css("visibility", "hidden");
});




