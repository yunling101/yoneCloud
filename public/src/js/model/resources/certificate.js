var Controller = {
    config: {
        "add": "add_hosts_certificate",
        "del": "delete_hosts_certificate"
    },
    index: function () {
        if (!Fast.permission(Controller.config.add)){
            $("#toolbar .btn-add").remove();
        }

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "api/v1/certificate/lists",
                "add_url": Fast.permission(Controller.config.add) ? "certificate/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "certificate/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "auth/certificate/delete/" : "",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function() {
                   return function(){
                        Controller.api.change();
                   }
                },
                edit: function(rows) {
                   return function() {
                       Controller.api.change();

                       $("#ssh_type").find("option[value="+rows.ssh_type+"]").attr("selected", true);
                       $("textarea[name='ssh_key']").val(rows.ssh_key);
                       for(var k in rows){
                          var node = $("input[name='"+ k +"']");
                          if (node.length == 1){
                              node.val(rows[k]);
                          }
                       }
                       Controller.api.change_form(rows.ssh_type);
                   }
                }
            }
        });

        var table = $("#table");
        // 初始化表格
        table.bootstrapTable({
            url: $.fn.bootstrapTable.defaults.extend.index_url,
            columns: [
                [
                    {field: 'state', checkbox: true,},
                    {field: 'id', title: 'ID'},
                    {field: 'name', title: L('Name'), align: 'left'},
                    {field: 'ssh_type', title: L('Type'), align: 'left'},
                    {field: 'ssh_user', title: L('Username'), align: 'left'},
                    {field: 'ssh_port', title: L('Port'), align: 'left'},
                    {field: 'create_time', title: L('Create time'), formatter: Table.api.formatter.datetime},
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: Table.api.formatter.operate
                    }
                ]
            ]
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        change_form: function(value){
            if (value == "KEY") {
                $("input[name='ssh_password']").parent().parent().addClass("hide");
                $("textarea[name='ssh_key']").parent().parent().removeClass("hide");
            }else if (value == "PASSWORD"){
                $("input[name='ssh_password']").parent().parent().removeClass("hide");
                $("textarea[name='ssh_key']").parent().parent().addClass("hide");
            }
        },
        change: function(){
            $("#ssh_type").change(function() {
                var ssh = $(this).val();
                Controller.api.change_form(ssh);
            });
        }
    }
};