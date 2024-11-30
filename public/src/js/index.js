// 初始化
$(function () {
    Fast.view();
    window.onhashchange = function() {
        Fast.view();
    }

    $("body").on("click", "*[hunt-href]", function() {
        var e = $(this);
        var t = e.attr("hunt-href");

        location.hash = Fast.correctRouter(t);
    });
});