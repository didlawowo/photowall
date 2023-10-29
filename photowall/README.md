# Photowall gumpy

## mode dev

export FLASK_ENV=development

flask run

## install

```python
pip install pipenv
python3 -m pipenv install
```

## config

copy .env.example to .env and change parameters

## mode prod

run auto_start.cmd

## Nouvelle évènement

- 1 - Créer un nouveau logo client, appelé logo.jpg et le copier dans le dossier photowall/statis/logo_client
- 2 - purger le dossier photowall dans static
- 3 - modifier le fichier app_conf.py pour changer la valeur d'event_name pour mettre le nom de l'évènement client dans dslrbooth
- 4 - ouvrir le terminal et faire " cd C:\Users\gumpy\Documents\GitHub\photowall"
- 4 - lancer auto_start.cmd
- 5 - aller sur localhost:5000 pour voir si tout fonctionne bien
- 6 - tester sur la tablette avec l'IP wifi de la box  
- 7 - tester l'upload

## to dev

pipenv install
pipenv shell

python app.py

## change logo client

go to index.html
and change

```html

            <h1><img class="logo" src="static/logo/gumpy_transparent.png" alt="logo"></h1>
```
