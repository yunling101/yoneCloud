/*jslint browser:true */

var jQuery;
var geometry = {};

jQuery(function ($) {
    Terminal.applyAddon(fullscreen);
    Terminal.applyAddon(fit);
    Terminal.applyAddon(attach);

    function make_terminal(element, sid) {
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_url = ws_scheme + '://' + window.location.host + '/ws/ssh/';

        var term = new Terminal({
            fontFamily: 'monaco, Consolas, "Lucida Console", monospace',
            screenKeys: true,
            useStyle: true,
            rightClickSelectsWord: false,
            allowProposedApi: true,
            cursorBlink: true,
            cursorStyle: 'block',
            theme: { background: "#2d2e2c" },
            wordSeparator: '() []{}\',"`;:'
        });

        term.open(element, false);
        term.toggleFullScreen(true);
        term.write("Connection begin...\r\n");
        try {
            term.fit();
        } catch (e) { }

        function resize_terminal() {
            var cols = Math.floor(element.clientWidth / 9.1);
            var rows = Math.floor(element.clientHeight / 21);

            term.resize(cols, rows); // 调整终端大小
            term.scrollToBottom(); // 确保光标在底部
        }

        window.addEventListener('resize', resize_terminal);
        resize_terminal();

        var ws = new WebSocket(ws_url);
        ws.onopen = function (event) {
            term.focus();
            var cols = Math.floor(element.clientWidth / 9.1);
            var rows = Math.floor(element.clientHeight / 21);
            var data = { sid: sid, width: cols, height: rows };
            ws.send(JSON.stringify({ "tp": "init", "data": data }))

            term.attach(ws);
            term._initialized = true;
        };

        ws.onclose = function (e) {
            // term.destroy();
            term.write('\r\nConnection is closed.\r\n');
        };

        ws.onerror = function (e) {
            term.write("Connection Error.");
        }

        term.onResize(function (v) {
            ws.send(JSON.stringify({ "tp": "set_size", "width": v.cols, "height": v.rows }))
        });

        term.on('close', function () {
            if (ws) {
                ws.close(); // 关闭 WebSocket 连接
            }
        });

        return { socket: ws, term: term };
    }

    $(document).ready(function () {
        make_terminal(document.getElementById("terminal"), $("#terminal").attr("sid"));
    })

    $(window).bind('beforeunload', function () {
        return '您可能还有数据没有保存';
    });
});