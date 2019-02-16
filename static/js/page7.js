if ($('#pie-chart-inf').length) {

  var data_pie = [];
  var series = 10;
  for (var i = 0; i < series; i++) {
    data_pie[i] = {
      label : "Series" + (i + 1),
      data : Math.floor(Math.random() * 100) + 1
    }
  }
  data_pie[0].label = "Emirates"
  data_pie[1].label = "Air France"
  data_pie[2].label = "KLM"
  data_pie[3].label = "Lufthansa"
  data_pie[4].label = "Alitalia"

  $.plot($("#pie-chart-inf"), data_pie, {
    series : {
      pie : {
        show : true,
        innerRadius : 0.5,
        radius : 1,
        label : {
          show : true,
          radius : 3 / 4,
          formatter : function(label, series) {
            return '<div style="font-size:10px;text-align:center;padding:0;color:white;">' + Math.round(series.percent) + '%</div>';
          },
          threshold : 0.1
        }
      }
    },
    legend : {
      show : true,
      noColumns : 2, // number of colums in legend table
      labelFormatter : null, // fn: string -> string
      labelBoxBorderColor : "#000", // border color for the little label boxes
      container : null, // container (as jQuery object) to put legend in, null means default on top of graph
      position : "ne", // position of default legend container within plot
      margin : [10, 0], // distance from grid edge to default legend container within plot
      backgroundColor : "#efefef", // null means auto-detect
      backgroundOpacity : 1 // set to 0 to avoid background
    },
    grid : {
      hoverable : true,
      clickable : true
    },
  });

}