import {MnistData} from './data.js'

const loadImageButton = document.querySelector('#load-image-button');
const predictButton = document.querySelector('#predict-button');
const TauxClass = document.querySelector('#taux-button');
const MatriceConfusion = document.querySelector('#matrice-button');
const classification = document.querySelector('#classification');
const matrice = document.querySelector('#matrice');
const classNames = ['Zéro', 'Un', 'Deux', 'Trois', 'Quatre', 'Cinq', 'Six', 'Sept', 'Huit', 'Neuf'];
var model;
var data;
var image_input;
var number = 0;

async function run(){
    data = new MnistData();
    await data.load();
    model = await tf.loadLayersModel("/res/MLP/MLP.json");
}

function getNumber() {
    number = document.getElementById("nombre").value;
    console.log(number);
}

document.addEventListener('DOMContentLoaded', run);

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

TauxClass.addEventListener('click', () => {
    getNumber();
    if(number > 0){
        showAccuracy(model, data, Number(number));
    } else {
        console.log("Number n'est pas positif");
    }
});

MatriceConfusion.addEventListener('click', () => {
    getNumber();
    if(number > 0){
        showConfusion(model, data, Number(number));
    } else {
        console.log("Number n'est pas positif");
    }
});


function make_prediction(model,data) {
  image_input = tf.browser.fromPixels(data,1);
  image_input = tf.squeeze(image_input);
  image_input = image_input.expandDims(null);
  const preds = model.predict(image_input);
  return preds;
}

function doPrediction(model, data, testDataSize) {
  const IMAGE_WIDTH = 28;
  const IMAGE_HEIGHT = 28;
  const testData = data.nextTestBatch(testDataSize);
  const testxs = testData.xs.reshape([testDataSize, IMAGE_WIDTH, IMAGE_HEIGHT]);
  const labels = testData.labels.argMax(-1);
  const preds = model.predict(testxs).argMax(-1);
  testxs.dispose();
  return [preds, labels];
}

async function showAccuracy(model, data, nbData) {
  const [preds, labels] = doPrediction(model, data, nbData);
  const classAccuracy = await tfvis.metrics.perClassAccuracy(labels, preds);
  //const container = {name: 'Accuracy', tab: 'Evaluation'};
  tfvis.show.perClassAccuracy(classification, classAccuracy, classNames);
  labels.dispose();
}

async function showConfusion(model, data, nbData) {
  const [preds, labels] = doPrediction(model, data, nbData);
  const confusionMatrix = await tfvis.metrics.confusionMatrix(labels, preds);
  //const container = {name: 'Confusion Matrix', tab: 'Evaluation'};
  tfvis.render.confusionMatrix(matrice, {values: confusionMatrix, tickLabels: classNames});
  labels.dispose();
}