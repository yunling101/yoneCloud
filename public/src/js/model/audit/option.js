var Controller = {
    index: function () {
         Table.api.init({
            extend: {
                "index_url": "api/v1/audit/option",
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
                    {field: 'object', title: L('Object'), align: 'left'},
                    {field: 'ip', title: L('Address')},
                    {field: 'username', title: L('Username')},
                    {field: 'date_added', title: L('Time'), formatter: Table.api.formatter.datetime}
                ]
            ],
            commonSearch: false,
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    }
}