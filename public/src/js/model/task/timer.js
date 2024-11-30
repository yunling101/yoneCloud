$.jstree.core.prototype.get_all_checked = function (full) {
    var obj = {
        "business": [],
        "hosts": []
    }
    $('[aria-selected="true"][aria-level="1"]').each(function () {
        obj.business.push($(this).children("a").text())
    });
    $('[aria-selected="true"][aria-level="2"]').each(function () {
        if ($(this).parent().parent().attr("aria-selected") == "false") {
            var ii = $(this).parent().prev("a").text();
            var gg = $(this).children("a").text();
            obj.hosts.push(gg);
        }
    });

    return obj;
};
var Controller = {
    config: {
        "add": "add_task_timer",
        "del": "delete_task_timer"
    },
    index: function () {
        // 初始化表格参数配置
        // jQuery.getScript("/public/static/js/codemirror/codemirror.js");
        // jQuery.getScript("/public/static/js/codemirror/mode/shell.js");
        // $("<link>", {rel: 'stylesheet',type: 'text/css',href: '/public/static/js/codemirror/codemirror.css'}).appendTo('head');

        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
        }

        Table.api.init({
            extend: {
                "index_url": "api/v1/task/timer/lists",
                "add_url": Fast.permission(Controller.config.add) ? "task/timer/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "task/timer/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "task/timer/delete/" : "",
                "multi_url": "",
                "form": false
            },
            callback: {
                add: function () {
                    return function () {
                        //    Controller.api.initScriptText("");

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
                        $("textarea[name=scripts]").val(rows.scripts);
                        $("textarea[name=description]").val(rows.description);
                        $("#timer_type").find("option[value=" + rows.timer_type + "]").attr("selected", true);
                        for (var k in rows) {
                            var node = $("input[name='" + k + "']");
                            if (node.length == 1) {
                                node.val(rows[k]);
                            }
                        }

                        //   Controller.api.initScriptText(rows.scripts);
                        $("#authTree").jstree("destroy");
                        Fast.api.ajax({ "url": "/resources/hosts/batch/", "dataType": "json" }, function (data) {
                            if (data.code) {
                                var result = new Array();
                                for (var business in data.results) {
                                    var child_business = { text: business, children: [] };
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
                    { field: 'state', checkbox: true },
                    { field: 'id', title: 'ID' },
                    { field: 'name', title: L('Name'), align: 'left' },
                    { field: 'uuid', title: L('UUID'), align: 'left' },
                    // {field: 'username', title: L('Username')},
                    { field: 'timer_type', title: L('Timer type'), formatter: Controller.api.formatter.timerType },
                    { field: 'status', title: L('Status'), formatter: Controller.api.formatter.status },
                    { field: 'results', title: "执行" + L('Status'), formatter: Controller.api.formatter.results },
                    { field: 'execution_time', title: L('Timer time') },
                    { field: 'create_time', title: L('Create time'), formatter: Table.api.formatter.datetime },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        buttons: [{
                            name: 'detail',
                            text: "执行结果",
                            icon: '',
                            classname: 'btn btn-info btn-xs btn-detail btn-dialog',
                            callback: Controller.api.detail,
                            url: 'task/timer/detail'
                        }],
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
            timerType: function (value) {
                if (value == "once") {
                    return "一次性"
                }
                return "周期性"
            },
            status: function (value) {
                if (value == 0) {
                    return '<span class="label label-warning">停止</span>'
                }
                return '<span class="label label-info">正常</span>'
            },
            results: function (value) {
                if (value == 0) {
                    return "<span class='text-muted'>未执行</span>"
                }
                return "<span class='text-success'>已执行</span>"
            }
        },
        initScriptText: function (data) {
            var textArea = document.getElementById("scripts");
            var editor = CodeMirror.fromTextArea(textArea, {
                mode: "shell",
                lineNumbers: true,  //显示行号
                //    lineWrapping: false, //代码折叠
                //    foldGutter: true,
                //    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
                //                matchBrackets: true, //括号匹配
                autoRefresh: true
            });
            // editor.setValue(data)
            editor.refresh();
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
                    if (r.hosts.length == 0 && r.business.length == 0) {
                        Toastr.error("必须选择主机！");
                        return false;
                    } else {
                        $("input[name='hosts']").val(r.hosts.join(','));
                        $("input[name='business']").val(r.business.join(','));
                        return true;
                    }
                }
            });
        },
        detail: function (url) {
            Fast.api.ajax({ "url": url, "dataType": "json" }, function (data) {
                if (data.code) {
                    var tr = "";
                    for (var k in data.msg) {
                        if (k != "id") {
                            if (data.msg[k] != null && data.msg[k] != "") {
                                if (k == "hosts") {
                                    // var hosts = "";
                                    // var results_hosts = data.msg[k].split(",");
                                    // for (var i=0;i<results_hosts.length; i++){
                                    //     hosts += results_hosts[i] + "\n";
                                    // }
                                    // tr += "<tr><td>执行主机</td><td>"+ hosts +"</td></tr>";    
                                } else if (k == "results") {
                                    tr += "<tr><td>" + L(k.replace("_", " ")) + "</td><td><pre style=\"max-height: 200px;overflow-y: auto\">" + data.msg[k] + "</pre></td></tr>";
                                } else if (k == "frequency") {
                                    tr += "<tr><td>执行" + L(k.replace("_", " ")) + "</td><td>" + data.msg[k] + " 次</td></tr>";
                                } else {
                                    tr += "<tr><td>" + L(k.replace("_", " ")) + "</td><td>" + data.msg[k] + "</td></tr>";
                                }
                            }
                        }
                    }
                    $("#detailBody").html(tr);
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        }
    }
};