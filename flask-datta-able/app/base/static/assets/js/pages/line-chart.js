'use strict';
$(document).ready(function() {
    var current = new Date();
    var request_rate = [{ time: current.getTime(), value: 0 }];
    var response_time = [{ time: current.getTime(), value: 0 }];
    var server_scale = [{ time: current.getTime(), value: 0 }];


    var request_chart = Morris.Line({
        element: 'request-chart',
        data: request_rate,
        lineColors: ['#ef4f4f'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Request/Second'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });

    var response_chart = Morris.Line({
        element: 'response-chart',
        data: response_time,
        lineColors: ['#ee9595'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Response Time'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });

    var scale_chart = Morris.Line({
        element: 'scale-chart',
        data: server_scale,
        lineColors: ['#ffcda3'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Server Scale'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });


    setInterval(function() {
        $.ajax({
            type: "POST",
            url: "/index/update/metadata",
            dataType: "json",
            success: function(data) {
                //document.getElementById("remain_time").value = parseFloat(data.remain_time).toFixed(2);

                current = new Date();
                if (request_rate.length == 16) {
                    request_rate.shift();
                    response_time.shift();
                    server_scale.shift();
                }


                request_rate.push({ time: current.getTime(), value: data.request_rate });
                if (data.force_val != -1){
                    request_chart.setData(request_rate);
                }
                
                response_time.push({ time: current.getTime(), value: data.response_time});
                if (data.velocity_val != -1){
                    response_chart.setData(response_time);
                }
                
                server_scale.push({ time: current.getTime(), value: data.server_scale });
                
                if (data.server_scale != -1){
                    scale_chart.setData(server_scale);
                }
            }
        });
    }, 100);

    $("#interrupt").click(function(e) {
        $.ajax({
            type: "POST",
            url: "/index/interrupt",
            dataType: "json",
            success: function(data) {
                window.alert(data.msg);
            }
        });
    });
});
