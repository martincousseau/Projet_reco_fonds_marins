#coding:utf-8
import cgi


print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Dataset</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
        <style>
            .navbar{
                background-color: #c21111;
            }

            td {
                padding: 10px;
                font-weight: bold;
                text-align: center;
                font-size: 16px;
                color: #c21111;
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
                color: #e5e7e7;
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

            form{
                text-align: center;
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
                <h1>A propos de SUIM</h1>
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
            <h2><u>Dataset SUIM</u></h3>
            <br>
                <ul>
                    <li>
                        <h5>Pourquoi SUIM ?</h5>
                        <p>SUIM veut tout simplement dire Segmentation of Underwater IMagery</p>
                    </li>
                    <li>    
                        <h5>Comment est compose SUIM ?</h5>
                        <p> SUIM est un jeu de donnees compose de 1525 images d'entrainements et 110 de tests.
                            <br>Les labels ont ete annote pixel par pixel par 7 personnes. Ils donnaient pour chaque pixel, la couleur de la categorie correspondante.
                            Voici des exemples de label avec les images associees :
                        </p>
                        <img src="image/labels.png" alt="">
                    </li>
                    <br>
                    <li>
                        <h5>Quelles sont les differentes categories ? Et quelles sont les couleurs qui correspondent ?</h5>
                        <p>Il y a 8 categories differentes et voici les couleurs associees : </p>
                        <img src="image/categories.png" alt="">
                        <p>Dans le projet, le modele a ete entraine pour seulement 6 categories. 
                            <br>Les categories "Aquatic plants and sea-grass" et "Sea-floor and rocks" sont dans "Background".</p>
                    </li>
                    <li>
                        <h5>Mesures entre les differents modeles</h5>
                        <ol>
                            <li>Mesure des performances : </li>
                            <img src="image/tableauFPS.png" alt="" width="500">
                            <li>Mesure de precision</li>
                            <img src="image/tableauPerf.png" alt="" width="1000">
                            <li>Comparaison des predictions</li>
                            <img src="image/tableauImage.png" alt="" width="1000">
                        </ol>
                    </li>
                </ul>
            <form method="post" action="index.py">
                <input type="submit" value="Retour page accueil">
            </form>
            <br>
        </div>
    </body>
</html>"""

print(html)