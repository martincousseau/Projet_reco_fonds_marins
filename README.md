# Projet_reco_fonds_marins
Projet de fin d'année M1, créer un site web qui est capable de faire une séparation sémantique sur des images de fonds marins.


Comment faire fonctionner le projet ?

 - Télecharger tous les fichiers de la branche suimnet(rsb)
 - Installer anaconda
 - Ouvrir un terminal base(root)
 - Taper la commande suivante : conda deactivate
 - Se déplacer dans le dossier du projet
 - Taper la commande suivante (création de l'environnement) : conda create --name <nom de l'environnement> --file spec-file.txt
 - Un nouvel environnement devrait apparaitre dans l'interface conda
 - Créer un dossier "models" à la racine du projet
 - Télecharger les 2 modèles suimnet ([ici](https://drive.google.com/drive/folders/1aoluekvB_CzoaqGhLutwtJptIOBasl7i?usp=sharing))
 - Placer les 2 modèles dans le dossier "models"
 - Ouvrir un terminal dans le nouvel environnement et se déplacer dans le dossier du projet
 - Taper la commande : python ./server.py
 - Ouvrir un navigateur et entre l'adresse ci-contre : localhost/index.py
