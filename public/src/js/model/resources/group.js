var Controller = {
    config: {
        "add": "add_asset_group",
        "del": "delete_asset_group",
    },
    index: function () {
        $("<link>").attr({
            rel: "stylesheet",
            type: "text/css",
            href: "/public/static/js/duallistbox/duallistbox.min.css"
        }).appendTo("head");
        $.getScript("/public/static/js/duallistbox/duallistbox.min.js");

        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
        }
        if (!Fast.permission(Controller.config.del)) {
            $("#toolbar .btn-del").remove();
        }

        Table.api.init({
            extend: {
                "index_url": "api/v1/group/lists",
                "add_url": Fast.permission(Controller.config.add) ? "resources/group/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "resources/group/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "resources/hosts/group/delete/" : "",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function () {
                    return function () {
                        Controller.api.change();
                    }
                },
                edit: function (rows) {
                    return function () {
                        Controller.api.change(rows.hosts);
                        $("input[name='name']").val(rows.name);
                        $("input[name='id']").val(rows.id);
                        $("#comment").val(rows.comment);
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
                    { field: 'state', checkbox: true, },
                    { field: 'id', title: 'ID' },
                    { field: 'name', title: "分组" + L('Name') },
                    { field: 'hosts', title: L('Hosts') + "数", formatter: Controller.api.formatter.hosts },
                    { field: 'comment', title: L('Comment') + "信息" },
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
    },
    api: {
        formatter: {
            hosts: function (value, row, index) {
                if (value != null && value.length != 0) {
                    return value.length + "个";
                } else {
                    return 0 + "个";;
                }
            }
        },
        change: function (hosts) {
            $(".content").toggleClass("sk-loading");
            Fast.api.ajax({ "url": "/resources/hosts/pool/", "dataType": "json" }, function (data) {
                if (data.code) {
                    if (data.rows != null && data.rows.length != 0) {
                        for (var i = 0; i < data.rows.length; i++) {
                            var v = data.rows[i];
                            if (hosts != undefined && hosts.indexOf(v.id) != -1) {
                                var o = '<option value="' + v.id + '" selected>' + v.hostname + '</option>'
                            } else {
                                var o = '<option value="' + v.id + '">' + v.hostname + '</option>'
                            }
                            $("#select_hosts").append(o);
                        }
                        $("#select_hosts").bootstrapDualListbox({
                            nonSelectedListLabel: '可选择主机',
                            selectedListLabel: '已选择主机',
                            infoText: '共{0}个可选',
                            infoTextEmpty: '空列表',
                            filterPlaceHolder: '过滤',
                            selectorMinimalHeight: 160,
                        });
                        $(".content").toggleClass("sk-loading");
                    }
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        }
    }
}