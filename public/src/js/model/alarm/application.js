var Controller = {
    config: {
        "add": "add_alarm_application",
        "del": "delete_alarm_application"
    },
    index: function () {
        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
        }

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "api/v1/alarm/application/lists",
                "add_url": Fast.permission(Controller.config.add) ? "alarm/application/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "alarm/application/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "alarm/application/delete/" : "",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function () {
                    return function () {
                    }
                },
                edit: function (rows) {
                    return function () {
                        $("input[name='name']").val(rows.name);
                        $("input[name='address']").val(rows.address);
                        $("input[name='id']").val(rows.id);

                        $("textarea[name='comment']").val(rows.comment);
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
                    { field: 'state', checkbox: true },
                    { field: 'sid', title: L('Sid'), align: 'left' },
                    { field: 'name', title: L('Name'), align: 'left' },
                    { field: 'address', title: L('Address'), align: 'left' },
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