function set_service_icon(iframe_id, icon_path) {
  const service_id = iframe_id.slice(iframe_id.indexOf("_") + 1);
  let spinner = $(`#${service_id}`).children("img.spinner");
  spinner.attr("src", icon_path)
  spinner.removeClass("spinner")
}

function logoutSuccess(iframe_id, success_img_path) {
  set_service_icon(iframe_id, success_img_path)
}

function logoutFailure(iframe_id, failure_img_path) {
  set_service_icon(iframe_id, failure_img_path)
}

document.addEventListener("DOMContentLoaded", function(){
  const graph = (document.getElementById("heuristic-graph"));
  if (graph) {
    let chart;
    nv.addGraph(function() {
        chart = nv.models.multiBarChart()
        const data = 
        [{
            "color": "#0000E1",
            "key": "Logins by hour",
            "values": JSON.parse(graph.getAttribute('heuristic_data'))
        }];

        chart
            .x(function(data) {
                return data.label;
            })
            .y(function(data) {
                return data.value;
            })
            .showControls(false);
        
       chart.groupSpacing(.2);
        
       chart.yAxis
            .tickFormat(d3.format(''));
        
       d3.select("#heuristic-graph svg")
            .datum(data)
            .transition()
            .duration(350)
            .call(chart);
        
       nv.utils.windowResize(chart.update);
        return chart;
    });
  }
})
