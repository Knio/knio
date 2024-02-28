
timeline = document.querySelector('#timeline');
debug = document.querySelector('#debug');
time_range = [0,0];


function is_local(ip) {
  return (ip & 0xFFFF0000) === 0x0A570000;
}

function ip_from_int(x) {
  return ((x >> 24) & 0xFF) + '.' +
         ((x >> 16) & 0xFF) + '.' +
         ((x >> 8) & 0xFF) + '.' +
         (x & 0xFF);
}

class IpTrie {
  constructor(ip, depth) {
      this.ip = ip;
      this.depth = depth || 0;
      this.bytes_in = 0;
      this.bytes_out = 0;
      this.children = new Map();
  }

  label() {
    if (this.depth == 32) {
      return ip_from_int(this.ip);
    }
    return ip_from_int(this.ip) + "/" + (this.depth);
  }

  add(ip, bytes_in, bytes_out) {
    if (this.depth >= 32) {
      this.bytes_in += bytes_in;
      this.bytes_out += bytes_out;
      return;
    }
    var x = (ip & (1 << this.depth)) && 1;
    if (!this.children.has(x)) {
      this.children.set(x, new IpTrie(ip, this.depth + 1));
    }
    this.children.get(x).add(ip, bytes_in, bytes_out);
  }

  collapse() {
    if (this.depth == 32) {
      return [[this], [null]];
    }
    if (this.children.size == 2) {
      var names = [];
      var parents = [];
      for (var i = 0; i < 2; i++) {
        var [names_i, parents_i] = this.children.get(i).collapse();
        names = names.concat(names_i);
        parents = parents.concat(parents_i);
        parents.pop(); // pop the root
        parents.push(this);
      }
      names.push(this);
      parents.push(null);
      return [names, parents];
    }
    if (this.children.has(0)) {
      return this.children.get(0).collapse();
    }
    if (this.children.has(1)) {
      return this.children.get(1).collapse();
    }
  }
}


function update_zoom(data) {
  debug.innerText = JSON.stringify(data);

  var tries = new Map();
  for (var i = 0; i < data.length; i++) {
    var [ip_a, ip_b, bytes] = data[i];
    var bytes_in = 0, bytes_out = 0;
    var str_a = ip_from_int(ip_a);
    var str_b = ip_from_int(ip_b);
    if (is_local(ip_a)) {
      bytes_in = bytes;
    } else if (is_local(ip_b)) {
      [ip_a, ip_b] = [ip_b, ip_a];
      bytes_out = bytes;
    } else {
      console.log(['not local', str_a, str_b, ip_a, ip_b]);
    }

    if (!tries.has(ip_a)) {
      tries.set(ip_a, new IpTrie(ip_a, 0));
    }
    tries.get(ip_a).add(ip_b, 0, bytes_in, bytes_in);
  }

  debug.innerText = JSON.stringify(tries);

  var [labels, parents] = tries.get(173473802).collapse();
  console.log([labels, parents]);

  var labels_strs = labels.map(n => n.label() );
  var parents_strs = parents.map(n => n && n.label() || "");
  var values = labels.map(n => n.bytes_in + n.bytes_out );

  console.log([labels_strs, parents_strs, values]);

  var graph_data = [{
    type: "sunburst",
    labels: labels_strs,
    parents: parents_strs,
    values:  values,
    outsidetextfont: {size: 20, color: "#377eb8"},
    leaf: {opacity: 0.4},
    marker: {line: {width: 2}},
  }];

  var layout = {
    margin: {l: 0, r: 0, b: 0, t: 0},
    width: 500,
    height: 500
  };

  Plotly.newPlot("details", graph_data, layout);
}


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
