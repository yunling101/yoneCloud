var Controller = {
    config: {
        "add": "add_hosts",
        "del": "delete_hosts",
        "provider": [],
        "business": []
    },
    index: function () {
        // 初始化表格参数配置
        if (!Fast.permission(Controller.config.add)) {
            $("#toolbar .btn-add").remove();
            $("#toolbar .btn-import").remove();
        }
        if (!Fast.permission(Controller.config.del)) {
            $("#toolbar .btn-del").remove();
        }
        Controller.get_business();
        Controller.get_provider();

        Table.api.init({
            extend: {
                "index_url": "api/v1/hosts/lists",
                "add_url": Fast.permission(Controller.config.add) ? "resources/hosts/add" : "",
                "edit_url": Fast.permission(Controller.config.add) ? "resources/hosts/add" : "",
                "del_url": Fast.permission(Controller.config.del) ? "resources/hosts/delete/" : "",
                "multi_url": "resources/hosts/monitor/",
                "form": true
            },
            callback: {
                html: function (rows) {
                    //                    var certificate = "";
                    //                    Fast.api.ajax({"url": "/resources/certificate/lists/", "dataType":"json", "async": false}, function(data) {
                    //                       if (data.code){
                    //                          for(var i=0; i<data.rows.length; i++){
                    //                              var v = data.rows[i];
                    //                              if (rows != undefined && rows.certificate.indexOf(v.id) != -1) {
                    //                                  certificate += '<option value="'+v.id+'" selected>'+v.name+'</option>';
                    //                              }else{
                    //                                  certificate += '<option value="'+v.id+'">'+v.name+'</option>';
                    //                              }
                    //                          }
                    //                       }else{
                    //                          Toastr.error(data.msg);
                    //                          return false;
                    //                       }
                    //                    });
                    //                    return certificate;
                },
                add: function () {
                    return function () {
                        Controller.api.change();
                        Controller.api.provider();
                        Controller.api.change_certificate();
                    }
                },
                edit: function (rows) {
                    return function () {
                        if (rows.business != "" && rows.business != null && rows.business.length == 1) {
                            var pid = rows.business[0];
                        }
                        Controller.api.change(pid);
                        if (rows.certificate != "" && rows.certificate != null && rows.certificate.length == 1) {
                            var cid = rows.certificate[0];
                        }
                        Controller.api.change_certificate(cid);
                        Controller.api.provider();

                        if (rows.status != "" && rows.status != null && typeof rows.status === "object") {
                            if (rows.status.status != "unknown") {
                                $("select[name=status]").find("option[value=1]").attr("selected", true);
                            }
                        }

                        if (rows.proxy) {
                            $("#proxy").find("option[value=1]").attr("selected", true);
                        }
                        if (rows.provider) {
                            $("#provider").find("option[value=" + rows.provider + "]").attr("selected", true);
                        }

                        for (var k in rows) {
                            var node = $("form[role=form] input[name='" + k + "']");
                            if (node.length == 1) {
                                node.val(rows[k]);
                            }
                        }
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
                    { field: 'sid', title: 'ID', formatter: Controller.api.formatter.id },
                    // {field: 'instance_id', title: L('Instance id'), align: 'left'},
                    { field: 'hostname', title: L('Hostname'), align: 'left' },
                    { field: 'ip', title: L('Address'), align: 'left' },
                    // {field: 'business', title: L('Business'), searchList: Controller.config.business},
                    { field: 'provider', title: L('Provider'), searchList: Controller.config.provider },
                    { field: 'monitor', title: L('Monitor'), formatter: Controller.api.formatter.monitor, searchList: [L('Open'), L('Close')] },
                    // {field: 'agent_version', title: L('Agent version')},
                    { field: 'status', title: L('Status'), formatter: Controller.api.formatter.status, searchList: [L('Normal'), L('Abnormal'), L('Unkown')] },
                    { field: 'create_time', title: L('Create time'), sortable: true, operate: 'RANGE', addclass: 'datetimerange', formatter: Table.api.formatter.datetime },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        buttons: [{
                            name: 'detail',
                            text: L('Detail'),
                            icon: 'fa fa-list',
                            classname: 'btn btn-info btn-xs btn-detail btn-dialog',
                            callback: Controller.api.detail,
                            url: 'resources/hosts/detail'
                        }],
                        formatter: Table.api.formatter.operate
                    }
                ]
            ],
            commonSearch: true
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        formatter: {
            id: function (value, row, index) {
                if (row.monitor && row.ml) {
                    var m = '<a target="_blank" href="' + row.ml + '" style="padding-left:8px;"><i class="fa fa-bar-chart-o"></i></a>';
                } else {
                    var m = '<a style="padding-left:8px;color:#abacad;pointer-events:none;"><i class="fa fa-bar-chart-o"></i></a>';
                }
                if (row.console) {
                    var c = '<a target="_blank" href="/ssh/' + row.sid + '/?hostname=' + row.hostname + '" style="padding-left:8px;"><i class="fa fa-desktop fa-fw"></i></a>';
                } else {
                    var c = '<a style="padding-left:8px;color:#abacad;pointer-events:none;"><i class="fa fa-desktop fa-fw"></i></a>';
                }
                return value + c + m;
            },
            monitor: function (value, row, index) {
                var m = '<span class="text-danger">Disabled</span>';
                if (value) {
                    m = '<span class="text-success">Enabled</span>';
                }
                return '<a href="javascript:;" class="btn-change" data-id="' + row.id + '">' + m + '</a>';
            },
            status: function (value, row, index) {
                var status = L('Normal');
                return '<span class="text-success" title="' + L('Status') + ': ' + status + '"><i class="fa fa-circle"></i></span> ';
            }
        },
        detail: function (url) {
            Fast.api.ajax({ "url": url, "dataType": "json" }, function (data) {
                if (data.code) {
                    var tr = "";
                    for (var k in data.msg) {
                        if (k != "id") {
                            if (data.msg[k] != null && data.msg[k] != "") {
                                tr += "<tr><td>" + L(k.replace("_", " ")) + "</td><td>" + data.msg[k] + "</td></tr>";
                            }
                        }
                    }
                    $("#detailBody").html(tr);
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        },
        change: function (pid) {
            Fast.api.ajax({ "url": "/business/item/", "dataType": "json" }, function (data) {
                if (data.code) {
                    for (var i = 0; i < data.rows.length; i++) {
                        var v = data.rows[i];
                        if (pid == v.id) {
                            $("select[name=business]").append('<option value="' + v.id + '" selected>' + v.name + '</option>');
                        } else {
                            $("select[name=business]").append('<option value="' + v.id + '">' + v.name + '</option>');
                        }
                    }
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        },
        change_certificate: function (pid) {
            $("select[name=certificate]").append('<option value="">' + L('Choose') + L('Certificate') + '</option>');
            Fast.api.ajax({ "url": "/auth/certificate/lists/", "dataType": "json", "async": false }, function (data) {
                if (data.code) {
                    for (var i = 0; i < data.rows.length; i++) {
                        var v = data.rows[i];
                        if (pid == v.id) {
                            $("select[name=certificate]").append('<option value="' + v.id + '" selected>' + v.name + '</option>');
                        } else {
                            $("select[name=certificate]").append('<option value="' + v.id + '">' + v.name + '</option>');
                        }
                    }
                } else {
                    Toastr.error(data.msg);
                    return false;
                }
            });
        },
        provider: function (provider) {
            for (var i = 0; i < Controller.config.provider.length; i++) {
                var k = Controller.config.provider[i];
                if (provider == k) {
                    var h = '<option value="' + k + '" selected>' + k + '</option>';
                } else {
                    var h = '<option value="' + k + '">' + k + '</option>';
                }
                $("select[name=provider]").append(h)
            }
        }
    },
    get_business: function () {
        Fast.api.ajax({ "url": "/business/item/", "dataType": "json", "async": false }, function (data) {
            if (data.code) {
                for (var i = 0; i < data.rows.length; i++) {
                    var v = data.rows[i];
                    Controller.config.business.push(v.name);
                }
            } else {
                Toastr.error(data.msg);
                return false;
            }
        });
    },
    get_provider: function () {
        Fast.api.ajax({ "url": "/resources/provider/", "dataType": "json", "async": false }, function (data) {
            if (data.code) {
                if (data.data != null) {
                    for (var k in data.data) {
                        Controller.config.provider.push(k);
                    }
                }
            } else {
                Toastr.error(data.msg);
                return false;
            }
        });
    }
};