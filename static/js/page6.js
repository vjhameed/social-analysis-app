// Pie Chart
if ($('#pie-chart').length) {

  var data_pie = [];
  var series = 5;
  for (var i = 0; i < series; i++) {
    data_pie[i] = {
      label: "Series" + (i + 1),
      data: Math.floor(Math.random() * 100) + 1
    }
  }
  data_pie[0].label = "Emirates"
  data_pie[1].label = "Air France"
  data_pie[2].label = "KLM"
  data_pie[3].label = "Lufthansa"
  data_pie[4].label = "Alitalia"

  $.plot($("#pie-chart"), data_pie, {
    series: {
      pie: {
        show: true,
        innerRadius: 0.5,
        radius: 1,
        label: {
          show: true,
          radius: 2 / 3,
          formatter: function (label, series) {
            return '<div style="font-size:11px;text-align:center;padding:4px;color:white;">' + Math.round(series.percent) + '%</div>';
          },
          threshold: 0.1
        }
      }
    },
    legend: {
      show: true,
      noColumns: 1, // number of colums in legend table
      labelFormatter: null, // fn: string -> string
      labelBoxBorderColor: "#000", // border color for the little label boxes
      container: null, // container (as jQuery object) to put legend in, null means default on top of graph
      position: "ne", // position of default legend container within plot
      margin: [5, 10], // distance from grid edge to default legend container within plot
      backgroundColor: "#efefef", // null means auto-detect
      backgroundOpacity: 1 // set to 0 to avoid background
    },
    grid: {
      hoverable: true,
      clickable: true
    },
  });

}

// Pie Chart Ends

/* Sin chart */

// if ($("#sin-chart").length) {
//     var res = [parseInt(Math.random() * 2500000), parseInt(Math.random() * 400)];

//   var plot = $.plot($("#sin-chart"), [{
//     data : res,
//     label : "Results"
//   }], {
//     series : {
//       lines : {
//         show : false
//       },
//       points : {
//         show : true,
//         radius: 15,
//         fill: true,
//         fillColor: "#9834AA"
//       }
//     },
//     grid : {
//       hoverable : true,
//       clickable : true,
//       // tickColor : "#444",
//       borderWidth : 0,
//       // borderColor : "#fff",
//     },
//     tooltip : true,
//     tooltipOpts : {
//       // content : "Value <b>$x</b> Value <span>$y</span>",
//       defaultTheme : false
//     },
//     legend: false,
//     colors : ["#9834AA"],
//     yaxis : {
//       min : 0,
//       max : 400,
//       tickFormatter : function(val, axis) {
//         return val + 'G'
//       }
//     },
//     xaxis : {
//       min : 0,
//       max : 2500000,
//       tickSize: 250000,
//       tickFormatter : function(val, axis) {
//         var valStr = val.toString();
//         if (valStr.length > 6) {
//           return  valStr.slice(0, valStr.length - 6) + '.' + valStr.slice(1, valStr.length - 5) + 'M';
//         } else if (valStr.length > 3) {
//           return valStr.slice(0, valStr.length - 3) + 'K'
//         } else {
//           return val
//         }
//       }
//     }
//   });

//   $("#sin-chart").bind("plotclick", function(event, pos, item) {
//     if (item) {
//       $("#clickdata").text("You clicked point " + item.dataIndex + " in " + item.series.label + ".");
//       plot.highlight(item.series, item.datapoint);
//     }
//   });
// }

/* end sin chart */


window.onload = function () {
  // Bar Chart Starts


  // Bar Chart Data
  var barChartData = {
    labels: ['5 Aug', '6 Aug', '7 Aug', '8 Aug', '9 Aug', '10 Aug', '11 Aug'],
    datasets: [{
      label: 'Emirates',
      backgroundColor: "#EDC240",
      data: [30, 20, 10, 10, 30, 5, 20]
    }, {
      label: 'Air France',
      backgroundColor: "#AFD8F8",
      data: [20, 10, 20, 50, 10, 5, 20]
    }, {
      label: 'KLM',
      backgroundColor: "#CB4B4B",
      data: [10, 30, 5, 10, 40, 20, 25]
    }, {
      label: 'Lufthansa',
      backgroundColor: "#4DA74D",
      data: [20, 5, 20, 10, 10, 20, 25]
    }, {
      label: 'Alitalia',
      backgroundColor: "#9440ED",
      data: [20, 35, 45, 20, 10, 50, 10]
    }]

  };

  var ctx = document.getElementById('bar-chart').getContext('2d');
  window.myBar = new Chart(ctx, {
    type: 'bar',
    data: barChartData,
    options: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 20
        }
      },
      title: {
        display: false
      },
      tooltips: {
        mode: 'index',
        intersect: false
      },
      responsive: true,
      scales: {
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true
        }]
      }
    }
  });
  // Bar Chart Ends

  // Horizontal Bar Chart Starts

  // Bar Chart Data
  var hbarChartData = {
    labels: ['Emirates', 'Air France', 'KLM', 'Lufthansa', 'Alitalia'],
    datasets: [{
      label: 'Positive',
      backgroundColor: "#4DA74D",
      data: [30, 50, 40, 60, 10, 10, 80]
    }, {
      label: 'Neutral',
      backgroundColor: "#EDC240",
      data: [20, 40, 50, 20, 60, 80, 15]
    }, {
      label: 'Negative',
      backgroundColor: "#CB4B4B",
      data: [50, 10, 10, 20, 30, 10, 5]
    }]

  };

  var ctx = document.getElementById('hbar-chart').getContext('2d');
  window.myBar = new Chart(ctx, {
    type: 'horizontalBar',
    data: hbarChartData,
    options: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 20
        }
      },
      title: {
        display: false
      },
      tooltips: {
        mode: 'index',
        intersect: false
      },
      responsive: true,
      scales: {
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true
        }]
      }
    }
  });
  // Horizontal Bar Chart Ends

  // Bubble Chart Start
  new Chart(document.getElementById("bubble-chart"), {
    type: 'bubble',
    data: {
      labels: "",
      datasets: [
        {
          label: ["Emirates"],
          backgroundColor: "#EDC240",
          borderColor: "#f9db81",
          data: [{
            x: 73015,
            y: 320,
            r: 30,
            name: '12'
          }]
        }, {
          label: ["Air France"],
          backgroundColor: "#AFD8F8",
          borderColor: "#dbeefc",
          data: [{
            x: 22100,
            y: 80,
            r: 20
          }]
        }, {
          label: ["KLM"],
          backgroundColor: "#CB4B4B",
          borderColor: "#e07d7d",
          data: [{
            x: 29000,
            y: 100,
            r: 20
          }]
        }, {
          label: ["Lufthansa"],
          backgroundColor: "#4DA74D",
          borderColor: "#86ce86",
          data: [{
            x: 10000,
            y: 80,
            r: 20
          }]
        }, {
          label: ["Alitalia"],
          backgroundColor: "#9440ED",
          borderColor: "#ba84f4",
          data: [{
            x: 5200,
            y: 0,
            r: 10
          }]
        }
      ]
    },
    options: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 20
        }
      },
      tooltips: {
        callbacks: {
          label: function (t, d) {
            return d.datasets[t.datasetIndex].label + ' : ' + t.xLabel + ' results, ' + t.yLabel + ' engagements';
          }
        }
      },
      title: {
        display: false,
        text: ''
      }, scales: {
        yAxes: [{
          ticks: {
            callback: function (value, index, values) {
              return value + 'G';
            },
            max: 400
          }
          // scaleLabel: {
          // display: true,
          // labelString: "Happiness"
          // }
        }],
        xAxes: [{
          ticks: {
            max: 100000
          }
          // scaleLabel: {
          // display: true,
          // labelString: "GDP (PPP)"
          // }
        }]
      }
    }
  });
  // Bubble Chart End
};