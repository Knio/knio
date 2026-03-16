const upload = document.getElementById('upload');
const preview = document.getElementById('preview');
const log = document.getElementById('log');


function postForm(data) {

  fetch('/updo', {
    method: 'POST',
    body: data
  }).then(res => {
    if (!res.ok) throw new Error('Upload failed');
    return res.text();
  }).then(text => {
    log.appendChild(document.createTextNode('\nUpload success: ' + text));
  }).catch(err => {
    log.appendChild(document.createTextNode('\nUpload error: ' + err));
  });

}


const handleFile = (file) => {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('toirc', 'true');
  postForm(formData);

  /*
  // client side preview
  const reader = new FileReader();
  reader.onload = () => {
    const img = document.createElement('img');
    img.src = reader.result;
    // TODO make div with spinner, etc
    preview.appendChild(img);
  };
  reader.readAsDataURL(file);
  */
};

function handleText(text) {
  const formData = new FormData();
  formData.append('txt', text);
  formData.append('toirc', 'true');
  postForm(formData);
}


document.body.addEventListener('paste', (e) => {
  e.preventDefault();
  const items = e.clipboardData.items;
  for (let item of items) {
    console.log(item);
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile();
      handleFile(file);
    }
    if (item.type.startsWith('text/plain')) {
      item.getAsString(handleText);
    }
    console.log(`what to do with ${item.type}?`);
  }
});

document.body.addEventListener('dragover', (e) => {
  console.log(['dragover', e]);
  e.preventDefault();
});

document.body.addEventListener('drop', (e) => {
  console.log(['drop', e]);
  e.preventDefault();
  const items = e.dataTransfer.files;
  for (let file of items) {
      handleFile(file);
  }
});


const file = document.getElementsByName('file')[0];
file.addEventListener('change', (e) => {
  const formData = new FormData(file.form);
  postForm(formData);
  file.form.reset();
});

