var Controller = {
    configs: [],
    default_config: {},
    index: function () {
        Table.api.init({
            extend: {
                "index_url": "api/v1/alarm/route/lists",
                "add_url": "alarm/route/add",
                "edit_url": "alarm/route/add",
                "del_url": "alarm/route/delete/",
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
                        $("input[name='name']").attr("readonly", true);
                        for (var k in rows) {
                            var node = $("input[name='" + k + "']");
                            if (node.length == 1) {
                                node.val(rows[k]);
                            }
                        }
                        $("input[name='route_id']").val(rows.id);
                        $("textarea[name='match']").val(rows.match);
                    }
                },
            }
        });

        var table = $("#table");
        // 初始化表格
        table.bootstrapTable({
            url: $.fn.bootstrapTable.defaults.extend.index_url,
            columns: [
                [
                    { field: 'state', checkbox: true },
                    { field: 'name', title: L('Name') },
                    { field: 'group_by', title: "报警分组" },
                    { field: 'group_wait', title: "等待时间" },
                    { field: 'group_interval', title: "间隔时间" },
                    { field: 'repeat_interval', title: "重复时间" },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: function (value, row, index) {
                            var disable = false;
                            if (row.id == 1) {
                                disable = true
                            }
                            return Table.api.formatter.operate.call(this, value, row, index, disable);
                        }
                    }
                ]
            ],
            pagination: false,
            search: false,
        });
        // 为表格绑定事件
        Table.api.bindevent(table);

        Fast.api.ajax({ "url": "/alarm/route/", "dataType": "json", "async": false }, function (ret) {
            if (ret.code) {
                for (var r in ret.rows) {
                    var v = ret.rows[r];
                    $("select[name=alarm-router]").append('<option value="' + v.id + '">' + v.name + '</option>');
                }
            } else {
                Toastr.error(data.msg);
                return false;
            }
        });

        Controller.api.defaultConfig();
        Controller.api.alarmGlobalConfig();
        Controller.api.alarmConfig();

        $("select[name=alarm-router]").on("change", function () {
            Controller.api.alarmConfig();
        });
    },
    api: {
        getInput: function (name, value) {
            var label = '<label class="col-form-label">' + name + '</label>';
            var div = '<input type="text" name="' + name + '" value="' + value + '" class="form-control m-b" />'
            return label + div;
        },
        getSelect: function (name, value) {
            var label = '<label class="col-form-label">' + name + '</label>';
            var select = '<select name="' + name + '" class="form-control form-control-lg m-b">';
            select += '<option value="0">关闭</option>'
            if (value == "1") {
                select += '<option value="1" selected="selected">开启</option>'
            } else {
                select += '<option value="1">开启</option>'
            }
            select += "</select>";
            return label + select;
        },
        getDivBlock: function (child, idx, index) {
            var div = document.createElement("div");
            div.style.cssText = 'border: 1px dashed #e7eaec;padding:15px;margin-bottom:15px;'
            div.innerHTML = child;
            var a = document.createElement("a");
            a.setAttribute("href", "javascript:void(0)");
            a.setAttribute("parent", idx);
            a.setAttribute("index", index);
            a.textContent = "删除";
            a.onclick = function () {
                $(this).parent().remove();
                var i = $(this).attr("index");
                Controller.configs[$(this).attr("parent")].config.splice(parseInt(i), 1);
            }
            div.appendChild(a);
            return div;
        },
        configsMap: function (configs) {
            for (var i in configs) {
                var row = configs[i];
                $("#configs_" + row.ename).html('');
                for (var j in row.config) {
                    var line = row.config[j];
                    var rowBlock = '';
                    for (var k in line) {
                        var v = line[k];
                        if (k == "send_resolved") {
                            rowBlock += Controller.api.getSelect(k, v)
                        } else {
                            rowBlock += Controller.api.getInput(k, v)
                        }
                    }
                    $("#configs_" + row.ename).append(Controller.api.getDivBlock(rowBlock, i, j));
                }
            }
        },
        defaultConfig: function () {
            Fast.api.ajax({ "url": "/default_alertmanager_config/", "dataType": "json", "async": false }, function (data) {
                Controller.default_config = data;
            })
        },
        alarmConfig: function () {
            var route = $("select[name=alarm-router]").val();
            Fast.api.ajax({ "url": "/alarm/config/?route=" + route, "dataType": "json" }, function (data) {
                if (data.code && data.total != 0) {
                    $("ul.nav.nav-configs").html("");
                    $("#configsTabContent").html("");
                    for (var i in data.rows) {
                        var rows = data.rows[i];
                        if (rows.ename == "email_configs") {
                            $("ul.nav.nav-configs").append('<li><a class="nav-link active" href="#' + rows.ename + '" data-toggle="tab">' + L(rows.ename) + '</a></li>');
                        } else {
                            $("ul.nav.nav-configs").append('<li><a class="nav-link" href="#' + rows.ename + '" data-toggle="tab">' + L(rows.ename) + '</a></li>');
                        }
                        Fast.api.render("alarm/configLine", function (html) {
                            $("#configsTabContent").append(ejs.render(html, { name: rows.ename, config: rows.config, index: i }));
                        });
                    }

                    Controller.api.configsMap(data.rows);
                    Controller.configs = data.rows;

                    $("button#subClick").on("click", function () {
                        for (var i in Controller.configs) {
                            var row = Controller.configs[i];
                            if (row.ename == $(this).attr("name")) {
                                var j = row.config.length + 1;
                                var line = Controller.default_config[row.ename];
                                var rowBlock = '';
                                var rowObject = {};
                                for (var k in line) {
                                    if (k == "send_resolved") {
                                        rowBlock += Controller.api.getSelect(k, "")
                                    } else {
                                        rowBlock += Controller.api.getInput(k, "")
                                    }
                                    rowObject[k] = ""
                                }
                                Controller.configs[i].config.push(rowObject);
                                $("#configs_" + row.ename).append(Controller.api.getDivBlock(rowBlock, i, j - 1));
                                break
                            }
                        }
                    });

                    $("button#subSubmit").on("click", function () {
                        var index = $(this).attr("index");
                        for (var i in Controller.configs) {
                            var row = Controller.configs[i];
                            if (row.ename == $(this).attr("name")) {
                                for (var j in row.config) {
                                    var v = row.config[j];
                                    for (var k in v) {
                                        var value = $("[name=" + k + "]").val()
                                        if (k == "send_resolved") {
                                            var value = $("select[name=" + k + "]").eq(index).val()
                                        }
                                        if (value == undefined) {
                                            value = ""
                                        }
                                        Controller.configs[i].config[j][k] = value;
                                    }
                                }
                                break
                            }
                        }
                        Controller.api.alarmConfigSubmit(Controller.configs);
                    });
                } else if (data.code && data.total == 0) {
                    var configs = []
                    for (var k in Controller.default_config) {
                        configs.push({ route: route, ename: k, config: [Controller.default_config[k]] });
                    }
                    Controller.configs = configs;
                    Controller.api.configsMap(configs);
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        },
        alarmConfigSubmit: function (data) {
            Fast.api.ajax({
                "url": "/alarm/config/",
                "dataType": "json",
                "type": "post",
                "data": JSON.stringify(data)
            }, function (res) {
                if (res.code) {
                    Toastr.success("操作成功");
                    return true
                } else {
                    Toastr.error(res.msg);
                }
            })
        },
        alarmGlobalConfig: function () {
            Fast.api.ajax({ "url": "/alarm/global/config/", "dataType": "json" }, function (data) {
                if (data.code) {
                    $("ul.nav.nav-global").html("");
                    $("#globalTabContent").html("");
                    for (var i in data.rows) {
                        var rows = data.rows[i];
                        if (i == 0) {
                            $("ul.nav.nav-global").append('<li><a class="nav-link active" href="#' + rows.ename + '" data-toggle="tab">' + rows.cname + '</a></li>');
                        } else {
                            $("ul.nav.nav-global").append('<li><a class="nav-link" href="#' + rows.ename + '" data-toggle="tab">' + rows.cname + '</a></li>');
                        }
                        Fast.api.render("alarm/configGlobalLine", function (html) {
                            $("#globalTabContent").append(ejs.render(html, {
                                name: rows.ename,
                                config: rows.config,
                            }));
                        });
                    }
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
                Form.api.bindevent($('[role="globalForm"]'));
            });
        }
    }
};