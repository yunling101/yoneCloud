var Fast = {
    config: {
        // toastr默认配置
        toastr: {
            "closeButton": true,
            "debug": false,
            "newestOnTop": false,
            "progressBar": false,
            "positionClass": "toast-top-right",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        }
    },
    api: {
        ajax: function (options, success, error) {
            options = $.extend({
                success: success,
                error: function (xhr) {
                    var ret = {
                        code: xhr.status,
                        msg: xhr.statusText,
                        data: null
                    };
                    Toastr.error(ret.msg)
                    return false;
                }
            }, options);

            return $.ajax(options);
        },
        //修复URL
        fixurl: function (url) {
            return url;
        },
        //查询Url参数
        query: function (name, url) {
            if (!url) {
                url = window.location.href;
            }
            name = name.replace(/[\[\]]/g, "\\$&");
            var regex = new RegExp("[?&/]" + name + "([=/]([^&#/?]*)|&|#|$)"),
                results = regex.exec(url);
            if (!results)
                return null;
            if (!results[2])
                return '';
            return decodeURIComponent(results[2].replace(/\+/g, " "));
        },
        render: function (url, callback) {
            try {
                if (url.substr(0, 1) === "/") {
                    var path = url.substr(1);
                } else {
                    var path = url;
                }
                callback(Templates[path]())
            } catch (e) {
                console.log(e)
                Toastr.error("模板不存在！")
                return false;
            }
        },
        //打开一个弹出窗口
        open: function (url, title, options) {
            Fast.api.render(url, function (html) {
                if (options.html != "" && options.html != undefined) {
                    html = L(html, options.html)
                }
                title = options && options.title ? options.title : (title ? title : "");
                var area = Fast.config.openArea != undefined ? Fast.config.openArea : [$(window).width() > 800 ? '800px' : '95%', $(window).height() > 600 ? '600px' : '95%'];
                options = $.extend({
                    type: 1,
                    title: title,
                    //shadeClose: true,
                    //shade: false,
                    maxmin: true,
                    moveOut: true,
                    area: area,
                    offset: "60px",
                    content: html,
                    zIndex: Layer.zIndex,
                    success: function (layero, index) {
                        Layer.setTop(layero);
                        if ($(layero).height() > $(window).height()) {
                            //当弹出窗口大于浏览器可视高度时,重定位
                            Layer.style(index, {
                                top: 0,
                                height: $(window).height()
                            });
                        }
                    }
                }, options ? options : {});
                if ($(window).width() < 480 || (/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream && top.$(".navbar-header").size() > 0)) {
                    options.area = [top.$(".navbar-header").width() + "px", "100%"];
                    options.offset = [top.$(".navbar-header").height() + "px", "0px"];
                }

                layer.open(options);
                if (options.callback && typeof options.callback === 'function') {
                    options.callback();
                }

                if (options.form) {
                    return Form.api.bindevent($("form[role=form]"));
                }
            });
        },
        serializeObject: function (a) {
            var o = {};
            $.each(a, function () {
                if (o[this.name] !== undefined) {
                    if (!o[this.name].push) {
                        o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';
                }
            });
            return o;
        },
        gettablecolumnbutton: function (options) {
            if (typeof options.tableId !== 'undefined' && typeof options.fieldIndex !== 'undefined' && typeof options.buttonIndex !== 'undefined') {
                var tableOptions = $("#" + options.tableId).bootstrapTable('getOptions');
                if (tableOptions) {
                    var columnObj = null;
                    $.each(tableOptions.columns, function (i, columns) {
                        $.each(columns, function (j, column) {
                            if (typeof column.fieldIndex !== 'undefined' && column.fieldIndex === options.fieldIndex) {
                                columnObj = column;
                                return false;
                            }
                        });
                        if (columnObj) {
                            return false;
                        }
                    });
                    if (columnObj) {
                        return columnObj['buttons'][options.buttonIndex];
                    }
                }
            }
            return null;
        }
    },
    correctRouter: function (e) {
        return /^\//.test(e) || (e = "/" + e),
            e.replace(/^(\/+)/, "/").replace(new RegExp("/" + 'index' + "$"), "/")
    },
    router: function (r) {
        var e = location.hash;
        var o = {
            path: [],
            search: {},
            param: r || {},
            hash: (e.match(/[^#](#.*$)/) || [])[1] || ""
        }
        if (/^#\//.test(e)) {
            e = e.replace(/^#\//, "")
            o.href = "/" + e;
        }

        if (o.href == "/" || o.href == "" || o.href == undefined) {
            o.path = "/";
            o.href = "/home";
        } else {
            o.path = e.replace(/([^#])(#.*$)/, "$1").split("/") || []
        }

        return o;
    },
    headCrumb: function (app, s) {
        var line = '<h2>' + s + '</h2>';
        line += '<ol class="breadcrumb">';
        if (app != "dashboard") {
            line += '<li class="breadcrumb-item">';
            line += '<a href="/">仪表盘</a>';
            line += '</li>';
            line += '<li class="breadcrumb-item">';
            line += '<a>' + s + '</a>';
            line += '</li>';
        }
        line += '</ol>';
        $("#headCrumb").html(line);
    },
    setNavbar: function (path) {
        if (path == "" || path == undefined || path == "/") {
            var app = "dashboard";
        } else {
            if (path.length == 1) {
                var app = path[0];
            } else {
                for (var i = 1; i < path.length; i++) {
                    var l = path[i];
                    path[i] = path[i].toString()[0].toUpperCase() + path[i].toString().slice(1);;
                }
                var app = path.join("");
            }
        }
        Fast.headCrumb(app, $("#" + app).children("a").text());
        $(".navbar-default .nav li").removeClass("active");
        if ($(".navbar-default .nav #" + app).parent().hasClass("nav-third-level")) {
            $(".navbar-default .nav #" + app).addClass("active").parent().addClass("in").parent().addClass("active").parent().addClass("in").parent().addClass("active");
        } else {
            $(".navbar-default .nav #" + app).addClass("active").parent().addClass("in").parent().addClass("active");
        }
    },
    view: function () {
        var r = Fast.router();

        Fast.setNavbar(r.path);
        if (r.path.length != 0) {
            Fast.api.render(r.href, function (e) {
                $(".wrapper-content").html(e);
                jQuery.getScript(Config.model + r.href + ".js").done(function () {
                    Controller.index();
                });
            });
        }
    },
    lang_ajax: function () {
        var result = "";
        Fast.api.ajax({ type: "GET", url: Config.lang, dataType: "json", async: false }, function (d) {
            result = d;
        });
        return result;
    },
    get_base_domain: function () {
        var url = window.location.href;
        var hostname = url.split('/')[2];
        hostname = hostname.split(':')[0];

        var isIP = hostname.match(/^\d{1,3}(\.\d{1,3}){3}$/);
        if (isIP) {
            return hostname; // 如果是 IP 地址，直接返回
        }

        var parts = hostname.split('.');
        if (parts.length > 2) {
            return '.' + parts.slice(-2).join('.');
        }
        return '.' + hostname;
    },
    oAuth: function () {
        Fast.api.ajax({ url: Config.oauth, type: "GET", dataType: "json" }, function (d) {
            if (d.code) {
                // var domain = location.hostname.split(".").slice(-2).join(".");
                document.cookie = "oauth_grafana=" + d.msg.oauth_state + "; path=/; domain=" + Fast.get_base_domain();
                return true;
            } else {
                // console.log(d);
                return false;
            }
        });
    },
    query_permission: function () {
        var permission = "";
        Fast.api.ajax({ url: Config.permission, type: "GET", dataType: "json", async: false }, function (d) {
            permission = d
        })
        return permission;
    },
    permission: function (path) {
        if (Permission.super) {
            return true;
        } else {
            if (Permission.data.indexOf(path) === -1) {
                return false;
            } else {
                return true;
            }
        }
    },
    lang: function (Lang) {
        return function () {
            var args = arguments,
                string = args[0],
                i = 1;
            string = string.toLowerCase();
            if (typeof Lang !== 'undefined' && typeof Lang[string] !== 'undefined') {
                if (typeof Lang[string] == 'object')
                    return Lang[string];
                string = Lang[string];
            } else if (string.indexOf('.') !== -1 && false) {
                var arr = string.split('.');
                var current = Lang[arr[0]];
                for (var i = 1; i < arr.length; i++) {
                    current = typeof current[arr[i]] != 'undefined' ? current[arr[i]] : '';
                    if (typeof current != 'object')
                        break;
                }
                if (typeof current == 'object')
                    return current;
                string = current;
            } else {
                string = args[0];
            }
            return string.replace(/%((%)|s|d)/g, function (m) {
                // m is the matched format, e.g. %s, %d
                var val = null;
                if (m[2]) {
                    val = m[2];
                } else {
                    val = args[i];
                    // A switch statement so that the formatter can be extended. Default is %s
                    switch (m) {
                        case '%d':
                            val = parseFloat(val);
                            if (isNaN(val)) {
                                val = 0;
                            }
                            break;
                    }
                    i++;
                }
                return val;
            });
        }
    },
    init: function () {
        // 获取监控权限
        Fast.oAuth()

        // Layer配置
        layer.config({
            skin: 'layui-layer-fast'
        });

        //配置Toastr的参数
        toastr.options = Fast.config.toastr;

        //添加ios-fix兼容iOS下的iframe
        if (/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream) {
            $("html").addClass("ios-fix");
        }

        //点击包含.btn-dialog的元素时弹出dialog
        $(document).on('click', '.btn-dialog', function (e) {
            var that = this;
            var options = $.extend({}, $(that).data() || {});
            var url = $(that).data("url") || $(that).attr('href');
            var title = $(that).attr("title") || $(that).data("title") || $(that).data('original-title');

            var button = Fast.api.gettablecolumnbutton(options);
            if (typeof options.confirm !== 'undefined') {
                Layer.confirm(options.confirm, function (index) {
                    Fast.api.open(button.url, title, options);
                    Layer.close(index);
                });
            } else {
                window[$(that).data("window") || 'self'].Fast.api.open(button.url, title, options);
            }

            if (button && typeof button.callback === 'function') {
                options.callback = button.callback(url);
            }
            return false;
        });
    }
}

//将Layer暴露到全局中去
window.Layer = layer;
//将Toastr暴露到全局中去
window.Toastr = toastr;
//将语言方法暴露到全局中去
window.L = Fast.lang(Fast.lang_ajax());
//全局权限
window.Permission = Fast.query_permission();

//将Fast渲染至全局
window.Fast = Fast;
//默认初始化执行的代码
Fast.init();
