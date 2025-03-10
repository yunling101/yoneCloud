var Controller = {
    config: {
        "add": "add_network",
        "del": "delete_network"
    },
    index: function () {
        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
        }

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "/api/v1/network/lists",
                "add_url": Fast.permission(Controller.config.add) ? "resources/network/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "resources/network/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "resources/network/delete/" : "",
                "multi_url": "resources/network/monitor/",
                "form": true
            },
            callback: {
                html: function () {
                },
                add: function () {
                    return function () {
                        Controller.api.get_network_type();
                    }
                },
                edit: function (rows) {
                    return function () {
                        Controller.api.get_network_type();

                        if (rows.network_type) {
                            $("#network_type").find("option[value=" + rows.network_type + "]").attr("selected", true);
                        }
                        if (rows.monitoring_status) {
                            $("#monitoring_status").find("option[value=1]").attr("selected", true);
                        }
                        for (var k in rows) {
                            var node = $("form[role=form] input[name='" + k + "']");
                            if (node.length == 1) {
                                node.val(rows[k]);
                            }
                        }
                        $("#comment").val(rows.other_info);
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
                    { field: 'id', title: 'ID', formatter: Controller.api.formatter.id },
                    { field: 'name', title: L('Name'), align: 'left' },
                    { field: 'address', title: L('Address'), align: 'left' },
                    { field: 'monitoring_status', title: L('Monitor'), formatter: Controller.api.formatter.monitor },
                    { field: 'network_type', title: L('Type') },
                    { field: 'network_model', title: L('Model') },
                    { field: 'region', title: L('Position') },
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
            commonSearch: false
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        formatter: {
            id: function (value, row, index) {
                if (row.monitoring_status && row.monitoring_address) {
                    var m = '<a target="_blank" href="' + row.monitoring_address + '" style="padding-left:8px;"><i class="fa fa-bar-chart-o"></i></a>';
                } else {
                    var m = '<a style="padding-left:8px;color:#abacad;pointer-events:none;"><i class="fa fa-bar-chart-o"></i></a>';
                }
                return value + m;
            },
            monitor: function (value, row, index) {
                var m = '<span class="text-danger">Disabled</span>';
                if (value) {
                    m = '<span class="text-success">Enabled</span>';
                }
                return '<a href="javascript:;" data-toggle="tooltip" class="btn-change" data-id="' + row.id + '">' + m + '</a>';
            }
        },
        get_network_type: function (network_type) {
            Fast.api.ajax({ "url": "/resources/network_type/", "dataType": "json", "async": false }, function (data) {
                if (data.code) {
                    if (data.data != null) {
                        for (var k in data.data) {
                            if (network_type == k) {
                                var h = '<option value="' + data.data[k] + '" selected>' + data.data[k] + '</option>';
                            } else {
                                var h = '<option value="' + data.data[k] + '">' + data.data[k] + '</option>';
                            }
                            $("select[name=network_type]").append(h)
                        }
                    }
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        }
    }
};