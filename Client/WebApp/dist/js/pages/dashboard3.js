$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }

  var mode      = 'index'
  var intersect = true

  var $salesChart = $('#sales-chart')
  var salesChart  = new Chart($salesChart, {
    type   : 'bar',
    data   : {
      labels  : ['Sarana dan Prasarana', 'Akademik', 'Humas', 'Litbang', 'Rektorat'],
      datasets: [
        {
          backgroundColor: '#007bff',
          borderColor    : '#007bff',
          data           : [400, 300, 200, 50, 50]
        }
      ]
    },
    options: {
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true,
            lineWidth    : '4px',
            color        : 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks    : $.extend({
            beginAtZero: true,

            // Include a dollar sign in the ticks
            callback: function (value, index, values) {
              if (value >= 1000) {
                value /= 1000
                value += 'k'
              }
              return value
            }
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          gridLines: {
            display: false
          },
          ticks    : ticksStyle
        }]
      }
    }
  })

  var $visitorsChart = $('#visitors-chart')
  var visitorsChart  = new Chart($visitorsChart, {
    data   : {
      labels  : ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
      datasets: [{
        type                : 'line',
        data                : [100, 120, 170, 167, 180, 177, 160],
        backgroundColor     : 'transparent',
        borderColor         : '#007bff',
        pointBorderColor    : '#007bff',
        pointBackgroundColor: '#007bff',
        fill                : false
        // pointHoverBackgroundColor: '#007bff',
        // pointHoverBorderColor    : '#007bff'
      },
        {
          type                : 'line',
          data                : [60, 80, 70, 67, 80, 77, 100],
          backgroundColor     : 'tansparent',
          borderColor         : '#ced4da',
          pointBorderColor    : '#ced4da',
          pointBackgroundColor: '#ced4da',
          fill                : false
          // pointHoverBackgroundColor: '#ced4da',
          // pointHoverBorderColor    : '#ced4da'
        }]
    },
    options: {
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true,
            lineWidth    : '4px',
            color        : 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          gridLines: {
            display: false
          },
          ticks    : ticksStyle
        }]
      }
    }
  })

  var pieChartCanvas1 = $('#pieChart1').get(0).getContext('2d')
  var pieData1        = {
    labels: [
        'Akademik', 
        'Pelayanan',
        'Sarana dan Prasarana', 
        'Keamanan',  
    ],
    datasets: [
      {
        data: [400,300,200,100],
        backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef'],
      }
    ]
  }
  var pieOptions     = {
    legend: {
      display: true
    }
  }
  var pieChart = new Chart(pieChartCanvas1, {
    type: 'pie',
    data: pieData1,
    options: pieOptions      
  })

  var pieChartCanvas2 = $('#pieChart2').get(0).getContext('2d')
  var pieData2        = {
    labels: [
        'Uncofirmed', 
        'Open',
        'Action', 
        'Closed',  
    ],
    datasets: [
      {
        data: [300,300,200,200],
        backgroundColor : ['#00a65a', '#f39c12', '#f56954', '#00c0ef'],
      }
    ]
  }
  var pieOptions     = {
    legend: {
      display: true
    }
  }
  var pieChart = new Chart(pieChartCanvas2, {
    type: 'pie',
    data: pieData2,
    options: pieOptions      
  })
})
