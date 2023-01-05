/*var button = document.getElementById("load-button");
var imageLoaded = false;

button.addEventListener("click", searchOutput = function () {
  if (!imageLoaded) {
    var image = new Image();
    image.src = "téléchargement.jpg";
    document.body.appendChild(image);
    imageLoaded = true;
  }
});*/

const loadImageButton = document.querySelector('#load-image-button');
const image = document.querySelector('#image');

loadImageButton.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();

    input.addEventListener('change', () => {
        const file = input.files[0];
        const reader = new FileReader();
        
        reader.addEventListener('load', () => {
            image.src = reader.result;
        });
        
        reader.readAsDataURL(file);
    });
});