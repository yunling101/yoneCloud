/* 忘记密码 */
$(function () {
    var Controller = {
        index: function(){
           $("input[name=code]").val('');
           $(document).on("click", "#sendPassword", function(){
               var that = $(this);
               var email = $("input[name=email]").val();
               var code = $("input[name=code]").val();

               if (/^ *$/.test(email)){
                  $("input[name=email]").parent().addClass("has-error");
                  return
               }else{
                  $("input[name=email]").parent().removeClass("has-error");
               }

               if (code == ''){
                   jQuery.ajax({
                         "url": "/forgot/code/",
                         "type": "POST",
                         "dataType": "json",
                         "data": {"email":email},
                         "beforeSend": function(){
                            that.attr("disabled", "disabled");
                            that.text("加载中...");
                         },
                         "complete": function(){
                            that.text("确认重置密码");
                            that.removeAttr("disabled");
                         },
                         "success": function(result){
                             if(result.code){
                                $("#codeDiv").removeClass("hide");
                                return true;
                             }else{
                                $("#errorInfo").text(result.msg);
                                $("#errorInfo").css({'display':'block', "color":"#ed5565"});
                                return false
                             }
                         }
                   });
               }else{
                  jQuery.ajax({
                         "url": "/forgot/password/",
                         "type": "POST",
                         "dataType": "json",
                         "data": {"email":email, "code":code},
                         "beforeSend": function(){
                            that.attr("disabled", "disabled");
                            that.text("正在重置中...");
                         },
                         "complete": function(){
                            that.text("确认重置密码");
                            that.removeAttr("disabled");
                         },
                         "success": function(result){
                             if(result.code){
                                $("#errorInfo").text(result.msg);
                                $("#errorInfo").css({'display':'block', "color":"#676a6c"});
                                window.location.href = "/login/";
                                return true;
                             }else{
                                $("#errorInfo").text(result.msg);
                                $("#errorInfo").css({'display':'block', "color":"#ed5565"});
                                return false
                             }
                         }
                  });
               }
           })
        }
    }
    Controller.index();
});