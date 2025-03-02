
timeline = document.querySelector('#timeline');
debug = document.querySelector('#debug');
time_range = [0,0];
selected_ip = 0n;
ipapi = new Map();
ipapi_raw.map(x => ipapi.set(x[0], x[1]));

var topn = document.querySelectorAll('#topn input');
topn.forEach(x => x.addEventListener('change', x => {
  selected_ip = Number(x.target.value);
  console.log(selected_ip);
}));


function is_local(ip) {
  ip = BigInt(ip);
  return (ip & 0xFFFF0000n) === 0x0A570000n;
}

function ip_from_int(x) {
  x = BigInt(x);
  return ((x >> 24n) & 0xFFn) + '.' +
         ((x >> 16n) & 0xFFn) + '.' +
         ((x >> 8n) & 0xFFn) + '.' +
         (x & 0xFFn);
}

class IpTrie {
  constructor(ip, depth) {
      ip = BigInt(ip);
      this.depth = BigInt(depth || 0);
      var ip_masked = BigInt(ip) & (~(0xffffffffn >> this.depth));
      this.ip = ip_masked;
      this.bytes_in = 0;
      this.bytes_out = 0;
      this.children = new Map();
  }

  label() {
    var l = "";
    if (this.depth == 32) {
      l += ip_from_int(this.ip);
    }
    else {
      l += ip_from_int(this.ip) + "/" + (this.depth);
    }
    var m = ipapi.get(Number(this.ip));
    if (m?.org) {
      l += " " + m.org;
    } else if (m?.isp) {
      l += " " + m.isp;
    } else if (m?.as) {
      l += " " + m.as;
    } else if (m?.country) {
      l += " " + m.country;
    } else if (m?.message) {
      l += " " + m.message;
    }
    return l;
  }

  add(ip, bytes_in, bytes_out) {
    if (this.depth >= 32n) {
      this.bytes_in += bytes_in;
      this.bytes_out += bytes_out;
      return;
    }
    ip = BigInt(ip);
    var x = (ip & (1n << (31n - this.depth))) ? 1 : 0;
    if (!this.children.has(x)) {
      this.children.set(x, new IpTrie(ip, this.depth + 1n));
    }
    this.children.get(x).add(ip, bytes_in, bytes_out);
  }

  collapse() {
    if (this.depth === 32n) {
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
  console.log(tries);
  console.log(selected_ip);

  var root = tries.get(selected_ip);
  console.log(root);
  if (root === undefined) {
    return;
  }
  var [labels, parents] = tries.get(selected_ip).collapse();
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
    width: 1000,
    height: 1000
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
