var Controller = {
    config: {
        "add": "add_user",
        "del": "delete_user"
    },
    index: function () {
        // 初始化表格参数配置
        if (!Fast.permission(Controller.config.add)){
            $("#toolbar .btn-add").remove();
        }
        Table.api.init({
            extend: {
                "index_url": "api/v1/user/lists",
                "add_url": Fast.permission(Controller.config.add) ? "user/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "user/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "user/delete/" : "",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function() {
                   return function(pid){
                        Fast.api.ajax({"url":$.fn.bootstrapTable.defaults.extend.index_url, "dataType":"json"}, function(data) {
                           if (data.code){
                              for (var i=0;i<data.rows.length;i++){
                                 if (pid == data.rows[i].id){
                                    var option = '<option value='+ data.rows[i].id +' selected="selected">'+ data.rows[i].title +'</option>';
                                 }else{
                                    var option = '<option value='+ data.rows[i].id +'>'+ data.rows[i].title +'</option>';
                                 }

                                 $("#pid").append(option);
                                 Controller.api.role(null);
                              }
                           }
                        });
                   }
                },
                edit: function(rows) {
                   return function() {
                       $("input[name=password]").parent().parent().remove();
                       $("#is_active").find("option[value="+rows.is_active+"]").attr("selected", true);
                       for(var k in rows){
                          var node = $("input[name='"+ k +"']");
                          if (node.length == 1){
                              node.val(rows[k]);
                          }
                       }

                       Controller.api.role(rows.role);
                   }
                }
            }
        });

        var table = $("#table");
        // 初始化表格
        table.bootstrapTable({
            url: $.fn.bootstrapTable.defaults.extend.index_url,
            escape: false,
            columns: [
                [
                    {field: 'state', checkbox: true,},
                    {field: 'id', title: 'ID'},
                    {field: 'sid', title: 'UID'},
                    {field: 'username', title: L('Username'), align: 'left'},
                    {field: 'nickname', title: L('Nickname'), align: 'left'},
                    {field: 'email', title: L('Email'), align: 'left'},
                    {field: 'is_active', title: L('Is active'), formatter: Table.api.formatter.status},
                    {field: 'role', title: L('Role'), align: 'left'},
                    {field: 'last_login', title: L('Last login'), formatter: Table.api.formatter.datetime},
                    {field: 'operate', title: L('Operate'), table: table, events: Table.api.events.operate,
                        formatter: function (value, row, index) {
                            if(row.id == 1){
                                return '';
                            }
                            return Table.api.formatter.operate.call(this, value, row, index);
                        }
                    }
                ]
            ]
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        role: function(name) {
            Fast.api.ajax({"url":"/user/role/", "dataType":"json"}, function(data) {
                if (data.code){
                   $("#role").html('<option value="">------</option>');
                   for(var i=0;i<data.rows.length;i++){
                      var v = data.rows[i];
                      if (name == v.name) {
                         $("#role").append('<option value="'+v.id+'" selected>'+v.name+'</option>');
                      }else{
                         $("#role").append('<option value="'+v.id+'">'+v.name+'</option>');
                      }
                   }
                }else{
                   Toastr.error("角色获取出错！");
                   return false;
                }
            });
        }
    }
};