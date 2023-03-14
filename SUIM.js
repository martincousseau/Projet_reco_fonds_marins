//---------- Variables + Constantes -------------

const loadImageButton = document.querySelector('#load-image-button');
const predictButton = document.querySelector('#predict-button');
var x = document.getElementById("legende");
var model;
var data;
var image_input;
const IMAGE_WIDTH = 320;
const IMAGE_HEIGHT = 240;
const classes = ['RO', 'FV', 'WR', 'HD', 'RI'];
const channel = 3;
//var img_numpy = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, channel), dtype=np.uint8);


//------------- Fonction pour charger modele -------------

async function run(){
    model = await tf.loadLayersModel("/Projet_M1v2/res/model.json");
    console.log("model loaded");
}

document.addEventListener('DOMContentLoaded', run);

//--------- Chargement Image + Redimenssionner FONCTIONNEL -----------

loadImageButton.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();

    input.addEventListener('change', () => {
        const file = input.files[0];
        const reader = new FileReader();

        reader.addEventListener('load', () => {
            const img = new Image();
            img.src = reader.result;

            img.addEventListener('load', () => {
                // Créez une balise canvas avec la taille souhaitée
                const canvas = document.createElement('canvas');
                canvas.width = IMAGE_WIDTH;
                canvas.height = IMAGE_HEIGHT;

                // Dessinez l'image sur le canvas avec la nouvelle taille
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                // Créez une nouvelle balise image avec l'image redimensionnée
                const resizedImage = new Image();
                resizedImage.src = canvas.toDataURL('image/jpeg');

                // Remplacez l'image existante par la nouvelle image redimensionnée
                const oldImage = document.getElementById('image');
                oldImage.parentNode.replaceChild(resizedImage, oldImage);
            });
        });

        reader.readAsDataURL(file);
    });
});

// ------------- PREDICTION --------------

predictButton.addEventListener('click', () => {
    x.style.display = "block";
    /*var pred = make_prediction(model,image);
    pred = pred.dataSync();
    console.log(pred);
    var result = 0;
    for (var i in pred){
      if(pred[i] == '1'){
        result = i;
      } 
    }
    assemblingMasks(resizedImage);
    document.getElementById('display').src = "CHEMIN/VERS/IMAGE.png";*/
  });

function make_prediction(model,data) {
    image_input = tf.browser.fromPixels(data,1);
    image_input = tf.squeeze(image_input);
    image_input = image_input.expandDims(null);
    const preds = model.predict(image_input);
    return preds;
  }
  
  function doPrediction(model, data, testDataSize) {
    const testData = data.nextTestBatch(testDataSize);
    const testxs = testData.xs.reshape([testDataSize, IMAGE_WIDTH, IMAGE_HEIGHT]);
    const labels = testData.labels.argMax(-1);
    const preds = model.predict(testxs).argMax(-1);
    testxs.dispose();
    return [preds, labels];
  }

  //------------- NORMALEMENT FONCTIONNEL (AIDE DE CHATGPT) ------------
function assemblingMasks(img_name) {
    // création du mask final avec les couleurs
    const img_data = new Uint8ClampedArray(IMAGE_HEIGHT * IMAGE_WIDTH * channel);

    for (let i = 0; i < IMAGE_HEIGHT * IMAGE_WIDTH; i++) {
        img_data[i * channel] = 0;
        img_data[i * channel + 1] = 0;
        img_data[i * channel + 2] = 0;
    }

    for (let p of classes) {
        // get image and convert to np array
        const mask = new Image();
        mask.src = samples_dir + p + "/" + img_name;
        mask.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = IMAGE_WIDTH;
        canvas.height = IMAGE_HEIGHT;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(mask, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT);
        const mask_data = ctx.getImageData(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT).data;

        // set the color depending on the class
        for (let i = 0; i < IMAGE_HEIGHT; i++) {
            for (let j = 0; j < IMAGE_WIDTH; j++) {
            const idx = (i * IMAGE_WIDTH + j) * channel;
            const value = mask_data[idx];
            if (value === 255) {
                // robots == red
                if (p === "RO") {
                img_data[idx] = 255;
                img_data[idx + 1] = 0;
                img_data[idx + 2] = 0;
                }
                // Fish and vertebrates == yellow
                else if (p === "FV") {
                img_data[idx] = 255;
                img_data[idx + 1] = 255;
                img_data[idx + 2] = 0;
                }
                // Wrecks/ruins == cyan
                else if (p === "WR") {
                img_data[idx] = 0;
                img_data[idx + 1] = 255;
                img_data[idx + 2] = 255;
                }
                // Human divers == blue
                else if (p === "HD") {
                img_data[idx] = 0;
                img_data[idx + 1] = 0;
                img_data[idx + 2] = 255;
                }
                // Reefs and invertebrates
                else if (p === "RI") {
                img_data[idx] = 255;
                img_data[idx + 1] = 0;
                img_data[idx + 2] = 255;
                }
            }
            }
        }

        const canvas2 = document.createElement("canvas");
        canvas2.width = IMAGE_WIDTH;
        canvas2.height = IMAGE_HEIGHT;
        const ctx2 = canvas2.getContext("2d");
        const img = ctx2.createImageData(IMAGE_WIDTH, IMAGE_HEIGHT);
        img.data.set(img_data);
        ctx2.putImageData(img, 0, 0);
        const dataURL = canvas2.toDataURL();
        const imgEl = document.createElement("img");
        imgEl.src = dataURL;
        document.body.appendChild(imgEl);
        };
    }
}
