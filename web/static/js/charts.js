function createDataSeries(data = []) {
    var series = []
    data.forEach((val) => {
        var serie = {
            name: val.label,
            data: val.data.length == 0 ? [0] : val.data,
        }
        series.push(serie)
    })
    return series
}

function createStaticLinePolarChart(el, title, labels, seriesName, data, polar = false, chartType = 'line') {
    Highcharts.chart(el, {
        chart: {
            polar: polar,
            type: chartType
        },
        title: {
            text: title,
            x: 0
        },
        pane: {
            size: '80%'
        },
        xAxis: {
            // categories: ['Akurasi', 'Kecepatan', 'Teknik', 'Fisik'],
            categories: labels,
            tickmarkPlacement: 'on',
            lineWidth: 0,
        },
        yAxis: {
            title: {
                text: null
            },
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0
        },
        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },
        legend: {
            enabled: false,
            align: 'top',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
        },
        series: [{
            name: seriesName,
            data: data,
            pointPlacement: 'on'
        }]
    });
}

function createDynamicLinePolarChart(el, title, labels, seriesName, data, polar = false, chartType = 'line') {
    Highcharts.chart(el, {
        chart: {
            polar: polar,
            type: chartType
        },
        title: {
            text: title,
            x: 0
        },
        pane: {
            size: '80%'
        },
        xAxis: {
            // categories: ['Akurasi', 'Kecepatan', 'Teknik', 'Fisik'],
            categories: labels,
            tickmarkPlacement: 'on',
            lineWidth: 0,
        },
        yAxis: {
            title: {
                text: null
            }
        },
        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },
        legend: {
            enabled: false,
            align: 'top',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
        },
        series: createDataSeries(data)
    });
}

function createBarChart(el, title, labels, data) {
    Highcharts.chart(el, {
        chart: {
            type: 'column'
        },
        title: {
            text: title
        },
        xAxis: {
            min: 0,
            categories: ['Pria', 'Wanita', 'Hello'],
            crosshair: false,
            labels: {
                enabled: false
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: null
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: createDataSeries(data)
    });
}

function createPieDataSeries(data = []) {
    var series = []
    data.forEach((val) => {
        var serie = {
            name: val.label,
            y: val.data,
        }
        series.push(serie)
    })

    return series
}

function createPieChart(el, title, data) {
    Highcharts.chart(el, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: title
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: title,
            colorByPoint: true,
            data: createPieDataSeries(data)
        }]
    });
}