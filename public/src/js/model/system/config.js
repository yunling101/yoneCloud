var Controller = {
   index: function () {
      Fast.api.ajax({ "url": "system/config", "dataType": "json" }, function (data) {
         if (data.code) {
            for (var i in data.rows) {
               var rows = data.rows[i];
               if (rows.ename == "basic") {
                  $("ul.nav.nav-tabs").append('<li><a class="nav-link active" href="#' + rows.ename + '" data-toggle="tab">' + rows.cname + '</a></li>');
               } else {
                  $("ul.nav.nav-tabs").append('<li><a class="nav-link" href="#' + rows.ename + '" data-toggle="tab">' + rows.cname + '</a></li>');
               }
               var textarea = ["whitelist", "describe", "forbiddenip", "authorize"];
               Fast.api.render("system/configLine", function (html) {
                  $("#myTabContent").append(ejs.render(html, {
                     name: rows.ename,
                     config: rows.config,
                     textarea: textarea
                  }));
               });
            }

            $("input[name='logoFile']").on("change", function () {
               var data = new FormData();
               var obj = $(this)[0].files[0];
               data.append("data", obj);

               Fast.api.ajax({
                  "url": "/logo/upload/",
                  "dataType": "json",
                  "type": "POST",
                  "data": data,
                  "cache": false,
                  "processData": false,
                  "contentType": false
               }, function (res) {
                  if (res.code) {
                     document.getElementById("logoId").src = res.msg;
                     return true;
                  } else {
                     Toastr.error(res.msg);
                     return false;
                  }
               });
            });

            $(".basic-logo").on("click", "#logoDefault", function () {
               Fast.api.ajax({ "url": "/logo/default/", "dataType": "json", "type": "POST" }, function (res) {
                  if (res.code) {
                     location.reload();
                     return true;
                  } else {
                     Toastr.error(res.msg);
                     return false;
                  }
               });
            });
         } else {
            Toastr.error(data.msg);
            return false;
         }

         Form.api.bindevent($('[role="form"]'));
      });
   }
}