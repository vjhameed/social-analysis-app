if ($('#pie-chart').length) {

  var data_pie = [];
  var series = 10;
  for (var i = 0; i < series; i++) {
    data_pie[i] = {
      label: "Series" + (i + 1),
      data: Math.floor(Math.random() * 100) + 1
    }
  }
  data_pie[0].label = 'Twitter'
  data_pie[1].label = 'Google'
  data_pie[2].label = 'Online'
  data_pie[3].label = 'Instagram'
  data_pie[4].label = 'YouTube'
  data_pie[5].label = 'Etc'
  data_pie[6].label = 'Forums'
  data_pie[7].label = 'Facebook'
  data_pie[8].label = 'Newspaper'
  data_pie[9].label = 'Other'

  $.plot($("#pie-chart"), data_pie, {
    series: {
      pie: {
        show: true,
        innerRadius: 0.5,
        radius: 1,
        label: {
          show: true,
          radius: 3 / 4,
          formatter: function (label, series) {
            return '<div style="font-size:10px;text-align:center;padding:0;color:white;">' + Math.round(series.percent) + '%</div>';
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
      margin: [30, 200], // distance from grid edge to default legend container within plot
      backgroundColor: "#efefef", // null means auto-detect
      backgroundOpacity: 1 // set to 0 to avoid background
    },
    grid: {
      hoverable: true,
      clickable: true
    },
  });

}