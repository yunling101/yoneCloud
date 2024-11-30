var Controller = {
    index: function () {
        Controller.api.render_template();
    },
    api: {
        render_template: function(){
            Fast.api.ajax({"url": "/alarm/template/", "dataType":"json"}, function(data) {
                if (data.code) {
                   $("ul.nav.nav-tabs").html("");
                   $("#myTabContent").html("");
                   for(var i in data.rows){
                       var rows = data.rows[i];
                       if (rows.ename == "mail") {
                          $("ul.nav.nav-tabs").append('<li><a class="nav-link active" href="#'+ rows.ename +'" data-toggle="tab">'+ rows.cname +'</a></li>');
                       }else{
                          $("ul.nav.nav-tabs").append('<li><a class="nav-link" href="#'+ rows.ename +'" data-toggle="tab">'+ rows.cname +'</a></li>');
                       }
                       Fast.api.render("alarm/templateLine", function(html){
                          $("#myTabContent").append(ejs.render(html, {
                                name: rows.ename,
                                config: rows.config
                          }));
                       });
                   }
                }else{
                   Toastr.error(data.msg);
                   return false;
                }

                Form.api.bindevent($('[role="form"]'));
            });
        }
    }
};