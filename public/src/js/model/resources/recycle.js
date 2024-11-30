var Controller = {
    index: function () {
        Table.api.init({
            extend: {
                "index_url": "api/v1/recycle/lists",
                "add_url": "",
                "edit_url": "",
                "del_url": "system/recycle/delete/",
                "multi_url": "",
                "form": true
            },
            callback: {
                html: function () {
                },
                add: function () {
                },
                edit: function (rows) {
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
                    { field: 'id', title: 'ID' },
                    { field: 'name', title: L('Name'), align: 'left' },
                    { field: 'ip', title: L('Address') },
                    { field: 'type', title: L('Type'), align: 'left' },
                    { field: 'username', title: L('Username') },
                    { field: 'create_time', title: L('Create time'), formatter: Table.api.formatter.datetime },
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
}