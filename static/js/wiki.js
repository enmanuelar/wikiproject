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

//Signup Validation
function validationClass(inputDiv, status){
    if (status == "success"){
        $(inputDiv).removeClass("has-success has-error").addClass("has-success").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove").addClass("glyphicon-ok");
    }else if (status == "error"){
        $(inputDiv).removeClass("has-success has-error").addClass("has-error").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove").addClass("glyphicon-remove");
        $("#input-password").val("");
        $("#input-verify").val("");
    }
}

function validate(input){
    //username
    if (/^[a-zA-Z0-9_-]{3,20}$/.test(input.username)){
        validationClass("#input-name-div", "success");
    }
    else{
        validationClass("#input-name-div", "error");
    }
    //password
    if (/^.{3,20}$/.test(input.password) && (input.password == input.verify)){
        validationClass("#input-password-div", "success");
    }
    else{
        validationClass("#input-password-div", "error");
    }
    //verify
     if (/^.{3,20}$/.test(input.verify) && (input.password == input.verify)){
        validationClass("#input-verify-div", "success");
    }
    else{
        validationClass("#input-verify-div", "error");
    }
    //email
    if (/^[\S]+@[\S]+.[\S]+$/.test(input.email)){
        validationClass("#input-email-div", "success");
    }
    else{
        validationClass("#input-email-div", "error");
    }
}

$("#register-btn").click(function(){
    var username = $("#input-name").val();
    var password = $("#input-password").val();
    var verify = $("#input-verify").val();
    var email = $("#input-email").val();
    var input = {
        username: username,
        password: password,
        verify: verify,
        email: email
    };
    validate(input);
    //var userRe = /r^[a-zA-Z0-9_-]{3,20}$/;
    /*if (/^[a-zA-Z0-9_-]{3,20}$/.test(username)){
        $("#input-name-valid").addClass()
    }
    else{
        alert("invalid");
    }*/

});


