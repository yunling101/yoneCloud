var Controller = {
    index: function () {
         Table.api.init({
            extend: {
                "index_url": "api/v1/audit/command",
                "add_url": "",
                "edit_url": "",
                "del_url": "",
                "multi_url": "",
                "form": true
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
                    {field: 'log_id', title: L('SID')},
                    {field: 'username', title: L('Username')},
                    {field: 'log_type', title: L('Type')},
                    {field: 'command', title: L('Command')},
                    {field: 'datetime', title: L('Time'),formatter: Table.api.formatter.datetime}
                ]
            ],
            commonSearch: false,
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    }
}