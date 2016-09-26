function draw_chart(data) {
    // Glucose Average by Day chart
     var chartOptions = {
        chart: {
            renderTo: 'chart_panel',
            type: 'line'
        },
        legend: {enabled: true},
        title: {text: 'Custom Chart'},
        subtitle: {text: 'Last 14 Days'},
        xAxis: {title: {text: null}, labels: {rotation: -45}},
        yAxis: {title: {text: null}},
        series: [{}]
    };


    chartOptions.xAxis.categories = data["dates"];
    signal = data["signal"];
    chartOptions.series[0].name = get_legend(signal);
    chartOptions.series[0].data = data[signal];
    var chart = new Highcharts.Chart(chartOptions);
}


function get_legend(signal) {
    if(signal == 'temperature'){
        legend = 'Avg Temperature (ºC)';
    }else if(signal == 'rainfall'){
        legend = 'Total Rainfall (mm)';
    }
    return legend;
}


// Submit post on submit
$('#post-chart').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    create_chart();
});


// AJAX for posting
function create_chart() {
    console.log("create chart is working!"); // sanity check
    $.ajax({
        url : "", // the endpoint
        type : "GET", // http method
        data : { sensor : $('#sensor').val(), signal: $('#signal').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            draw_chart(json["chart_data"]);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}