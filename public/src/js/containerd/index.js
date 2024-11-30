// 初始化
//$(function () {
//    Fast.view();
//    window.onhashchange = function() {
//        Fast.view();
//    }
//
//    $("body").on("click", "*[hunt-href]", function() {
//        var e = $(this);
//        var t = e.attr("hunt-href");
//
//        location.hash = Fast.correctRouter(t);
//    });
//});

var Controller = {
    index: function () {
        Table.api.init({
            extend: {
                "index_url": "",
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
                    {field: 'state', checkbox: true},
                    {field: 'id', title: '状态'},
                    {field: 'username', title: L('Name')},
                    {field: 'source', title: L('Role')},
                    {field: 'ip', title: L('Version')},
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
Controller.index();