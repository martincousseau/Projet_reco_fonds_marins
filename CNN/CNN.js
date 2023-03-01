import {MnistData} from './data.js';

//button
const loadImageButton = document.querySelector('#load-image-button');
const predictButton = document.querySelector('#predict-button');
const accuracyButton = document.querySelector('#accuracy-button');
const confusionMatrixButton = document.querySelector('#confusion-matrix-button');


//display
const image = document.querySelector('#image');
const accuracyDisplay = document.querySelector('#accuracy-display');
const confusionMatrixDisplay = document.querySelector('#confusion-matrix-display');



var model;
var data;
var value = 0;


async function run() {
  data = new MnistData();
  await data.load();
  model = await tf.loadLayersModel("/res/CNN/CNN.json");
  console.log("model loaded");
}

document.addEventListener('DOMContentLoaded', run);

function getNbImage() {
  value = document.querySelector('#nb-image').value;
  console.log(value);
}

//fonction pour charger une image
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


//fonction de prédiction
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
  
  document.getElementById('display-prediction').innerHTML = "Le chiffre est : " + result;
});


function make_prediction(model,data) {
  var image_input = tf.browser.fromPixels(data,1);
  image_input = image_input.expandDims(null);
  const preds = model.predict(image_input);
  return preds;
}


//fonction pour générer le taux de classification
accuracyButton.addEventListener('click', () => {
  //récupération de la valeur
  getNbImage();

  if(value > 0){
    showAccuracy(model,data,Number(value));
  }
  else{
    console.log("nombre d'image nul");
  }
  
});



//fonction pour générer la matrice de confusion
confusionMatrixButton.addEventListener('click', () => {

  getNbImage();

  if(value > 0){
    showConfusion(model,data,Number(value));
  }
  else{
    console.log("nombre d'image nul");
  }
  
});




const classNames = ['Zéro', 'Un', 'Deux', 'Trois', 'Quatre', 'Cinq', 'Six', 'Sept', 'Huit', 'Neuf'];

function doPrediction(model, data, testDataSize) {
  const IMAGE_WIDTH = 28;
  const IMAGE_HEIGHT = 28;
  const testData = data.nextTestBatch(testDataSize);
  const testxs = testData.xs.reshape([testDataSize, IMAGE_WIDTH, IMAGE_HEIGHT, 1]);
  const labels = testData.labels.argMax(-1);
  const preds = model.predict(testxs).argMax(-1);

  testxs.dispose();
  return [preds, labels];
}

async function showAccuracy(model, data, nbData) {
  const [preds, labels] = doPrediction(model, data, nbData);
  const classAccuracy = await tfvis.metrics.perClassAccuracy(labels, preds);
  tfvis.show.perClassAccuracy(accuracyDisplay, classAccuracy, classNames);

  labels.dispose();
}


async function showConfusion(model, data, nbData) {
  const [preds, labels] = doPrediction(model, data, nbData);
  const confusionMatrix = await tfvis.metrics.confusionMatrix(labels, preds);
  tfvis.render.confusionMatrix(confusionMatrixDisplay, {values: confusionMatrix, tickLabels: classNames});

  labels.dispose();
}






