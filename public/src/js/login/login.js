/* 登录 */
$(function () {
    var Controller = {
        login: function () {
             var username = $("#username").val();
             var password = $("#password").val();

             if (/^ *$/.test(username)){
                $("#username").parent().addClass("has-error");
                return
             }else{
                $("#username").parent().removeClass("has-error");
             }
             if (/^ *$/.test(password)){
                $("#password").parent().addClass("has-error");
                return
             }else{
                $("#password").parent().removeClass("has-error");
             }

             jQuery.ajax({
                 "url": "/login_user/",
                 "type": "POST",
                 "dataType": "json",
                 "data": {"username":username,"password":password},
                 "success": function(result){
                     if(result.ret){
                        window.location.href = "/";
                        return true;
                     }else{
                        $("#errorInfo").text(result.msg);
                        $("#errorInfo").css({'display':'block', "color":"#ed5565"});
                        return false
                     }
                 }
             });
        },
        index: function () {
            $("#username").keyup(function(e){
                if (e.keyCode == 13){
                   Controller.login();
                }
            });
            $("#password").keyup(function(e){
                if (e.keyCode == 13){
                   Controller.login();
                }
            });
            $("#loginSubmit").on("click", function(){
                Controller.login();
            })
        }
    }
    Controller.index();
});