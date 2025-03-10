var Controller = {
    index: function () {
        Table.api.init({
            extend: {
                "index_url": "api/v1/audit/connect",
                "add_url": "",
                "edit_url": "",
                "del_url": "",
                "multi_url": "",
                "form": true
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
                    { field: 'log', title: L('UUID') },
                    { field: 'username', title: L('Username') },
                    { field: 'server', title: L('Address') },
                    { field: 'hostname', title: L('Hostname') },
                    { field: 'is_finished', title: L('Status'), formatter: Controller.api.formatter.finished },
                    { field: 'start_time', title: L('Start time'), formatter: Table.api.formatter.datetime },
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        buttons: [
                            {
                                name: 'command',
                                text: L('History') + L('Command'),
                                classname: 'btn btn-primary btn-xs btn-detail btn-dialog',
                                callback: Controller.api.detail.command,
                                url: 'audit/detail/command'
                            },
                            {
                                name: 'playback',
                                text: L('Playback'),
                                classname: 'btn btn-info btn-xs btn-detail btn-dialog',
                                callback: Controller.api.detail.connect,
                                url: 'audit/detail/playback'
                            }
                        ],
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
            finished: function (value, row, index) {
                if (value) {
                    var m = '<span class="text-danger">' + L('Offline') + '</span>';
                } else {
                    var m = '<span class="text-info">' + L('Online') + '</span>';
                }
                return m;
            }
        },
        detail: {
            command: function (url) {
                Fast.api.ajax({ "url": url, "dataType": "json" }, function (data) {
                    if (data.code) {
                        var body = '';
                        for (var i = 0; i < data.data.length; i++) {
                            var n = data.data[i];
                            body += '<p style="margin-left:20px;margin-bottom:0px;">' + n.datetime + '<span style="margin-left:50px;">' + n.command + '</span></p>';
                        }
                        if (body == '') {
                            $("#detailBody").html('<span style="margin-left:20px;">无历史命令.</span>');
                        } else {
                            $("#detailBody").html(body);
                        }
                    } else {
                        Toastr.error(data.msg);
                        return false;
                    }
                });
            },
            connect: function (url) {
                $("#detailBody").html("");
                Fast.api.ajax({ "url": url, "dataType": "json" }, function (data) {
                    if (data.code) {
                        var v = data.data;
                        var body = '<div style="margin-left: 29px;margin-bottom: 5px;">';
                        body += L('Username') + ': <span class="text-info">' + v.username + '</span>';
                        body += L('Server') + ': <span class="text-info">' + v.hosts + '</span>';
                        body += L('Start') + L('Time') + ': <span class="text-info">' + v.start_time + '</span></div>';
                        body += '<asciinema-player src="' + v.path + '"></asciinema-player>';
                        $("#detailBody").html(body);
                    } else {
                        Toastr.error(data.msg);
                        return false;
                    }
                });
            }
        }
    }
}