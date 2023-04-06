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
<head>
    <meta charset="utf-8">
    <title>Ma page web</title>
<head>
<body>
    <h1>Page de resultat</h1>
</body>

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
print("model loaded")


#enregistrement de l'image d'entrée
file = open("image/image_input.jpg", "wb")
file.write(username)
file.close()


#affichage de l'image d'entrée
html = """<img src="image/image_input.jpg">"""
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
    print ("tested: {0}".format(name_image))
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

#affichage de l'image d'entrée
html = """<img src="image/image_output.jpg">"""
print(html)
