#coding:utf-8
import cgi, cgitb

#import chargementdu modèle et prédiction
#from __future__ import print_function, division
#import os
import ntpath
import numpy as np
from PIL import Image
#from os.path import join, exists

# local libs
from ia.suim_net import SUIM_Net
from ia.data_utils import getPaths
from ia.data_utils import processSUIMDataRFHW
from ia.data_utils import getRobotFishHumanReefWrecks


#récupération de l'image  passée par la réquête de type post
cgitb.enable()
form = cgi.FieldStorage()

if form.getvalue("profile_pic"):
    username = form.getvalue("profile_pic")
else:
    raise Exception("Image non transmise")


#affichage html
print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Result</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
        
        <style>
            .navbar{
                background-color: #c21111;
            }

            h1{
                font-weight: bold;
                color: #e5e7e7;
                margin-left: auto;
                margin-right: auto;
            }

            body{
                color:white;
            }

            .container-fluid{
                padding-left: 0%;
            }

            .container{
                background-color: rgba(0,0,0,0.2);
                border-radius: 1em;
            }

            #vid2{
                position: fixed; right: 0; bottom: 0;
                min-width: 100%; min-height: 100%;
                width: auto; height: auto; z-index: -100;
                background-size: cover;
            }

            figcaption{
                font-weight: 500;
                color: #e5e7e7;
            }

            span{
                font-size: 15px;
                font-weight:500;
                color: #e5e7e7;
            }

            .legend {
                display: flex;
                flex-direction: row;
                font-size: 14px;
            }

            .legend-item {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
                margin-left: 25px;
            }

            .color {
                width: 25px;
                height: 25px;
                margin-right: 8px;
                border: 2px solid black;
                border-radius: 20%;
            }

            .blue {
                background-color: blue;
            }

            .cyan {
                background-color: cyan;
            }

            .red {
                background-color: red;
            }

            .yellow {
                background-color: yellow;
            }

            .pink {
                background-color: magenta;
            }

            .black{
                background-color: black;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            td {
                padding: 10px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #e5e7e7;
            }
           
            form{
                position:relative;
                margin-right: auto;
                margin-left: auto;
                translate: 425px;
            }

            input{
                background-color: #c21111;
                color: #e5e7e7;
                font-weight: bold;
                width: 200px;
                height: 50px;
                border-radius: 1em;
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="container-fluid">
                <img src="image/isen.png" class="isen">
                <h1>SUIM-Net : VGG</h1>
            </div>
        </nav>

        <div id="vid">
            <video autoplay muted loop id="vid2">
                <source src="video/sous-marin-26830.mp4" type="video/mp4">
            </video>
        </div>

          <br><br>

"""
print(html)


#chargement du modèle


## input/output shapes
base_ = 'VGG' # or 'RSB'

im_res_ = (320, 240, 3) 
ckpt_name = "models/suimnet_vgg5.hdf5"

suimnet = SUIM_Net(base=base_, im_res=im_res_, n_classes=5)
model = suimnet.model
#print (model.summary())
model.load_weights(ckpt_name)
#print("model loaded")


#enregistrement de l'image d'entrée
file = open("image/image_input.jpg", "wb")
file.write(username)
file.close()


#affichage de l'image d'entrée
html = """
          <div class="container">
                <div class="row">
                    <div class="col-md-4 offset-md-1">
                        <br>
                        <figure>
                            <figcaption>Image d'entree :</figcaption>
                            <img src="image/image_input.jpg" alt="" height="""

print(html)
print(im_res_[1])
html =""" width="""
print(html)
print(im_res_[0])

html = """>
                          </figure>
                
                    </div>

"""
print(html)


#prédiction
im_h, im_w = im_res_[1], im_res_[0]

def Generator(name_image):

    # read and scale inputs
    img = Image.open(name_image).resize((im_w, im_h))
    img = np.array(img)/255.
    img = np.expand_dims(img, axis=0)
    # inference
    out_img = model.predict(img)
    # thresholding
    out_img[out_img>0.5] = 1.
    out_img[out_img<=0.5] = 0.
    #print ("tested: {0}".format(name_image))
    # get filename
    img_name = ntpath.basename(name_image).split('.')[0] + '.bmp'
    # save individual output masks
    ROs = np.reshape(out_img[0,:,:,0], (im_h, im_w))
    FVs = np.reshape(out_img[0,:,:,1], (im_h, im_w))
    HDs = np.reshape(out_img[0,:,:,2], (im_h, im_w))
    RIs = np.reshape(out_img[0,:,:,3], (im_h, im_w))
    WRs = np.reshape(out_img[0,:,:,4], (im_h, im_w))
    
    #assembling masks
    classes = {"RO":ROs,"FV":FVs,"WR":WRs,"HD":HDs,"RI":RIs}
    #im_h, im_w = 240, 320
    channel = 3

    #création du mask final avec les couleurs
    img_numpy = np.zeros((im_h, im_w, channel), dtype=np.uint8)
    
    for name,mask in classes.items():
  
        #set the color depending on the class
        for i in range(im_h):
            for j in range(im_w):
                if(mask[i,j] == 1):
                    #robots == red
                    if (name == "RO"):
                        img_numpy[i,j] = (255, 0, 0)
                    #Fish and vertebrates == yellow
                    elif (name == "FV"):
                        img_numpy[i,j] = (255, 255, 0) 
                    #Wrecks/ruins == cyan
                    elif (name == "WR"):
                        img_numpy[i,j] = (0, 255, 255) 
                    #Human divers == blue
                    elif (name == "HD"):
                        img_numpy[i,j] = (0, 0, 255) 
                    #Reefs and invertebrates
                    elif (name == "RI"):
                        img_numpy[i,j] = (255, 0, 255)         

            
    img = Image.fromarray(img_numpy, "RGB")
    #img.show()
    #Image.fromarray(img.save(img_name))
    img = img.save("image/image_output.jpg")

Generator('image/image_input.jpg')


#affichage de l'image de sortie
html = """
 <div class="col-md-4 offset-md-2">
                        <br>
                        <figure>
                            <figcaption>Image de sortie :</figcaption>
                            <img src="image/image_output.jpg" alt="">
                          </figure>
                        <br>
                    </div>

                    <div class="legend">
                        <div class="legend-item">
                            <div class="color red"></div>
                            <span>Robots/Instruments</span>
                        </div>
                        <div class="legend-item">
                            <div class="color yellow"></div>
                            <span>Poissons/vertebres</span>
                        </div>
                        <div class="legend-item">
                            <div class="color cyan"></div>
                            <span>Epaves/Ruines</span>
                          </div>
                        <div class="legend-item">
                            <div class="color blue"></div>
                            <span>Plongeurs</span>
                          </div>
                        <div class="legend-item">
                          <div class="color pink"></div>
                          <span>Recifs/Invertebres</span>
                        </div>
                        <div class="legend-item">
                            <div class="color black"></div>
                            <span>Eau/Fond marin/rochers/Plantes</span>
                        </div>
                      </div>
                </div>
                <br><br><br>

            <form method="post" action="index.py">
                    <input type="submit" value="Retour page accueil">
            </form>
            <br>
          </div>
    </body>
</html>


"""

print(html)
