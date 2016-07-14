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
       //$("#input-password").val("");
        //$("#input-verify").val("");
    }
}

//username
$("#input-name").blur(function () {
    var username = $("#input-name").val();
    var validation = $("input#validation-input").val();
    if (username && /^[a-zA-Z0-9_-]{3,20}$/.test(username)) {
        $.post("/signup", {username: username, validation: validation}).done(function(data){
            var status = JSON.parse(data).status;
            if (status == false){
                validationClass("#input-name-div", "success");
            }
            else{
                validationClass("#input-name-div", "error");
            }
        });
    }
    else {
        validationClass("#input-name-div", "error");
    }
});
//password
$("#input-password").change(function () {
    var password = $("#input-password").val();
    var verify = $("#input-verify").val();

    if (password && /^.{3,20}$/.test(password)) {
        validationClass("#input-password-div", "success");
        if (verify && verify == password){
            validationClass("#input-verify-div", "success");
        }
    }
    else {
        validationClass("#input-password-div", "error");
    }
});
//verify
$("#input-verify").change(function () {
    var verify = $("#input-verify").val();
    var password = $("#input-password").val();
    if (verify && /^.{3,20}$/.test(verify) && (password == verify)) {
        validationClass("#input-verify-div", "success");
    }
    else {
        validationClass("#input-verify-div", "error");
    }
});
//email
var email = $("#input-email")
if (email.val()){
    $("#input-email").blur(function () {
        var email = $("#input-email").val();
        if ((email && /^[\S]+@[\S]+.[\S]+$/.test(email)) || !email) {
            validationClass("#input-email-div", "success");
        }
        else {
            validationClass("#input-email-div", "error");
        }
    });
}
$("#register-btn").click(function(){
   if ($("div.has-feedback").children("span.glyphicon-ok").length >= 3){
       $("input#validation-input").val("false");
   }else{
        $("#input-password").val("");
        $("#input-password-div").removeClass("has-success has-error").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove")
        $("#input-verify").val("");
        $("#input-verify-div").removeClass("has-success has-error").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove")

   }
});



