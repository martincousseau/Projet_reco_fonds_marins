
const loadImageButton = document.querySelector('#load-image-button');
const predictButton = document.querySelector('#predict-button');
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

predictButton.addEventListener('click', () => {
  var pred = make_prediction(model,image);
  pred = pred.dataSync();
  console.log(pred);
  var result = 0;
  for (var i in pred){
    if(pred[i] == '1'){
      result = i;
    }
     
  }
  
  document.getElementById('display').innerHTML = "Le chiffre est : " + result;
});

async function loadModel(){
  model = undefined;
  model = await tf.loadLayersModel("https://raw.githubusercontent.com/martincousseau/Projet_reco_fonds_marins/main/model.json");
  console.log("model loaded")
}


loadModel();


function make_prediction(model,data) {
  image_input = tf.browser.fromPixels(data,1);
  image_input = image_input.expandDims(null);
  const preds = model.predict(image_input);
  return preds;
}

