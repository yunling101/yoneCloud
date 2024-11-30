var Controller = {
    index: function () {
        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "white/lists",
                "add_url": "system/white/add",
                "edit_url": "system/white/add",
                "del_url": "white/delete/",
                "multi_url": "",
                "form": true
            },
            callback: {
                edit: function (rows) {
                    return function () {
                        $("textarea[name=comment]").val(rows.comment);
                        $("input[name=address]").val(rows.ip);
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
                    { field: 'state', checkbox: true, },
                    { field: 'id', title: 'ID' },
                    { field: 'ip', title: L('Address'), align: 'left' },
                    { field: 'username', title: L('Username'), align: 'left' },
                    { field: 'create_time', title: L('Create time'), formatter: Table.api.formatter.datetime },
                    { field: 'comment', title: L('Comment'), align: 'left' },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: Table.api.formatter.operate
                    }
                ]
            ],
            commonSearch: false,
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    }
};