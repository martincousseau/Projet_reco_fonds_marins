#coding:utf-8
import cgi


print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ProjetM1</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script>
        $(document).ready(function (afficher) {
            $('input[id="files"]').on('change', (afficher) => {
                let a = afficher.currentTarget
                if (a.files && a.files[0]) {
                    $(a).next('.afficher').html(a.files[0].name)
                    let reader = new FileReader()
                    reader.onload = (afficher) => {
                        $('#voir').attr('src', afficher.target.result)
                    }
                    reader.readAsDataURL(a.files[0])
                }
            })
        });

        $(document).ready(function (afficher2) {
            $('input[id="fichier"]').on('change', (afficher2) => {
                let a = afficher2.currentTarget
                if (a.files && a.files[0]) {
                    $(a).next('.affiche').html(a.files[0].name)
                    let reader = new FileReader()
                    reader.onload = (afficher2) => {
                        $('#voi').attr('src', afficher2.target.result)
                    }
                    reader.readAsDataURL(a.files[0])
                }
            })
        });
    </script>
    <style>
        .navbar{
            background-color: #c21111;
        }

        td {
            padding: 10px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        h1{
            font-weight: bold;
            color: #e5e7e7;
            margin-left: auto;
            margin-right: auto;
        }

        .container-fluid{
            padding-left: 0%;
        }

        body{
            color:#e5e7e7;
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


        .form{
            display: flex;
            background-color: #c21111;
            color: #e5e7e7;
            font-weight: bold;
            width: 155px;
            height: 40px;
            border-radius: 1em;
        }

        .sub{
            background-color: #c21111;
            color: #e5e7e7;
            font-weight: bold;
            cursor: pointer;
            width: 180px;
            height: 40px;
            border-radius: 1em;
        }

        .dataset{
            text-align: center;
        }

        .btnDataset{
            background-color:#c21111;
            color:#e5e7e7;
            font-weight: bold;
            cursor: pointer;
            width: 275px;
            height: 40px;
            border-radius: 1em;
        }

    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container-fluid">
            <img src="image/isen.png" class="isen">
            <h1>Comprendre le milieu sous-marin</h1>
        </div>
    </nav>

    <div id="vid">
        <video autoplay muted loop id="vid2">
            <source src="video/sous-marin-26830.mp4" type="video/mp4">
        </video>
    </div>

      <br>

    <div class="container">
        <br>
        <h3>Selectionnez le modele :</h3>
        <br>
        <div class="row">
            <div class="col-sm-6">
                <h4>SUIM-Net RSB</h4>
                <br>
                <form method="post" action="suimnet_rsb.py" enctype="multipart/form-data" class="form">
                    <label for="files" class="btn" style="font-weight: bold;">Choisir une image</label>   
                    <input id="files" type="file" name="profile_pic" style="visibility:hidden;" accept="jpg" class="afficher">  
                    <input type="submit" value="Segmenter" class="sub">
                </form>
                <br>
                <img id="voir" src="" height="190" width="275" alt="">
                <br>
            </div>
        </div>
        <br>
        <div class="row">
            <div class="col-sm-6">
                <h4>SUIM-Net VGG</h4>
                <br>
                <form method="post" action="suimnet_vgg.py" enctype="multipart/form-data" class="form">
                    <label for="fichier" class="btn" style="font-weight: bold;">Choisir une image</label>   
                    <input id="fichier" type="file" name="profile_pic" style="visibility:hidden;" accept="jpg" class="affiche">  
                    <input type="submit" value="Segmenter" class="sub">
                </form>
                <br>
                <img id="voi" src="" height="190" width="275" alt="">
                <br>
            </div>
        </div>
        <br><br>
        <div class="data">
            <form method="post" action="aboutDataset.py" class="dataset">
                <input type="submit" value="En savoir plus sur le dataset SUIM" class="btnDataset">
            </form>
            <br>
        </div>
    </div>
</body>
</html>
"""

print(html)


#with open("templates/index.html", "w") as file:
#   file.write(html)

