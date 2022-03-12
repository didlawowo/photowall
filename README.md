# Photowall gumpy

## mode dev

export FLASK_ENV=development

flask run

## install

pip install -r requirements.txt

## config

modify app_conf.py

## mode prod

run auto_start.cmd

## Nouvelle évènement

- 1 - Créer un nouveau logo client, appelé logo.jpg et le copier dans le dossier photowall/statis/logo_client
- 2 - purger le dossier photowall dans static
- 3 - modifier le fichier app_conf.py pour changer la valeur d'event_name pour mettre le nom de l'évènement client dans dslrbooth
- 4 - ouvrir le terminal et faire " cd C:\Users\gumpy\Documents\GitHub\photowall"
- 4 - lancer auto_start.cmd
- 5 - aller sur localhost:8080 pour voir si tout fonctionne bien
- 6 - tester sur la tablette avec l'IP wifi de la box  
- 7 - tester l'upload
