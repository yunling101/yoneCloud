var Controller = {
    config: {
        "add": "add_business",
        "del": "delete_business"
    },
    index: function () {
        if (!Fast.permission(Controller.config.add)){
            $("#toolbar .btn-add").remove();
        }

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "api/v1/business/lists",
                "add_url": Fast.permission(Controller.config.add) ? "business/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "business/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "business/delete/" : "",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function() {
                   return function(){
                   }
                },
                edit: function(rows) {
                   return function() {
                       for(var k in rows){
                          var node = $("input[name='"+ k +"']");
                          if (node.length == 1){
                              node.val(rows[k]);
                          }
                       }
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
    }
};