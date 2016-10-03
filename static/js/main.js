function draw_chart(data) {
    // Signals chart
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


// Submit chart on submit
$('#form-chart').on('submit', function(event){
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
        data : { sensor : $('#sensor').val(), signal: $('#signal').val() },

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            draw_chart(json["chart_data"]);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr) {
            $('#feedback').html("<div class='alert alert-danger'>Oops! We have encountered an error."); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


// Submit csv on submit
$('#form-csv').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    upload_csv();
});


// AJAX for upload csv file
function upload_csv() {
    console.log("upload csv is working!"); // sanity check
    var data = new FormData($('form').get(0));

    $.ajax({
        url : "/", // the endpoint
        type : "POST", // http method
        contentType: false,
        dataType: 'json',
        data : data,
        processData: false,

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            $('#feedback').html("<div class='alert alert-success'>Data successfully uploaded!"); // add the success msg to the dom
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr) {
            $('#feedback').html("<div class='alert alert-danger'>Oops! We have encountered an error."); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
