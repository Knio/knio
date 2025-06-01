const upload = document.getElementById('upload');
const preview = document.getElementById('preview');
const log = document.getElementById('log');


const handleFile = (file) => {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('toirc', 'true');

  fetch('/updo', {
    method: 'POST',
    body: formData
  }).then(res => {
    if (!res.ok) throw new Error('Upload failed');
    return res.text();
  }).then(text => {
    log.appendChild(document.createTextNode('\nUpload success: ' + text));
  }).catch(err => {
    log.appendChild(document.createTextNode('\nUpload error: ' + err));
  });


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


document.body.addEventListener('paste', (e) => {
  e.preventDefault();
  const items = e.clipboardData.items;
  for (let item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile();
      handleFile(file);
    }
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


log.appendChild(document.createTextNode('Paste, Drag, or Select an image here to upload.'));
log.appendChild(document.createTextNode("\n$ curl https://img.zkpq.ca/updo -X POST -F 'file=@your_file.jpg' "));
log.appendChild(document.createTextNode("\n$ wget https://img.zkpq.ca/updo --method=POST --body-file 'your_file.jpg' "));
