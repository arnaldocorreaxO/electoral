var input_daterange;

function generateReport(all) {
    var parameters = {
        'action': 'search_report',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }

    $.ajax({
        url: pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json',
    }).done(function (request) {
        if (!request.hasOwnProperty('error')) {
            console.log(request);
            Highcharts.chart('container', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                exporting: {
                    enabled: false
                },
                title: {
                    text: ''
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.y:.1f}$</b>'
                },
                accessibility: {
                    point: {
                        valueSuffix: '%'
                    }
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                        },
                        showInLegend: true
                    },
                },
                series: [{
                    name: 'Total',
                    colorByPoint: true,
                    data: request
                }]
            });
            return false;
        }
        message_error(request.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

$(function () {

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            },
        });

    $('.drp-buttons').hide();

    $('.btnSearchReport').on('click', function () {
        generateReport(false);
    });

    $('.btnSearchAll').on('click', function () {
        generateReport(true);
    });

    generateReport(false);
});