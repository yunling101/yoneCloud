var Controller = {
    index: function () {
        Fast.api.ajax({"url": "monitor/config", "dataType":"json"}, function(data) {
            if (data.code) {
               Fast.api.render("alarm/monitorLine", function(html){
                $("#myTabContent").append(ejs.render(html, {
                    v: data.msg
                }));
            });
            }else{
               Toastr.error(data.msg);
               return false;
            }

            Form.api.bindevent($('[role="consul-form"]'));
            Form.api.bindevent($('[role="prometheus-form"]'));
            Form.api.bindevent($('[role="alertmanager-form"]'));
            Form.api.bindevent($('[role="grafana-form"]'));
        });
    },
    api: {
        firstLetter: function(str) {
            if (!str) return str;
            return str.charAt(0).toUpperCase() + str.slice(1);
        }
    }
}