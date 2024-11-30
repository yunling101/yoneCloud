$.jstree.core.prototype.get_all_checked = function (full) {
    var obj = {
        "menu": [],
        "permission": []
    }
    $('[aria-selected="true"][aria-level="1"]').each(function(){
       obj.menu.push($(this).children("a").text())
    });
    $('[aria-selected="true"][aria-level="2"]').each(function(){
       if ($(this).parent().parent().attr("aria-selected") == "false") {
            var ii = $(this).parent().prev("a").text();
            var gg = $(this).children("a").text();
            obj.permission.push(ii + "|" + gg);
       }
    });

    return obj;
};
var Controller = {
    initAuthTree: function(content){
        // 初始化树
        $("#authTree").jstree({
            "themes": {"stripes": true},
            "checkbox": {
                "keep_selected_style": false,
            },
            "plugins": ["checkbox"],
            "core": {
                'check_callback': true,
                "data": content
            }
        });

        $(document).on("click", "#checkall", function () {
            $("#authTree").jstree($(this).prop("checked") ? "check_all" : "uncheck_all");
        });
        $(document).on("click", "#expandall", function () {
            $("#authTree").jstree($(this).prop("checked") ? "open_all" : "close_all");
        });
    },
    index: function () {
        // 初始化表格参数配置
        Table.api.init({
            extend: {
                "index_url": "user/role",
                "add_url": "user/role/add",
                "edit_url": "user/role/add",
                "del_url": "user/role/delete/",
                "multi_url": "",
                "form": true
            },
            callback: {
                add: function() {
                   return function(){
                          $("#authTree").jstree("destroy");
                          Fast.api.ajax({"url": "/user/role/perm", "dataType":"json"}, function(data) {
                              if (data.code){
                                  var result = new Array();
                                  for (var x=0;x<data.rows.length; x++) {
                                       var v = data.rows[x];
                                       var child_item = {text: v.menu, children: []};
                                       for (var i=0;i<v.child.length; i++){
                                           var k = v.child[i];
                                           child_item["children"].push({text:k.menu})
                                       }
                                       result.push(child_item)
                                  }

                                  Controller.initAuthTree(result);
                                  Controller.api.bindevent();
                              }
                          });
                   }
                },
                edit: function(rows) {
                   return function() {
                      for(var k in rows){
                          var node = $("input[name='"+ k +"']");
                          if (node.length == 1){
                              node.val(rows[k]);
                          }
                      }
                      $("#comment").val(rows.comment);

                      $("#authTree").jstree("destroy");
                      Fast.api.ajax({"url": "/user/role/perm", "dataType":"json"}, function(data) {
                          if (data.code){
                              var result = new Array();
                              for (var x=0;x<data.rows.length; x++) {
                                   var v = data.rows[x];
                                   var child_item = {text: v.menu, children: []};
                                   if (rows.permission.indexOf(v.id) != -1) {
                                        child_item["state"] = {"selected": true}
                                   }
                                   for (var i=0;i<v.child.length; i++){
                                       var k = v.child[i];
                                       nLine = {text:k.menu}
                                       if (rows.permission.indexOf(k.id) != -1) {
                                            nLine["state"] = {"selected": true}
                                       }
                                       child_item["children"].push(nLine)
                                   }
                                   result.push(child_item)
                              }

                              Controller.initAuthTree(result);
                              Controller.api.bindevent();
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
                    {field: 'state', checkbox: true,},
                    {field: 'id', title: 'ID'},
                    {field: 'name', title: L('Name'), align: 'left'},
                    {field: 'comment', title: L('comment'), align: 'left'},
                    {
                        field: 'operate',
                        title: L('Operate'),
                        table: table,
                        events: Table.api.events.operate,
                        formatter: Table.api.formatter.operate
                    }
                ]
            ],
            pagination: false
        });

        // 为表格绑定事件
        Table.api.bindevent(table);
    },
    api: {
        bindevent: function () {
           Form.api.bindevent($("form[role=form]"), null, null, function () {
                if ($("#authTree").size() > 0) {
                    var r = $("#authTree").jstree("get_all_checked");
                    if (r.menu.length ==0){
                         Toastr.error("权限选择不能为空！");
                         return false;
                    }else{
                        $("input[name='menu']").val(r.menu.join(','));
                    }
                    if (r.permission.length != 0){
                        $("input[name='permission']").val(r.permission.join(','));
                    }
                }
                return true;
           });
        }
    }
};