var layout = {

};

timeline = document.querySelector('#timeline');
debug = document.querySelector('#debug');
layout = {
  title: "network traffic",
  xaxis: {
    rangeslider: {}
  },
  yaxis: {
    fixedrange: true
  }
};

function update_zoom(data) {
  debug.innerText = JSON.stringify(data);
}



time_range = [0,0];
timeline.on('plotly_relayout',
function(eventdata) {
    time_range = timeline.layout.xaxis.range.map(t => Math.floor(new Date(t).getTime()/1000));
    fetch("/domx/sumrange/" + time_range[0] + "/" + time_range[1]).then(response => {
      if (!response.ok) {
        debug.innerText = "response not ok";
        return;
      }
      response.json().then(data => {
        update_zoom(data);
      })
    })
});
