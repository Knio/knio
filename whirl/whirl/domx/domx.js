(function(){

  const dx = {
    replace: function(event, elem, target, uri, method, outer, before, after) {
      const click_target = event.target;
      console.log(event);
      console.log(click_target);
      if (click_target.nodeName === 'A') {
        return true;
      }
      event.preventDefault();
      event.stopPropagation();

      let target_node = null;
      if (target === 'this') {
        target_node = elem;
      } else if (target === 'parent') {
        target_node = elem.parentNode;
      } else {
        target_node = document.querySelector(target);
      }

      // if this is in a form, and method is post, capture the form data
      let cur = elem;
      let form = null;
      while ((cur !== null) && (cur != document.body)) {
        if (cur.nodeName === 'FORM') {
          form = cur;
          break;
        }
        cur = cur.parentNode;
      }

      const parent = target_node.parentNode;
      const sibling = target_node.previousElementSibling;

      function reshandler(response) {
        console.log(response);
        // if (!response.ok) {
        //   return
        // }
        response.text().then(data => {
          if (outer) {
            target_node.outerHTML = data;
          } else {
            target_node.innerHTML = data;
          }
          window.requestAnimationFrame(function(){
            console.log('after2');
            console.log(after);
            if (after) {
              after.call(target_node);
            }
          });
        });
      }

      options = {};

      if (method === 'post') {
        options.method = 'POST';
        if (form !== null) {
          options.body = new FormData(form);
        }
      }
      else if (method === 'get') {
        if (form !== null) {
          const fd = new FormData(form);
          const fs = new URLSearchParams(fd).toString();
          uri += '?' + fs;
        }
      }
      console.log('before');
      if (before) {
        r = before.call(target_node);
        if (r === false) {
          return;
        }
      }

      fetch(uri, options).then(reshandler);
      return false;
    }
  };

  window.dx = dx;
})();
