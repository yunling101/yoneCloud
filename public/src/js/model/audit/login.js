var Controller = {
    index: function () {
         Table.api.init({
            extend: {
                "index_url": "api/v1/audit/login",
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
                    {field: 'username', title: L('Username')},
                    {field: 'source', title: L('source')},
                    {field: 'ip', title: L('Address')},
                    {field: 'session_key', title: L('session')},
                    {field: 'date_added', title: L('Time'), align: 'left', formatter: Table.api.formatter.datetime}
                ]
            ],
            commonSearch: false,
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    }
}