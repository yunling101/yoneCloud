var Controller = {
    index: function () {
        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "/api/v1/permission/lists",
                "add_url": "user/perm/add",
                "edit_url": "user/perm/add",
                "del_url": "user/perm/delete/",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function () {
                    return function () {
                    }
                },
                edit: function (rows) {
                    return function () {
                        for (var k in rows) {
                            if (k == "comment") {
                                $("textarea[name='comment']").text(rows[k]);
                            } else {
                                var node = $("input[name='" + k + "']");
                                if (node.length == 1) {
                                    node.val(rows[k]);
                                }
                            }
                        }
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
                    { field: 'name', title: L('Name'), align: 'left' },
                    { field: 'menu', title: L('Menu'), align: 'left' },
                    { field: 'view', title: L('View'), align: 'left' },
                    { field: 'comment', title: L('comment'), align: 'left' },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: Table.api.formatter.operate
                    }
                ]
            ],

        });

        // 为表格绑定事件
        Table.api.bindevent(table);
        Controller.api.bindevent();
    },
    api: {
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