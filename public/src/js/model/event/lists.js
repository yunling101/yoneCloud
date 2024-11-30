var Controller = {
    config: {
        "del": "delete_event"
    },
    index: function () {
        if (!Fast.permission(Controller.config.del)){
            $("#toolbar .btn-del").remove();
        }

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "event/lists",
                "add_url": "",
                "edit_url": "",
                "del_url": Fast.permission(Controller.config.del) ? "event/delete/" : "",
                "multi_url": "event/change/",
                "form": true
            }
        });
        var table = $("#table");

        // 初始化表格
        table.bootstrapTable({
            url: $.fn.bootstrapTable.defaults.extend.index_url,
            columns: [
                [
                    {field: 'state', checkbox: true},
                    {field: 'status', title: L('Is active'), formatter: Controller.api.formatter.status},
                    {field: 'id', title: 'ID'},
                    {field: 'event_type', title: L('Type')},
                    {field: 'event_title', title: L('Title'), align: 'left'},
                    // {field: 'username', title: "L('Username')", align: 'left'},
                    {field: 'create_time', title: L('Create time'), formatter: Table.api.formatter.datetime},
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        buttons: [{
                            name: 'detail',
                            text: L('Detail'),
                            icon: 'fa fa-list',
                            classname: 'btn btn-info btn-xs btn-detail btn-dialog',
                            callback: Controller.api.detail,
                            url: 'event/detail'
                        }],
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
        formatter: {
            status: function(value, row, index){
               if (value){
                  return '<span style="color: #337ab7;"><i class="fa fa-circle"></i> 未读</span></a>'
               }else{
                  return '<span class="text-primary"><i class="fa fa-circle"></i> 已读</span></a>'
               }
            }
        },
        detail: function(url){
            Fast.api.ajax({"url": url, "dataType":"json"}, function(data) {
                if (data.code){
                   var tr = "";
                   for (var k in data.msg){
                     if (k != "id" && k != "username"){
                        if (data.msg[k] != null && data.msg[k] !=""){
                            tr += "<tr><td>"+L(k.replace("_", " "))+"</td><td>"+ data.msg[k] +"</td></tr>";
                        }
                     }
                   }
                   $("#detailBody").html(tr);
                }else{
                   Toastr.error(data.msg);
                   return false;
               }
            });
        }
    }
};