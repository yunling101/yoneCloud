var Controller = {
   index: function () {
      Controller.weekDate();
      week = {
         "0": "Sunday",
         "1": "Monday",
         "2": "Tuesday",
         "3": "Wednesday",
         "4": "Thursday",
         "5": "Friday",
         "6": "Saturday"
      }
      $("#wlc-info").html(moment(new Date()).format(L('YYYY-MM-DD')) + " " + L(week[moment().format('d')]) + "，" + L('Welcome back to the console') + "。")

      Fast.api.ajax({ "url": "/index/stat/", "dataType": "json" }, function (data) {
         if (data.code) {
            $("#indexUser").text(data.msg.user);
            $("#indexHosts").text(data.msg.hosts);
            $("#indexBusiness").text(data.msg.business);
            $("#indexCluster").text(data.msg.cluster);
            $("#auth_type").html('<span class="label label-info">' + L(data.msg.auth_type) + '</span>');
            $("#auth_version").html(data.msg.auth_version);
            $("#monthDate").text(L('Last updated') + " " + data.msg.time);
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

      $("#check-update").on("click", function () {
         Fast.api.ajax({ "url": "/index/check/update/", "method": "POST", "dataType": "json" }, function (data) {
            if (data.code) {
               Toastr.success(data.msg);
               return true;
            } else {
               Toastr.error(data.msg);
               return false;
            }
         });
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