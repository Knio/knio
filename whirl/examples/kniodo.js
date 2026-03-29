
var MD = new remarkable.Remarkable({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(lang, str).value;
      } catch (err) {}
    }
    try {
      return hljs.highlightAuto(str).value;
    } catch (err) {}
    return ''; // use external default escaping
  }
}).use(remarkable.linkify);

function apply_markdown() {
  all('div.body.raw').foreach(function(e, d) {
    e.dom.innerHTML = MD.render(e.dom.innerHTML);
    e.remove_class('raw');
    e.add_class('markdown');
  });
};
