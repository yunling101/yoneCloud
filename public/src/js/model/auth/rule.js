var Controller = {
    index: function () {
        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "auth/rule",
                "add_url": "auth/add",
                "edit_url": "auth/add",
                "del_url": "auth/delete/",
                "multi_url": "auth/change/",
                "form": true
            },
            callback: {
                add: function () {
                    return function (pid) {
                        Fast.api.ajax({ "url": $.fn.bootstrapTable.defaults.extend.index_url, "dataType": "json" }, function (data) {
                            if (data.code) {
                                for (var i = 0; i < data.rows.length; i++) {
                                    if (data.rows[i].pid != 0) {
                                        var title = data.rows[i].spacer + " " + data.rows[i].title;
                                    } else {
                                        var title = data.rows[i].title;
                                    }
                                    if (pid == data.rows[i].id) {
                                        var option = '<option value=' + data.rows[i].id + ' selected="selected">' + title + '</option>';
                                    } else {
                                        var option = '<option value=' + data.rows[i].id + '>' + title + '</option>';
                                    }

                                    $("#pid").append(option);
                                }
                            }
                        });
                    }
                },
                edit: function (rows) {
                    return function () {
                        $.fn.bootstrapTable.defaults.callback.add()(rows.pid);
                        if (rows.ismenu) {
                            $("input[name=ismenu][value=1]").attr("checked", true);
                        } else {
                            $("input[name=ismenu][value=0]").attr("checked", true);
                        }
                        $("#pid").find("option[value=1]").attr("selected", true);
                        for (var k in rows) {
                            var node = $("input[name='" + k + "']");

                            if (node.length == 1) {
                                if (k == "title") {
                                    node.val(rows.title.replace("&nbsp;├ ", ''));
                                } else {
                                    node.val(rows[k]);
                                }
                            }
                        }
                        if (rows.status) {
                            $("input[name=status][value=1]").attr("checked", true);
                        } else {
                            $("input[name=status][value=0]").attr("checked", true);
                        }
                    }
                }
            }
        });

        var table = $("#table");
        // 初始化表格
        table.bootstrapTable({
            url: $.fn.bootstrapTable.defaults.extend.index_url,
            sortName: 'weigh',
            escape: false,
            columns: [
                [
                    { field: 'state', checkbox: true, },
                    { field: 'id', title: 'ID' },
                    { field: 'title', title: L('Title'), align: 'left', formatter: Controller.api.formatter.title },
                    { field: 'entitle', title: L('EnTitle'), align: 'left' },
                    { field: 'icon', title: L('Icon'), formatter: Controller.api.formatter.icon },
                    { field: 'name', title: L('Name'), align: 'left', formatter: Controller.api.formatter.name },
                    { field: 'weigh', title: L('Weigh') },
                    { field: 'priority', title: L('Priority') },
                    { field: 'status', title: L('Status'), formatter: Table.api.formatter.status },
                    { field: 'ismenu', title: L('Ismenu'), align: 'center', formatter: Table.api.formatter.toggle },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: function (value, row, index) {
                            if (row.id == 1) {
                                return '';
                            }
                            return Table.api.formatter.operate.call(this, value, row, index);
                        }
                    }
                ]
            ],
            pagination: false,
            search: false,
            commonSearch: false,
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
        Controller.api.bindevent();
    },
    api: {
        formatter: {
            title: function (value, row, index) {
                if (row.pid != 0) {
                    return row.spacer + " " + value;
                } else {
                    return value;
                }
            },
            name: function (value, row, index) {
                return !row.ismenu || row.status == 'hidden' ? "<span class='text-muted'>" + value + "</span>" : value;
            },
            icon: function (value, row, index) {
                return '<span class="' + (!row.ismenu || row.status == 'hidden' ? 'text-muted' : '') + '"><i class="' + value + '"></i></span>';
            }
        },
        bindevent: function () {
            var iconlist = [];
            var iconfunc = function () {
                Fast.api.render("auth/tpl", function (e) {
                    Layer.open({
                        type: 1,
                        area: ['700px', '400px'], //宽高
                        zIndex: Layer.zIndex,
                        content: ejs.render(e, { iconlist: iconlist })
                    });
                })
            };
            $(document).on('click', ".btn-search-icon", function () {
                if (iconlist.length == 0) {
                    $.get(Config.cssText + "/variables.less", function (ret) {
                        var exp = /fa-var-(.*):/ig;
                        var result;
                        while ((result = exp.exec(ret)) != null) {
                            iconlist.push(result[1]);
                        }
                        iconfunc();
                    });
                } else {
                    iconfunc();
                }
            });
            $(document).on('click', '#chooseicon ul li', function () {
                $("input[name='icon']").val('fa fa-' + $(this).data("font"));
                var id = $(this).parent().parent().parent().parent().parent().attr("times");
                Layer.close(id);
            });
            $(document).on('keyup', 'input.js-icon-search', function () {
                $("#chooseicon ul li").show();
                if ($(this).val() != '') {
                    $("#chooseicon ul li:not([data-font*='" + $(this).val() + "'])").hide();
                }
            });
        }
    }
};