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
                background-color: #38023B;
            }

            h1{
                font-weight: bold;
                color: #95D9DA;
            }

            body{
                background-color: #95D9DA;
            }

            figcaption{
                font-weight: bold;
                color: #38023B;
            }

            span{
                font-size: 15px;
                font-weight: bold;
                color: #38023B;
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
                margin-left: 55px;
            }

            .color {
                width: 25px;
                height: 25px;
                margin-right: 8px;
                border: 2px solid #38023B;
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

            table {
                width: 100%;
                border-collapse: collapse;
            }

            td {
                padding: 10px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #38023B;
            }
           
            form{
                position:fixed;
                left: 48%;
                transform: translate(-50%, -50%);
            }

            input{
                background-color: #38023B;
                color: #95D9DA;
                font-weight: bold;
                width: 200px;
                height: 50px;
                border-radius: 8%;
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="container-fluid">
                <table>
                    <tr>
                        <td class="col-md-4 offset-md-1"><img src="image/isen.png"></td>
                        <td class="col-md-4 offset-md-2"><h1>SUIM</h1></td>             
                    </tr>
                </table>
            </div>
        </nav>

          <br><br>

"""
print(html)


#chargement du modèle


## input/output shapes
base_ = 'RSB' # or 'VGG'

im_res_ = (320, 240, 3) 
ckpt_name = "models/suimnet_rsb5.hdf5"

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
                        <figure>
                            <figcaption>Image avant seg :</figcaption>
                            <img src="image/image_input.jpg" alt="" height="320">
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
                        <figure>
                            <figcaption>Image apres seg :</figcaption>
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
                      </div>
                </div>
          </div>

          <br><br><br>

          <form method="post" action="index.py">
                <input type="submit" value="Retour page accueil">
          </form>
    </body>
</html>

"""

print(html)
