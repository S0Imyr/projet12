# CRM API

Il s'agit de créer une API pour le CRM d'une entreprise dans l'évenementiel.

## Installation
### Fichiers du site
Sur le terminal se placer sur un dossier cible.

Puis suivre les étapes suivantes :
1. Cloner le dépôt ici présent en tapant: `git clone https://github.com/rlossec/CRM-API-Event`
2. Accéder au dossier ainsi créé avec la commande : `cd src`
3. Créer un environnement virtuel pour le projet avec 
    - `python -m venv env` sous Windows 
    - ou `python3 -m venv env` sous MacOS ou Linux.
4. Activez l'environnement virtuel avec 
    - `./env/Scripts/activate` sous Windows 
    - ou `source env/bin/activate` sous MacOS ou Linux.
5. Installez les dépendances du projet avec la commande `pip install -r requirements.txt`

6. Définir les variables d'environnement dans un fichier .env ainsi :

```
SECRET_KEY=*******
DEBUG=******
ALLOWED_HOSTS=******* ******
POSTGRES_USER=*******
POSTGRES_PASSWORD*******
```

### Creation de la base de données

7. Créer la base de données avec votre nom d'utilisateur sous PostgreSQL : `createdb -U UserName crmdb`
8. Renseigner votre nom d'utilisateur dans src/config/settings.py :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crmdb',
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': '',
        'PORT': '5432',
    }
}
```

9. Appliquer les migrations `python manage.py migrate`
10. Alimenter la base de données des utilisateurs `python manage.py loaddata accounts/fixtures/authentication.json`
11. Alimenter la base de données des projets `python manage.py loaddata crm/fixtures/crm.json`

En cas de problème d'encodage, ne pas hésiter à utiliser un éditeur pour ouvrir et sauvegarder les fichiers JSON avec l'encodage utf-8. Puis réalimenter (étape 10 et 11).

### Lancement du serveur
Revenir dans le terminal et tapper :

12. Démarrer le serveur avec `python manage.py runserver`

Lorsque le serveur fonctionne, après l'étape 11 de la procédure, on peut :
 - Se créer un compte avec l'url : [http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/).
 - Obtenir un token avec : [http://127.0.0.1:8000/token/](http://127.0.0.1:8000/token/).

Pour les autres endpoints, il faudra fournir le token.

Voici quelques comptes pour explorer :

  - Utilisateur : Manager1, 
  Mot de passe : epic-event

  - Utilisateur : Saler1, 
  Mot de passe : epic-event

  - Utilisateur : Saler2, 
  Mot de passe : epic-event

  - Utilisateur : Support1, 
  Mot de passe : epic-event

  - Utilisateur : Support2, 
  Mot de passe : epic-event


Une fois installé, toutes les étapes ne sont pas nécessaires. Pour les lancements ultérieurs du serveur de l'API, il suffit d'exécuter les étapes 4 et 11 à partir du répertoire racine du projet.

## Tests

Pour lancer les test, se placer dans le terminal dans le dossier : src

Puis tapper : `python manage.py test`.

## Documentation

La documentation Postman est disponible à l'adresse :

https://documenter.getpostman.com/view/14358423/TzsbKmxb