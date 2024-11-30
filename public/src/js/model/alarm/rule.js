var Controller = {
    config: {
        "add": "add_alarm_rule",
        "del": "delete_alarm_rule"
    },
    index: function () {
        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
        }
        // Controller.api.label_name();

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "api/v1/alarm/rule/lists",
                "add_url": Fast.permission(Controller.config.add) ? "alarm/rule/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "alarm/rule/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "alarm/rule/delete/" : "",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function () {
                    return function () {
                        Controller.api.group();

                        $("input[name='interval']").val("5m");
                        $("input[name='title']").val("{{ $labels.instance }} of webserver has been down");
                        $("textarea[name='content']").val("{{ $labels.instance }} of job {{ $labels.job }} webserver has been down");
                    }
                },
                edit: function (rows) {
                    return function () {
                        Controller.api.group(rows.group);
                        $("input[name='name']").attr("readonly", true);
                        $("select[name='group']").attr("readonly", true);
                        $("select[name='group']").on("mousedown", function (e) {
                            e.preventDefault(); // 阻止下拉框打开
                        });

                        $("input[name='name']").val(rows.name);
                        $("input[name='interval']").val(rows.interval);
                        $("input[name='id']").val(rows.id);
                        $("input[name='title']").val(rows.title);
                        $("textarea[name='content']").val(rows.content);
                        $("input[name='desc']").val(rows.desc);
                        $("textarea[name='rules']").val(rows.expression);

                        try {
                            var tags = JSON.parse(rows.tags)
                            $("#level").find("option[value=" + tags.severity + "]").attr("selected", true);
                        } catch (e) { console.log(e) }
                    }
                },
                // del: function (rows) {
                //     return { "group": rows.alarm_group }
                // }
            }
        });

        var table = $("#table");
        // 初始化表格
        table.bootstrapTable({
            url: $.fn.bootstrapTable.defaults.extend.index_url,
            columns: [
                [
                    { field: 'state', checkbox: true },
                    { field: 'name', title: L('Alarm name'), align: 'left' },
                    { field: 'alarm_group', title: L('Alarm group'), align: 'left' },
                    { field: 'interval', title: L('For'), align: 'left' },
                    {
                        field: 'expression', title: L('expr'), align: 'left',
                        formatter: Controller.api.formatter.expr
                    },
                    { field: 'desc', title: L('Description'), align: 'left' },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: Table.api.formatter.operate
                    }
                ]
            ],
            pagination: false,
            search: false,
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        formatter: {
            expr: function (value, row, index) {
                if (value.length > 30) {
                    return text.substr(0, 30) + "..."
                }
                return value;
            }
        },
        group: function (pid) {
            Fast.api.ajax({ "url": "/alarm/rule/group/", "dataType": "json" }, function (data) {
                if (data) {
                    for (var i = 0; i < data.length; i++) {
                        var v = data[i];
                        if (pid == undefined) {
                            var option = '<option value="' + v.en_name + '">' + v.zh_name + '</option>';
                        } else {
                            if (pid == v.group) {
                                var option = '<option value=' + v.en_name + ' selected="selected" disabled>' + v.zh_name + '</option>';
                            }
                        }
                        $("#group").append(option);
                    }
                }
            });
        },
        label_name: function () {
            $("textarea[name='rules']").typeahead({
                loadingAnimation: true,
                fitToElement: false,
                items: 'all',
                source: function (query, process) {
                    return $.ajax({
                        url: '/alarm/rule/label/?_=' + moment(new Date()).valueOf(),
                        type: 'GET',
                        dataType: "json",
                        success: function (result) {
                            $("textarea[name='rules']").typeahead('close');
                            $("textarea[name='rules']").focus();
                            if (result.code) {
                                return process(result.data);
                            } else {
                                return process([]);
                            }
                        },
                    });
                }
            });
        }
    }
};