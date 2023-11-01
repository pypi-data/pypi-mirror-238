# Bibliothèque de Gestion de Tâches

Une bibliothèque Python pour la gestion efficace des tâches, des projets et des ressources.

## Table des matières

- [Bibliothèque de Gestion de Tâches](#bibliothèque-de-gestion-de-tâches)
  - [Table des matières](#table-des-matières)
  - [Description du projet](#description-du-projet)
  - [Installation](#installation)
  - [Utilisation](#utilisation)
  - [Documentation](#documentation)
  - [Contributions](#contributions)
  - [Auteurs](#auteurs)

## Description du projet

Créez une application de gestion de tâches en utilisant Python.

L'application doit permettre à l'utilisateur de :

- Ajouter une nouvelle tâche à la liste avec à minima un nom et une description
- Marquer une tâche comme terminée.
- Supprimer une tâche de la liste.
- Afficher la liste des tâches en cours.

## Installation

Pour installer cette bibliothèque, suivez ces étapes :

1. Clonez le dépôt depuis GitHub.
2. Naviguez vers le répertoire du projet : `cd nom-du-repertoire-du-projet`
3. Créez un environnement virtuel avec la commande : `python3 -m venv venv`
4. Activez votre environnement avec la commande : `source venv/bin/activate`
5. Installez les dépendances en exécutant la commande suivante : `pip install -r requirements.txt`

## Utilisation

Pour lancer l'application, exécutez la commande suivante :

```bash
python -m tasks.main
```

Vous pourrez utiliser les fonctionnalités de gestion de tâches via le menu.

## Documentation

Pour ouvrir la documentation, exécutez la commande suivante :

```bash
open docs/_build/html/index.html
```

## Déploiement Docker

### Étape 1: Configuration du Dockerfile

Le fichier 'Dockerfile' décrit comment l'application doit être construite et exécutée dans un conteneur Docker. Le 'Dockerfile' contient des informations sur l'environnement dans lequel l'application est exécutée, le répertoire de travail dans le conteneur Docker, les dépendances nécessaires et les commandes à exécuter lorsque le conteneur est démarré.

### Étape 2: Construction de l'image Docker

Pour construire l'image Docker, exécutez la commande suivante à partir du répertoire contenant le Dockerfile :

```bash
docker build -t todolistimage .
```

### Étape 3: Exécution du Conteneur Docker

Pour exécuter votre application dans un conteneur Docker, utilisez la commande suivante, en remplaçant <host_port> par le port de votre choix :

```bash
docker run -p <host_port>:<container_port> -d todolistimage
```

## Déploiement sur PyPI

### Étape 1: Mettre à jour la version dans setup.py.

Assurer le fichier setup.py est correctement configuré avec les métadonnées de projet. Mise à jour l'attribut 'Version' dans setup.py.

### Étape 2 : Configuration et utilisation de GitHub Actions

Utiliser GitHub Actions pour automatiser le processus d'envoi de versions sur PyPI. Chaque fois que vous créez une pull request sur la branche "master", il supprimera d'abord les anciens fichiers de distribution, construira un nouveau package à partir de setup.py et l'enverra sur PyPI en utilisant Twine.

Pour construire le package, y compris le fichier de distribution source et le fichier de distribution "wheel":

```bash
python setup.py sdist bdist_wheel
```

La commande crée un dossier nommé 'dist' et y génère les fichiers de distribution.

Pour publier le package Python sur PyPi:

```bash
twine upload dist/*
```

Une fois qu'une pull request est créée sur la branche "master", le flux de travail sera déclenché, et le package sera envoyé sur PyPI automatiquement.

## Contributions

Les contributions sont les bienvenues ! Pour contribuer à ce projet, suivez ces étapes :

1. Fork le projet.
2. Créez une branche pour votre fonctionnalité (git checkout -b ma-nouvelle-fonctionnalite).
3. Commit et poussez vos modifications (git commit -m 'Ajout de ma nouvelle fonctionnalité').
4. Créez une demande d'extraction.

## Auteurs

- Alban Pereira - alban.pereira@telecom-paris.fr
- Yuchen Xia - yuchen.xia@telecom-paris.fr
- Aurélien Raulo - aurelien.raulo@telecom-paris.fr
- Salimatou Traore - salimatou.traore@telecom-paris.fr
