var Controller = {
   index: function () {
      Controller.weekDate();

      Fast.api.ajax({ "url": "/index/stat/", "dataType": "json" }, function (data) {
         if (data.code) {
            $("#indexHosts").text(data.msg.hosts);
            $("#indexBusiness").text(data.msg.business);
            $("#weekDate").text(" " + L('Last updated') + " " + data.msg.time);
         } else {
            Toastr.error(data.msg);
            return false;
         }
      });

      Fast.api.ajax({ "url": "/index/login/", "dataType": "json" }, function (data) {
         if (data.code) {
            for (var i = 0; i < data.msg.length; i++) {
               var v = data.msg[i];
               var li = '<li class="list-group-item">';
               li += '<p><a class="text-info" href="javascript:;">@' + v.username + '</a> session: ' + v.session_key + '</p>';
               li += '<small class="block text-muted"><i class="fa fa-clock-o"></i> ' + moment(new Date(v.date_added)).format('YYYY-MM-DD hh:mm:ss') + '</small>';
               li += '</li>';
               $("#loginRecord").append(li);
            }
         } else {
            Toastr.error(data.msg);
            return false;
         }
      });

      Fast.api.ajax({ "url": "/index/option/", "dataType": "json" }, function (data) {
         if (data.code) {
            for (var i = 0; i < data.msg.length; i++) {
               var v = data.msg[i];
               var div = '<div class="timeline-item">';
               div += '<div class="row">';
               div += '<div class="col-lg-3 date">';
               div += '<i class="fa fa-briefcase"></i>';
               div += moment(new Date(v.date_added)).format(L('YYYY-MM-DD'));
               div += '<br/>';
               div += '<small class="text-navy">' + moment(new Date(v.date_added)).format('hh:mm:ss') + '</small>';
               div += '</div>';
               div += '<div class="col-lg-7 content no-top-border">';
               div += '<p class="m-b-xs"><strong>' + v.username + '</strong></p>';
               div += '<p>' + v.object + '; <br/>【' + L('Operate') + ' IP】' + v.ip + '</p>';
               div += '</div>';
               div += '</div>';
               div += '</div>';
               $("#optionRecord").append(div);
            }
         } else {
            Toastr.error(data.msg);
            return false;
         }
      });
   },
   weekDate: function () {
      Fast.api.ajax({ "url": "/index/week/", "dataType": "json" }, function (data) {
         if (data.code) {
            var ctx = document.getElementById("lineChart").getContext("2d");
            new Chart(ctx, {
               type: 'line',
               data: data.msg,
               options: {
                  responsive: true
               }
            });
            $("#weekHosts").text(data.hosts);
            $("#weekBusiness").text(data.business);
            $("#weekHostsBar").css("width", data.hosts + "%");
            $("#weekBusinessBar").css("width", data.business + "%");
         } else {
            Toastr.error(data.msg);
            return false;
         }
      });
   }
};