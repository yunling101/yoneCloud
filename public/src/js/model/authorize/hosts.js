$.jstree.core.prototype.get_all_checked = function (full) {
    var obj = {
        "business": []
    }
    $('[aria-selected="true"][aria-level="1"]').each(function () {
        obj.business.push($(this).children("a").text())
    });

    return obj;
};

var Controller = {
    config: {
        "add": "add_hosts_authorize",
        "del": "delete_hosts_authorize"
    },
    index: function () {
        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
        }

        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "api/v1/authorize/lists",
                "add_url": Fast.permission(Controller.config.add) ? "authorize/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "authorize/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "auth/authorize/delete/" : "",
                "multi_url": "",
                "form": false
            },
            callback: {
                add: function () {
                    return function () {
                        Controller.api.change_user();

                        $("#authTree").jstree("destroy");
                        Fast.api.ajax({ "url": "/resources/hosts/batch/", "dataType": "json" }, function (data) {
                            if (data.code) {
                                var result = new Array();
                                for (var business in data.results) {
                                    var child_business = { text: business, children: [] };
                                    for (var i = 0; i < data.results[business].hosts.length; i++) {
                                        var h = data.results[business].hosts[i];
                                        child_business["children"].push({
                                            text: h.hostname,
                                            icon: "fa fa-linux",
                                            ip: h.ip,
                                            sid: h.sid,
                                            hostname: h.hostname,
                                            proxy: h.proxy
                                        })
                                    }
                                    result.push(child_business);
                                }

                                Controller.api.initHostsTree(result);
                                Controller.api.bindForm();
                            } else {
                                Toastr.error(data.msg);
                                return false;
                            }
                        });
                    }
                },
                edit: function (rows) {
                    return function () {
                        Controller.api.change_user(rows.user);

                        $("#authTree").jstree("destroy");
                        Fast.api.ajax({ "url": "/resources/hosts/batch/", "dataType": "json" }, function (data) {
                            if (data.code) {
                                var result = new Array();
                                for (var business in data.results) {
                                    var child_business = { text: business, children: [] };
                                    if (rows.business.indexOf(business) != -1) {
                                        child_business["state"] = { "selected": true }
                                    }
                                    for (var i = 0; i < data.results[business].hosts.length; i++) {
                                        var h = data.results[business].hosts[i];
                                        var hosts = {
                                            text: h.hostname,
                                            icon: "fa fa-linux",
                                            ip: h.ip,
                                            sid: h.sid,
                                            hostname: h.hostname,
                                            proxy: h.proxy
                                        }
                                        if (rows.hosts.indexOf(h.id) != -1) {
                                            hosts["state"] = { "selected": true }
                                        }
                                        child_business["children"].push(hosts)
                                    }
                                    result.push(child_business);
                                }

                                Controller.api.initHostsTree(result);
                                Controller.api.bindForm();
                            } else {
                                Toastr.error(data.msg);
                                return false;
                            }
                        });

                        try {
                            var d = JSON.parse(rows.console)
                            if (d.ssh) {
                                $("select[name='auth_console']").find("option[value=1]").attr("selected", true);
                            }
                            if (d.monitor) {
                                $("select[name='auth_monitor']").find("option[value=1]").attr("selected", true);
                            }
                        } catch (e) {
                        }
                        $("input[name='name']").val(rows.name);
                        $("textarea[name='comment']").val(rows.comment);
                        $("input[name='id']").val(rows.id);
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
                    { field: 'name', title: L('Name') },
                    { field: 'user', title: L('User') },
                    { field: 'business', title: L('Business'), formatter: Controller.api.formatter.business },
                    { field: 'hosts', title: L('Hosts'), formatter: Controller.api.formatter.hosts },
                    { field: 'create_time', title: L('Create time'), formatter: Table.api.formatter.datetime },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: Table.api.formatter.operate
                    }
                ]
            ]
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        formatter: {
            hosts: function (value, row, index) {
                if (value != null && typeof (value) == "object") {
                    return value.length;
                }

                return value
            },
            business: function (value, row, index) {
                if (value != null && typeof (value) == "object") {
                    return value.length;
                }

                return value
            }
        },
        change_user: function (pid) {
            Fast.api.ajax({ "url": "/user/lists/", "dataType": "json", "data": { "super": false } }, function (data) {
                if (data.code) {
                    for (var i = 0; i < data.rows.length; i++) {
                        var v = data.rows[i];
                        if (v.username == pid) {
                            $("select[name=auth_user]").append('<option value="' + v.id + '" selected>' + v.username + '</option>')
                        } else {
                            $("select[name=auth_user]").append('<option value="' + v.id + '">' + v.username + '</option>')
                        }
                    }
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        },
        initHostsTree: function (data) {
            $("#authTree").jstree({
                "themes": { "stripes": true },
                "checkbox": {
                    "keep_selected_style": false,
                },
                "plugins": ["checkbox"],
                "core": {
                    'check_callback': true,
                    "data": data
                }
            })
            $(document).on("click", "#checkall", function () {
                $("#authTree").jstree($(this).prop("checked") ? "check_all" : "uncheck_all");
            });
            $(document).on("click", "#expandall", function () {
                $("#authTree").jstree($(this).prop("checked") ? "open_all" : "close_all");
            });
        },
        bindForm: function () {
            Form.api.bindevent($("form[role=form]"), null, null, function () {
                if ($("#authTree").size() > 0) {
                    var r = $("#authTree").jstree("get_all_checked");
                    var h = $('#authTree').jstree(true).get_selected(true);
                    if (h.length == 0 && r.business.length == 0) {
                        Toastr.error(L('You must select a host') + "！");
                        return false;
                    } else {
                        var hosts = [];
                        var business = [];
                        for (var i = 0; i < h.length; i++) {
                            var v = h[i];
                            if (v.parent == "#") {
                                business.push(v.id)
                            } else {
                                if (business.indexOf(v.parent) == -1) {
                                    hosts.push(v.text);
                                }
                            }
                        }
                        $("input[name='hosts']").val(hosts.join(','));
                        $("input[name='business']").val(r.business.join(','));
                        return true;
                    }
                }
            });
        }
    }
};