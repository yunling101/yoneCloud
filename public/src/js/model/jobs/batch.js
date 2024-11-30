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
            var v = $(this).children("a").text();
            obj.hosts.push(v);
        }
    });

    return obj;
};

var Controller = {
    index: function () {
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
            } else {
                Toastr.error(data.msg);
                return false;
            }
        });

        var term = new Terminal({
            fontSize: 13,
            cols: 110,
            rows: 39,
            theme: {
                background: "#222d32"
            }
        });
        term.open(document.getElementById("tabContent"));
        term.write("\r\n请输入要批量执行的命令!")

        $(document).on("click", "button[name=submit]", function () {
            var user = $("#ssh_user").val();
            var command = $("textarea[name=command]").val();
            if (command.length == 0) {
                Toastr.warning("命令不能为空!");
                return false;
            }
            var r = $("#assetTree").jstree("get_all_checked");
            if (r.hosts.length == 0 && r.business.length == 0) {
                Toastr.warning("请至少选择1台主机!");
                return false;
            }

            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_url = ws_scheme + '://' + window.location.host + '/ws/batch/';
            var ws = new WebSocket(ws_url);
            ws.onopen = function (event) {
                ws.send(JSON.stringify({
                    "tp": "init", "data": {
                        "username": user,
                        "command": command,
                        "hosts": r.hosts,
                        "business": r.business
                    }
                }))
            }
            ws.onmessage = function (event) {
                term.write("\r\n" + event.data)
                ws.send(JSON.stringify({ "tp": "close" }));
            }
            ws.onclose = function (event) {
                if (r.hosts.length !== 0) {
                    term.write("\r\n\r\nHosts: " + r.hosts.length + " Time: " + new Date().getTime())
                } else if (r.business.length !== 0) {
                    term.write("\r\n\r\nBusiness: " + r.business.length + " Time: " + new Date().getTime())
                }
            }
        });

        $(document).on("click", "button[name=clear]", function () {
            term.reset();
            term.write("\r\n请输入要批量执行的命令!")
        });
    },
    api: {
        initHostsTree: function (data) {
            $("#assetTree").jstree({
                "themes": { "stripes": true },
                "checkbox": {
                    "keep_selected_style": false,
                },
                "plugins": ["checkbox"],
                "core": {
                    'check_callback': true,
                    "data": data
                }
            }).on("loaded.jstree", function (event, data) {
                $('#assetTree').jstree().open_all();
            });

            $(document).on("click", "#checkall", function () {
                $("#assetTree").jstree($(this).prop("checked") ? "check_all" : "uncheck_all");
            });
            $(document).on("click", "#expandall", function () {
                $("#assetTree").jstree($(this).prop("checked") ? "open_all" : "close_all");
            });
        }
    }
};